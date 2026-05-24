# SecVault - Secure Cloud File Vault

SecVault is a Flask web app for encrypted file storage on AWS S3.  
Each uploaded file is encrypted before upload and can later be downloaded as a password-protected ZIP.

## Features
- User registration and login
- Password hashing for stored user credentials
- File upload, listing, and deletion per user
- Client-side style encryption flow using Diffie-Hellman key exchange + AES encryption
- Download preparation that creates a password-protected ZIP using `pyzipper`
- Basic upload/encryption timing stats

## Tech Stack
- Python + Flask
- AWS S3 (`boto3`)
- `cryptography` (DH + AES)
- `pyzipper`

## Project Structure
```text
.
|- app.py
|- s3_utils.py
|- crypto_utils.py
|- sessions_key.py
|- templates/
|  |- login.html
|  |- register.html
|  |- index.html
|- requirements.txt
|- .env.example
```

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file using `.env.example` as a guide.
4. Set required environment variables:

```env
FLASK_SECRET_KEY=replace-with-a-long-random-value
FLASK_DEBUG=0
AWS_S3_BUCKET=your-s3-bucket-name
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

5. Run:

```bash
python app.py
```

6. Open:

```text
http://127.0.0.1:5000
```

## Security Notes
- Do not commit `.env`, `users.json`, `file_keys.json`, or generated ZIP/temp files.
- This repo is now configured with `.gitignore` to exclude local secrets and runtime artifacts.
- `app.secret_key` is loaded from `FLASK_SECRET_KEY` for deployment safety.
- Existing plaintext user passwords are auto-migrated to hashed values at next successful login.

## GitHub Push Checklist
- Confirm AWS credentials are only in environment variables.
- Confirm `.env` is not committed.
- Review `git status` before each commit.
- Add a remote and push:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```
