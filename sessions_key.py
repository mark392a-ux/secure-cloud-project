import json
import os

KEY_FILE = "file_keys.json"

# Load keys
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "r") as f:
        session_key_store = json.load(f)
else:
    session_key_store = {}

def _save():
    with open(KEY_FILE, "w") as f:
        json.dump(session_key_store, f)

def make_key(username, filename):
    return f"{username}/{filename}"

def save_session_key(username, filename, key):
    session_key_store[make_key(username, filename)] = key.hex()
    _save()

def get_session_key(username, filename):
    k = make_key(username, filename)
    val = session_key_store.get(k)
    if val is None:
        return None
    return bytes.fromhex(val)

def delete_session_key(username, filename):
    k = make_key(username, filename)
    if k in session_key_store:
        del session_key_store[k]
        _save()
