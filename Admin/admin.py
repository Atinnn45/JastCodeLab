"""
Jalankan script ini untuk membuat akun admin JCL.
Cara: python buat_admin.py
"""
import sqlite3
import hashlib
import os

# ── Konfigurasi ──
USERNAME = "admin"
EMAIL    = "admin@jcl.com"
PASSWORD = "admin123"

# Hash password
salt    = os.urandom(16).hex()
hashed  = hashlib.sha256(f"{salt}{PASSWORD}".encode()).hexdigest()
pw_hash = f"{salt}:{hashed}"

conn = sqlite3.connect("jastcodelab.db")
cur  = conn.cursor()

cur.execute("SELECT id, is_admin FROM users WHERE username = ?", (USERNAME,))
existing = cur.fetchone()

if existing:
    cur.execute(
        "UPDATE users SET is_admin=1, password_hash=?, email=? WHERE username=?",
        (pw_hash, EMAIL, USERNAME)
    )
    print(f"✅ Akun '{USERNAME}' diperbarui dan dijadikan admin!")
else:
    cur.execute(
        "INSERT INTO users (username, email, password_hash, xp, streak_days, is_admin) VALUES (?,?,?,0,0,1)",
        (USERNAME, EMAIL, pw_hash)
    )
    print(f"✅ Akun admin baru berhasil dibuat!")

conn.commit()
conn.close()

print(f"\n{'='*35}")
print(f"  Username : {USERNAME}")
print(f"  Password : {PASSWORD}")
print(f"  Email    : {EMAIL}")
print(f"  Role     : Admin ✅")
print(f"{'='*35}")
print("\nSekarang login di Frontend/login.html")
print("dengan username dan password di atas.")