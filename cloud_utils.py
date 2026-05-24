import os

CLOUD_FOLDER = "uploads"

# Create folder if not exists
if not os.path.exists(CLOUD_FOLDER):
    os.makedirs(CLOUD_FOLDER)

def upload_to_cloud(filename, data):
    path = os.path.join(CLOUD_FOLDER, filename)
    with open(path, "wb") as f:
        f.write(data)
    return path

def download_from_cloud(filename):
    path = os.path.join(CLOUD_FOLDER, filename)
    with open(path, "rb") as f:
        return f.read()
