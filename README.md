# SecVault — Secure Cloud File Vault

> A Flask web app for encrypted file storage on AWS S3, featuring Diffie-Hellman key exchange, AES encryption, and password-protected ZIP downloads.

---

## Screenshots

| Login Page | Dashboard & File Management |
|:---:|:---:|
| ![Login](https://raw.githubusercontent.com/mark392a-ux/secure-cloud-project/main/docs/screenshots/login.png) | ![Dashboard](https://raw.githubusercontent.com/mark392a-ux/secure-cloud-project/main/docs/screenshots/dashboard.png) |

---

## Features

- **User authentication** — registration, login, password hashing with auto-migration of plaintext credentials at next login
- **Encrypted file storage** — Diffie-Hellman key exchange + AES encryption before every S3 upload
- **File management** — upload, list, and delete files per user
- **Secure downloads** — files packaged as password-protected ZIPs via `pyzipper`
- **Session key management** — per-user session keys stored separately from file data
- **Upload stats** — basic encryption and upload timing metrics

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Cloud Storage | AWS S3 (boto3) |
| Cryptography | Diffie-Hellman key exchange, AES (cryptography lib) |
| Downloads | pyzipper (password-protected ZIP) |
| Frontend | HTML, CSS, JavaScript |

---

## Project Structure

```text
secure-cloud-project/
├── app.py              # Flask app entrypoint and routes
├── crypto_utils.py     # DH key exchange + AES encryption/decryption
├── s3_utils.py         # AWS S3 upload/download/delete helpers
├── sessions_key.py     # Per-user session key management
├── templates/
│   ├── login.html
│   ├── register.html
│   └── index.html
├── requirements.txt
├── .env.example        # Environment variable template
└── .gitignore
```

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/mark392a-ux/secure-cloud-project.git
cd secure-cloud-project
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
```

Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
FLASK_SECRET_KEY=replace-with-a-long-random-value
FLASK_DEBUG=0
AWS_S3_BUCKET=your-s3-bucket-name
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

**5. Run the app**

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Security Notes

- AWS credentials live only in environment variables — never hardcoded
- `.env`, `users.json`, `file_keys.json`, and generated ZIP/temp files are excluded via `.gitignore`
- `app.secret_key` is loaded from `FLASK_SECRET_KEY` at runtime
- Plaintext passwords in existing `users.json` are auto-migrated to hashed values on next successful login
- Always run `git status` before committing to confirm no secrets are staged

---

## What I Learned

- Implementing cryptographic protocols (Diffie-Hellman + AES) in a real application
- Integrating AWS S3 with Python using `boto3`
- Applying Flask security best practices: password hashing, session management, secret key loading
- Handling encrypted file lifecycles — upload, storage, and secure download

---

## Roadmap

- [ ] Two-factor authentication (2FA)
- [ ] Shareable download links with expiration
- [ ] Audit logging and activity monitoring
- [ ] Migrate from JSON to SQLite / PostgreSQL
- [ ] Docker + CI/CD pipeline

---

## License

MIT License — see [LICENSE](./LICENSE) for details.

---

## Contact

For questions or feedback, open a GitHub Issue or submit a pull request.
