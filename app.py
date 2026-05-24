from flask import Flask, render_template, request, send_file, redirect, url_for, session
import time, os, json, random, string
import pyzipper
from werkzeug.security import generate_password_hash, check_password_hash

from crypto_utils import generate_keys, generate_shared_key, encrypt_data, decrypt_data
from s3_utils import upload_to_s3, download_from_s3, list_files, delete_from_s3
from sessions_key import save_session_key, get_session_key, delete_session_key

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "local-dev-only-change-me")

USERS_FILE = "users.json"

# ================= Helpers =================
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def categorize_files(file_list):
    photos, videos, documents = [], [], []
    for filename in file_list:
        ext = filename.lower().split(".")[-1]
        if ext in ["jpg", "jpeg", "png", "webp", "gif"]:
            photos.append(filename)
        elif ext in ["mp4", "mkv", "avi", "mov", "webm"]:
            videos.append(filename)
        else:
            documents.append(filename)
    return photos, videos, documents

# ================= State =================
user_stats = {}
user_history = {}

# ================= Auth =================
@app.route("/register", methods=["GET", "POST"])
def register():
    users = load_users()
    if request.method == "POST":
        u, p = request.form["username"], request.form["password"]
        if u in users:
            return render_template("register.html", error="Username already exists!")
        users[u] = generate_password_hash(p)
        save_users(users)
        return render_template("register.html", success="Account created! You can login now.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    users = load_users()
    if request.method == "POST":
        u, p = request.form["username"], request.form["password"]
        stored_password = users.get(u)
        if stored_password:
            is_hashed = stored_password.startswith(("pbkdf2:", "scrypt:"))
            valid_password = (
                check_password_hash(stored_password, p)
                if is_hashed
                else stored_password == p
            )
            if valid_password:
                # Auto-migrate old plaintext passwords to hashed format.
                if not is_hashed:
                    users[u] = generate_password_hash(p)
                    save_users(users)
                session["user"] = u
                return redirect(url_for("index"))
        return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================= Dashboard =================
@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    user_stats.setdefault(user, {})
    user_history.setdefault(user, [])

    if request.method == "POST":
        file = request.files["file"]
        data = file.read()

        privA, pubA = generate_keys()
        privB, pubB = generate_keys()
        key = generate_shared_key(privA, pubB)

        save_session_key(user, file.filename, key)

        start = time.time()
        encrypted = encrypt_data(key, data)
        enc_time = time.time() - start

        start = time.time()
        upload_to_s3(user, file.filename, encrypted)
        up_time = time.time() - start

        user_stats[user] = {
            "filename": file.filename,
            "size": len(data),
            "encryption": round(enc_time, 4),
            "upload": round(up_time, 4)
        }

        user_history[user].append({
            "encryption": round(enc_time, 4),
            "upload": round(up_time, 4)
        })

    files = list_files(user)
    photos, videos, documents = categorize_files(files)

    return render_template(
        "index.html",
        user=user,
        photos=photos,
        videos=videos,
        documents=documents,
        stats=user_stats.get(user),
        history=user_history.get(user, []),
        last_password=session.pop("last_download_password", None),
        zip_ready=session.pop("zip_ready", False)
    )

# ================= Prepare Download =================
@app.route("/prepare-download/<filename>")
def prepare_download(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]

    try:
        encrypted = download_from_s3(user, filename)
    except Exception:
        return redirect(url_for("index"))

    key = get_session_key(user, filename)
    if key is None:
        return redirect(url_for("index"))
    decrypted = decrypt_data(key, encrypted)

    temp_file = f"temp_{filename}"
    zip_file = temp_file + ".zip"

    with open(temp_file, "wb") as f:
        f.write(decrypted)

    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    with pyzipper.AESZipFile(
        zip_file,
        "w",
        compression=pyzipper.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES
    ) as zf:
        zf.setpassword(password.encode())
        zf.write(temp_file, arcname=filename)

    os.remove(temp_file)

    session["last_download_password"] = password
    session["zip_path"] = zip_file
    session["zip_ready"] = True

    return redirect(url_for("index"))

# ================= Download ZIP =================
@app.route("/download-zip")
def download_zip():
    if "user" not in session:
        return redirect(url_for("login"))

    zip_path = session.get("zip_path")
    if not zip_path or not os.path.exists(zip_path):
        return redirect(url_for("index"))
    return send_file(zip_path, as_attachment=True)

# ================= Delete =================
@app.route("/delete/<filename>")
def delete_file(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    user = session["user"]
    delete_from_s3(user, filename)
    delete_session_key(user, filename)
    return redirect(url_for("index"))

# ================= Run =================
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
