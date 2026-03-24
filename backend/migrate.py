"""
JastCodeLab — Fix created_at columns
Jalankan: python migrate_fix.py
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "jastcodelab.db")

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    now  = datetime.now().isoformat()

    tables = ["lessons", "challenges"]

    for table in tables:
        # Cek apakah kolom sudah ada
        cur.execute(f"PRAGMA table_info({table})")
        kolom = [row[1] for row in cur.fetchall()]

        if "created_at" not in kolom:
            # Tambah kolom tanpa default (SQLite tidak support fungsi sebagai default)
            cur.execute(f"ALTER TABLE {table} ADD COLUMN created_at TEXT")
            # Isi semua baris yang ada dengan waktu sekarang
            cur.execute(f"UPDATE {table} SET created_at = ?", (now,))
            print(f"  ✅ Ditambahkan: {table}.created_at")
        else:
            # Kolom sudah ada tapi mungkin nilainya NULL — isi yang kosong
            cur.execute(f"UPDATE {table} SET created_at = ? WHERE created_at IS NULL", (now,))
            print(f"  ⏭  Sudah ada: {table}.created_at (nilai NULL diisi)")

    conn.commit()
    conn.close()
    print("\n✅ Fix selesai! Sekarang restart uvicorn.")

if __name__ == "__main__":
    migrate()