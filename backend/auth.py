"""
JastCodeLab — Autentikasi (JWT + Password Hashing)

PERBAIKAN dari versi sebelumnya:
1. _sign() — pakai hmac.new() yang benar (ada di Python stdlib)
2. verifikasi_token() — padding base64 diperbaiki dengan cara yang benar
3. created_at di MySQL bertipe datetime object, bukan string
   → routes.py perlu str() saat mengembalikan ke JSON (sudah dihandle di ProfilUser model)
"""

import hashlib
import hmac
import os
import base64
import json
import time
from typing import Optional
from fastapi import HTTPException, Header

SECRET_KEY = os.environ.get("SECRET_KEY", "jastcodelab-secret-key-ganti-di-production")


# ════════════════════════════════════════
# PASSWORD HASHING (SHA-256 + salt)
# ════════════════════════════════════════

def hash_password(password: str) -> str:
    """Hash password menggunakan SHA-256 dengan salt acak."""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verifikasi password dengan hash yang tersimpan."""
    try:
        salt, hashed = password_hash.split(":", 1)
        expected = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        return hmac.compare_digest(expected, hashed)
    except Exception:
        return False


# ════════════════════════════════════════
# JWT SEDERHANA
# ════════════════════════════════════════

def _b64url_encode(data: bytes) -> str:
    """Encode bytes ke base64url tanpa padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(s: str) -> bytes:
    """
    Decode base64url string ke bytes.
    FIX: tambah padding yang TEPAT, bukan selalu '==' (bisa salah untuk string kelipatan 4).
    Rumus: padding = (4 - len(s) % 4) % 4
    """
    padding = (4 - len(s) % 4) % 4
    return base64.urlsafe_b64decode(s + "=" * padding)


def _sign(data: str) -> str:
    """
    Buat HMAC-SHA256 signature untuk data string.
    FIX: pakai hmac.new() dengan cara yang benar.
    """
    mac = hmac.new(
        SECRET_KEY.encode("utf-8"),
        data.encode("utf-8"),
        hashlib.sha256
    )
    return _b64url_encode(mac.digest())


def buat_token(user_id: int, username: str, is_admin: bool = False) -> str:
    """Buat JWT token untuk user. Token berlaku 7 hari."""
    header  = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = _b64url_encode(json.dumps({
        "sub":      str(user_id),   # selalu string agar konsisten
        "username": username,
        "is_admin": is_admin,
        "iat":      int(time.time()),
        "exp":      int(time.time()) + 60 * 60 * 24 * 7,  # 7 hari
    }, separators=(",", ":")).encode())
    signature = _sign(f"{header}.{payload}")
    return f"{header}.{payload}.{signature}"


def verifikasi_token(token: str) -> Optional[dict]:
    """
    Verifikasi JWT token dan kembalikan payload jika valid.
    Return None jika token tidak valid, expired, atau format salah.

    FIX:
    - Padding base64 dihitung dengan benar
    - Tangkap semua exception dengan detail
    """
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            return None

        header, payload, signature = parts

        # Verifikasi signature
        expected_sig = _sign(f"{header}.{payload}")
        if not hmac.compare_digest(signature, expected_sig):
            return None

        # Decode payload — FIX: gunakan _b64url_decode yang benar
        data = json.loads(_b64url_decode(payload))

        # Cek expiry
        if data.get("exp", 0) < time.time():
            return None

        # Pastikan field wajib ada
        if "sub" not in data:
            return None

        return data

    except Exception:
        return None


# ════════════════════════════════════════
# DEPENDENCY HELPERS (dipakai di routes)
# ════════════════════════════════════════

def get_user_optional(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """
    Ambil data user dari token JWT.
    Kembalikan None jika tidak ada token atau token tidak valid.
    Tidak melempar exception — aman untuk endpoint guest.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[7:].strip()
    if not token:
        return None
    return verifikasi_token(token)


def get_user_required(authorization: Optional[str] = Header(None)) -> dict:
    """
    Wajib login. Lempar 401 jika tidak ada token valid.
    """
    user = get_user_optional(authorization)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Silakan login terlebih dahulu"
        )
    return user


def get_admin_required(authorization: Optional[str] = Header(None)) -> dict:
    """
    Wajib login DAN harus admin.
    Lempar 401 jika tidak login, 403 jika bukan admin.
    """
    user = get_user_optional(authorization)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Silakan login terlebih dahulu"
        )
    if not user.get("is_admin", False):
        raise HTTPException(
            status_code=403,
            detail="Akses ditolak: hanya admin yang diizinkan"
        )
    return user