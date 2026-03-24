"""
JastCodeLab — Semua Endpoint API (FastAPI Router)
=================================================
Step 1: Challenge Feedback + Streak + Level System
Step 2: Coin System + Badge System + Shop
Step 3: Friend System + Friend Leaderboard
Step 4: Duel Challenge 1v1
Step 5: Daily Challenge
"""

import subprocess
import sys
import os
import time
import tempfile
import json
import random
from datetime import date, datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Header, Depends

from database import get_db
from auth import (
    hash_password, verify_password, buat_token,
    get_user_optional, get_user_required, get_admin_required
)
from models import (
    RegisterInput, LoginInput, TokenResponse,
    LessonInput, ChallengeInput,
    RunCodeInput, RunCodeOutput,
    PostBaru, KomentarBaru, ProfilUser,
    AdminUserUpdate,
)

router = APIRouter()


# ════════════════════════════════════════
# HELPER — MySQL datetime compatibility
# ════════════════════════════════════════

def _dt(val):
    """Konversi datetime/date object dari MySQL ke string ISO."""
    if val is None:
        return None
    if hasattr(val, "isoformat"):
        return val.isoformat()
    return str(val)


def _row_to_dict(row: dict) -> dict:
    """Konversi semua field datetime/date dalam satu dict row MySQL."""
    if not row:
        return row
    return {k: _dt(v) if hasattr(v, "isoformat") else v for k, v in row.items()}


# ════════════════════════════════════════
# HELPER — Level & XP (Step 1)
# ════════════════════════════════════════

LEVEL_TABLE = [0, 100, 250, 450, 700, 1000, 1350, 1750, 2200, 2700, 3250]

def _hitung_level(xp: int) -> dict:
    """Hitung level dan progress XP berdasarkan total XP."""
    level = 1
    for i, threshold in enumerate(LEVEL_TABLE):
        if xp >= threshold:
            level = i + 1
        else:
            break
    level = min(level, len(LEVEL_TABLE))

    xp_level_ini        = LEVEL_TABLE[level - 1]
    xp_level_berikutnya = LEVEL_TABLE[level] if level < len(LEVEL_TABLE) else LEVEL_TABLE[-1] + 1000
    xp_dalam_level      = xp - xp_level_ini
    xp_rentang          = xp_level_berikutnya - xp_level_ini
    progress            = round((xp_dalam_level / xp_rentang) * 100, 1) if xp_rentang > 0 else 100.0

    return {
        "level_sekarang":      level,
        "level_berikutnya":    level + 1 if level < len(LEVEL_TABLE) else level,
        "xp_untuk_level_ini":  xp_level_ini,
        "xp_untuk_naik_level": xp_level_berikutnya,
        "progress_persen":     min(progress, 100.0),
    }


# ════════════════════════════════════════
# HELPER — Coin reward (Step 2)
# ════════════════════════════════════════

COIN_REWARD = {"mudah": 5, "menengah": 10, "sulit": 20}

def _coin_untuk_tingkat(tingkat: str) -> int:
    return COIN_REWARD.get(tingkat.lower(), 5)


# ════════════════════════════════════════
# HELPER — Normalisasi output (case-insensitive)
# ════════════════════════════════════════

def _norm_output(s: str) -> str:
    """
    Normalisasi output sebelum dibandingkan:
    - Lowercase semua huruf
    - Strip spasi di ujung tiap baris
    - Hapus baris kosong
    Sehingga user tidak perlu persis sama huruf besar/kecilnya.
    """
    if not s:
        return ""
    return "\n".join(
        line.strip().lower()
        for line in s.strip().splitlines()
        if line.strip()
    )


# ════════════════════════════════════════
# HELPER — Badge otomatis (Step 2 + 4 + 5)
# ════════════════════════════════════════

def _cek_dan_beri_badge(cur, user_id: int) -> list:
    """
    Cek kondisi semua badge dan beri yang belum dimiliki.
    Return list badge baru yang baru saja didapat.
    CATATAN: commit dilakukan oleh pemanggil.
    """
    cur.execute("""
        SELECT
            u.xp, u.coins, u.streak_days,
            (SELECT COUNT(*) FROM user_challenges  uc  WHERE uc.user_id  = u.id AND uc.selesai = 1)              AS ch_selesai,
            (SELECT COUNT(*) FROM user_lessons     ul  WHERE ul.user_id  = u.id AND ul.selesai = 1)              AS les_selesai,
            (SELECT COUNT(*) FROM posts            p   WHERE p.user_id   = u.id)                                 AS jml_post,
            (SELECT COUNT(*) FROM friends          f   WHERE (f.user_id  = u.id OR f.friend_id = u.id) AND f.status = 'accepted') AS jml_teman,
            (SELECT COUNT(*) FROM duel_matches     dm  WHERE dm.winner_id = u.id AND dm.status = 'selesai')      AS duel_menang,
            (SELECT COUNT(*) FROM user_daily_challenges udc WHERE udc.user_id = u.id)                            AS daily_total
        FROM users u
        WHERE u.id = %s
    """, (user_id,))
    u = cur.fetchone()
    if not u:
        return []

    cur.execute("SELECT badge_id FROM user_badges WHERE user_id = %s", (user_id,))
    dimiliki = {r["badge_id"] for r in cur.fetchall()}

    cur.execute("SELECT id, kode, nama, ikon FROM badges")
    semua_badge = cur.fetchall()

    kondisi = {
        "first_challenge": u["ch_selesai"]       >= 1,
        "streak_3":        u["streak_days"]       >= 3,
        "streak_7":        u["streak_days"]       >= 7,
        "lesson_5":        u["les_selesai"]       >= 5,
        "challenge_5":     u["ch_selesai"]        >= 5,
        "challenge_10":    u["ch_selesai"]        >= 10,
        "challenge_20":    u["ch_selesai"]        >= 20,
        "xp_100":          u["xp"]                >= 100,
        "xp_500":          u["xp"]                >= 500,
        "xp_1000":         u["xp"]                >= 1000,
        "first_post":      u["jml_post"]          >= 1,
        "coins_100":       (u["coins"] or 0)      >= 100,
        "first_friend":    u["jml_teman"]         >= 1,
        "first_duel_win":  u["duel_menang"]       >= 1,
        "duel_win_5":      u["duel_menang"]       >= 5,
        "daily_3":         u["daily_total"]       >= 3,
        "daily_7":         u["daily_total"]       >= 7,
        "daily_30":        u["daily_total"]       >= 30,
    }

    badge_baru = []
    now = datetime.now().isoformat()
    for badge in semua_badge:
        if badge["id"] in dimiliki:
            continue
        if kondisi.get(badge["kode"], False):
            cur.execute(
                "INSERT IGNORE INTO user_badges (user_id, badge_id, earned_at) VALUES (%s, %s, %s)",
                (user_id, badge["id"], now)
            )
            badge_baru.append({"nama": badge["nama"], "ikon": badge["ikon"]})

    return badge_baru


# ════════════════════════════════════════
# AUTH
# ════════════════════════════════════════

@router.post("/register", response_model=TokenResponse, tags=["Auth"])
def register(data: RegisterInput):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (data.username, data.email))
    if cur.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username atau email sudah digunakan")

    pw_hash = hash_password(data.password)
    cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (data.username, data.email, pw_hash))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()

    token = buat_token(user_id, data.username, is_admin=False)
    return TokenResponse(token=token, user_id=user_id, username=data.username,
                         xp=0, streak_days=0, is_admin=False)


@router.post("/login", response_model=TokenResponse, tags=["Auth"])
def login(data: LoginInput):
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT id, username, password_hash, xp, streak_days, is_admin FROM users WHERE username = %s",
                (data.username,))
    user = cur.fetchone()
    conn.close()

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Username atau password salah")

    is_admin = bool(user["is_admin"])
    token    = buat_token(user["id"], user["username"], is_admin=is_admin)
    return TokenResponse(token=token, user_id=user["id"], username=user["username"],
                         xp=user["xp"], streak_days=user["streak_days"], is_admin=is_admin)


# ════════════════════════════════════════
# USER — PROFIL & LEADERBOARD
# ════════════════════════════════════════

@router.get("/profil", tags=["User"])
def profil_saya(user=Depends(get_user_required)):
    uid  = int(user["sub"])
    conn = get_db()
    cur  = conn.cursor()

    cur.execute("""
        SELECT id, username, xp, coins, streak_days, active_title, created_at, is_admin, is_banned
        FROM users WHERE id = %s
    """, (uid,))
    u = cur.fetchone()
    if not u:
        conn.close()
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    cur.execute("SELECT COUNT(*) AS total FROM user_lessons    WHERE user_id = %s AND selesai = 1", (uid,))
    jml_lesson = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM user_challenges WHERE user_id = %s AND selesai = 1", (uid,))
    jml_challenge = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM posts WHERE user_id = %s", (uid,))
    jml_post = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM friends WHERE (user_id=%s OR friend_id=%s) AND status='accepted'", (uid, uid))
    jml_teman = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM duel_matches WHERE winner_id = %s AND status = 'selesai'", (uid,))
    duel_menang = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM user_daily_challenges WHERE user_id = %s", (uid,))
    daily_total = cur.fetchone()["total"]

    cur.execute("""
        SELECT b.kode, b.nama, b.ikon, ub.earned_at FROM user_badges ub
        JOIN badges b ON ub.badge_id = b.id WHERE ub.user_id = %s ORDER BY ub.earned_at DESC
    """, (uid,))
    badges = [_row_to_dict(r) for r in cur.fetchall()]
    conn.close()

    return {
        "id": u["id"], "username": u["username"], "xp": u["xp"],
        "coins": u["coins"] or 0, "streak_days": u["streak_days"],
        "active_title": u["active_title"], "created_at": _dt(u["created_at"]),
        "is_admin": bool(u["is_admin"]), "is_banned": bool(u["is_banned"]),
        "jumlah_pelajaran_selesai": jml_lesson,
        "jumlah_tantangan_selesai": jml_challenge,
        "jumlah_post": jml_post,
        "jumlah_teman": jml_teman,
        "duel_menang": duel_menang,
        "daily_total": daily_total,
        "badges": badges,
    }


@router.get("/user/{username}", tags=["User"])
def profil_user_lain(username: str, user=Depends(get_user_optional)):
    conn = get_db()
    cur  = conn.cursor()

    cur.execute("SELECT id, username, xp, coins, streak_days, active_title, created_at, is_banned FROM users WHERE username = %s", (username,))
    u = cur.fetchone()
    if not u or u["is_banned"]:
        conn.close()
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    uid = u["id"]
    cur.execute("SELECT COUNT(*) AS total FROM user_challenges WHERE user_id=%s AND selesai=1", (uid,))
    jml_ch = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM user_lessons WHERE user_id=%s AND selesai=1", (uid,))
    jml_les = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM friends WHERE (user_id=%s OR friend_id=%s) AND status='accepted'", (uid, uid))
    jml_teman = cur.fetchone()["total"]
    cur.execute("SELECT b.nama, b.ikon FROM user_badges ub JOIN badges b ON ub.badge_id=b.id WHERE ub.user_id=%s ORDER BY ub.earned_at DESC", (uid,))
    badges = cur.fetchall()

    status_teman = None
    arah = None
    if user:
        my_id = int(user["sub"])
        if my_id != uid:
            cur.execute("""
                SELECT status, user_id FROM friends
                WHERE (user_id=%s AND friend_id=%s) OR (user_id=%s AND friend_id=%s)
            """, (my_id, uid, uid, my_id))
            rel = cur.fetchone()
            if rel:
                status_teman = rel["status"]
                arah = "sent" if rel["user_id"] == my_id else "received"
    conn.close()

    return {
        "id": uid, "username": u["username"], "xp": u["xp"],
        "coins": u["coins"] or 0, "streak_days": u["streak_days"],
        "active_title": u["active_title"], "created_at": _dt(u["created_at"]),
        "jumlah_tantangan_selesai": jml_ch, "jumlah_pelajaran_selesai": jml_les,
        "jumlah_teman": jml_teman, "badges": badges,
        "status_teman": status_teman, "arah_permintaan": arah,
    }


@router.get("/cari-user", tags=["User"])
def cari_user(q: str, user=Depends(get_user_required)):
    if len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Kata pencarian minimal 2 karakter")

    my_id = int(user["sub"])
    conn  = get_db()
    cur   = conn.cursor()

    cur.execute("""
        SELECT id, username, xp, active_title, streak_days
        FROM users WHERE username LIKE %s AND id != %s AND is_banned = 0
        ORDER BY xp DESC LIMIT 15
    """, (f"%{q.strip()}%", my_id))
    rows = cur.fetchall()

    result = []
    for r in rows:
        cur.execute("""
            SELECT status, user_id FROM friends
            WHERE (user_id=%s AND friend_id=%s) OR (user_id=%s AND friend_id=%s)
        """, (my_id, r["id"], r["id"], my_id))
        rel = cur.fetchone()
        status_teman = rel["status"] if rel else None
        arah = ("sent" if rel["user_id"] == my_id else "received") if rel else None
        result.append({
            "id": r["id"], "username": r["username"], "xp": r["xp"],
            "active_title": r["active_title"], "streak_days": r["streak_days"],
            "status_teman": status_teman, "arah": arah,
        })
    conn.close()
    return result


@router.get("/leaderboard", tags=["User"])
def leaderboard():
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("""
        SELECT u.id, u.username, u.xp, u.coins, u.streak_days, u.active_title,
               (SELECT COUNT(*) FROM user_lessons    ul WHERE ul.user_id=u.id AND ul.selesai=1) AS pelajaran_selesai,
               (SELECT COUNT(*) FROM user_challenges uc WHERE uc.user_id=u.id AND uc.selesai=1) AS tantangan_selesai
        FROM users u WHERE u.is_banned=0 ORDER BY u.xp DESC LIMIT 10
    """)
    rows = cur.fetchall()
    conn.close()
    return [{"rank": i+1, "id": r["id"], "username": r["username"], "xp": r["xp"],
             "coins": r["coins"] or 0, "streak_days": r["streak_days"], "active_title": r["active_title"],
             "pelajaran_selesai": r["pelajaran_selesai"], "tantangan_selesai": r["tantangan_selesai"]}
            for i, r in enumerate(rows)]


# ════════════════════════════════════════
# BADGE
# ════════════════════════════════════════

@router.get("/badges/saya", tags=["Badge"])
def badge_saya(user=Depends(get_user_required)):
    user_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT b.kode, b.nama, b.deskripsi, b.ikon, ub.earned_at FROM user_badges ub
        JOIN badges b ON ub.badge_id=b.id WHERE ub.user_id=%s ORDER BY ub.earned_at DESC
    """, (user_id,))
    badges = [_row_to_dict(r) for r in cur.fetchall()]
    conn.close()
    return {"badges": badges, "total": len(badges)}


@router.get("/badges/semua", tags=["Badge"])
def semua_badge(user=Depends(get_user_optional)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, kode, nama, deskripsi, ikon FROM badges ORDER BY id")
    semua = cur.fetchall()
    dimiliki = set()
    if user:
        cur.execute("SELECT badge_id FROM user_badges WHERE user_id=%s", (int(user["sub"]),))
        dimiliki = {r["badge_id"] for r in cur.fetchall()}
    conn.close()
    return [{**b, "dimiliki": b["id"] in dimiliki} for b in semua]


# ════════════════════════════════════════
# SHOP & COSMETICS
# ════════════════════════════════════════

@router.get("/shop", tags=["Shop"])
def daftar_shop(user=Depends(get_user_optional)):
    conn = get_db(); cur = conn.cursor()

    # Ambil item unik per nama — sisakan id terkecil jika ada duplikat
    cur.execute("""
        SELECT id, nama, deskripsi, tipe, nilai, harga_coins, ikon
        FROM cosmetics
        WHERE id IN (SELECT MIN(id) FROM cosmetics GROUP BY nama)
        ORDER BY harga_coins ASC
    """)
    items = cur.fetchall()

    dibeli_ids = set()
    coins_user = 0

    if user:
        uid = int(user["sub"])
        cur.execute("SELECT cosmetic_id FROM user_cosmetics WHERE user_id=%s", (uid,))
        dibeli_ids = {r["cosmetic_id"] for r in cur.fetchall()}
        cur.execute("SELECT coins FROM users WHERE id=%s", (uid,))
        u = cur.fetchone()
        coins_user = u["coins"] if u else 0

    conn.close()
    return {
        "coins_user": coins_user or 0,
        "items": [{**item, "sudah_dibeli": item["id"] in dibeli_ids} for item in items]
    }


@router.post("/shop/beli/{cosmetic_id}", tags=["Shop"])
def beli_item(cosmetic_id: int, user=Depends(get_user_required)):
    user_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, nama, harga_coins, tipe, nilai FROM cosmetics WHERE id=%s", (cosmetic_id,))
    item = cur.fetchone()
    if not item:
        conn.close(); raise HTTPException(404, "Item tidak ditemukan")
    cur.execute("SELECT user_id FROM user_cosmetics WHERE user_id=%s AND cosmetic_id=%s", (user_id, cosmetic_id))
    if cur.fetchone():
        conn.close(); raise HTTPException(400, "Item sudah dibeli sebelumnya")
    cur.execute("SELECT coins FROM users WHERE id=%s", (user_id,))
    u = cur.fetchone()
    if not u or (u["coins"] or 0) < item["harga_coins"]:
        conn.close(); raise HTTPException(400, f"Coins tidak cukup. Butuh {item['harga_coins']}")
    cur.execute("UPDATE users SET coins=coins-%s WHERE id=%s", (item["harga_coins"], user_id))
    cur.execute("INSERT INTO user_cosmetics (user_id, cosmetic_id) VALUES (%s,%s)", (user_id, cosmetic_id))
    conn.commit()
    cur.execute("SELECT coins FROM users WHERE id=%s", (user_id,))
    sisa = cur.fetchone()["coins"]
    conn.close()
    return {"pesan": f"✅ '{item['nama']}' berhasil dibeli!", "item_nama": item["nama"],
            "coins_digunakan": item["harga_coins"], "coins_sisa": sisa}


@router.post("/shop/pakai/{cosmetic_id}", tags=["Shop"])
def pakai_item(cosmetic_id: int, user=Depends(get_user_required)):
    user_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT uc.cosmetic_id, c.tipe, c.nilai, c.nama FROM user_cosmetics uc
        JOIN cosmetics c ON uc.cosmetic_id=c.id WHERE uc.user_id=%s AND uc.cosmetic_id=%s
    """, (user_id, cosmetic_id))
    item = cur.fetchone()
    if not item:
        conn.close(); raise HTTPException(403, "Kamu belum memiliki item ini")
    if item["tipe"] == "title":
        cur.execute("UPDATE users SET active_title=%s WHERE id=%s", (item["nilai"], user_id))
    conn.commit(); conn.close()
    return {"pesan": f"✅ '{item['nama']}' sekarang aktif!", "nilai": item["nilai"]}


@router.post("/shop/lepas-title", tags=["Shop"])
def lepas_title(user=Depends(get_user_required)):
    user_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("UPDATE users SET active_title=NULL WHERE id=%s", (user_id,))
    conn.commit(); conn.close()
    return {"pesan": "Title berhasil dilepas"}


@router.get("/shop/koleksi", tags=["Shop"])
def koleksi_saya(user=Depends(get_user_required)):
    user_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.nama, c.deskripsi, c.tipe, c.nilai, c.ikon, uc.dibeli_at
        FROM user_cosmetics uc JOIN cosmetics c ON uc.cosmetic_id=c.id
        WHERE uc.user_id=%s ORDER BY uc.dibeli_at DESC
    """, (user_id,))
    items = [_row_to_dict(r) for r in cur.fetchall()]
    cur.execute("SELECT active_title FROM users WHERE id=%s", (user_id,))
    u = cur.fetchone(); conn.close()
    return {"koleksi": items, "active_title": u["active_title"] if u else None}


# ════════════════════════════════════════
# FRIEND SYSTEM (Step 3)
# ════════════════════════════════════════

@router.post("/friends/tambah/{target_id}", tags=["Friends"])
def tambah_teman(target_id: int, user=Depends(get_user_required)):
    my_id = int(user["sub"])
    if my_id == target_id:
        raise HTTPException(400, "Tidak bisa menambahkan diri sendiri")

    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE id=%s AND is_banned=0", (target_id,))
    target = cur.fetchone()
    if not target:
        conn.close(); raise HTTPException(404, "User tidak ditemukan")

    cur.execute("""
        SELECT id, status, user_id FROM friends
        WHERE (user_id=%s AND friend_id=%s) OR (user_id=%s AND friend_id=%s)
    """, (my_id, target_id, target_id, my_id))
    existing = cur.fetchone()

    if existing:
        if existing["status"] == "accepted":
            conn.close(); return {"pesan": f"Kamu sudah berteman dengan {target['username']}"}
        if existing["status"] == "pending":
            if existing["user_id"] == my_id:
                conn.close(); return {"pesan": "Permintaan pertemanan sudah dikirim sebelumnya"}
            else:
                cur.execute("UPDATE friends SET status='accepted' WHERE id=%s", (existing["id"],))
                _cek_dan_beri_badge(cur, my_id)
                _cek_dan_beri_badge(cur, target_id)
                conn.commit(); conn.close()
                return {"pesan": f"Kamu dan {target['username']} sekarang berteman! 🤝", "status": "accepted"}

    now = datetime.now().isoformat()
    cur.execute("INSERT INTO friends (user_id, friend_id, status, created_at) VALUES (%s,%s,'pending',%s)",
                (my_id, target_id, now))
    conn.commit(); conn.close()
    return {"pesan": f"Permintaan pertemanan dikirim ke {target['username']} ✉️", "status": "pending"}


@router.post("/friends/terima/{requester_id}", tags=["Friends"])
def terima_teman(requester_id: int, user=Depends(get_user_required)):
    my_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id FROM friends WHERE user_id=%s AND friend_id=%s AND status='pending'",
                (requester_id, my_id))
    rel = cur.fetchone()
    if not rel:
        conn.close(); raise HTTPException(404, "Permintaan tidak ditemukan")
    cur.execute("UPDATE friends SET status='accepted' WHERE id=%s", (rel["id"],))
    _cek_dan_beri_badge(cur, my_id)
    _cek_dan_beri_badge(cur, requester_id)
    conn.commit(); conn.close()
    return {"pesan": "Permintaan pertemanan diterima! 🤝", "status": "accepted"}


@router.post("/friends/tolak/{requester_id}", tags=["Friends"])
def tolak_teman(requester_id: int, user=Depends(get_user_required)):
    my_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("DELETE FROM friends WHERE user_id=%s AND friend_id=%s AND status='pending'",
                (requester_id, my_id))
    conn.commit(); conn.close()
    return {"pesan": "Permintaan pertemanan ditolak"}


@router.delete("/friends/hapus/{friend_id}", tags=["Friends"])
def hapus_teman(friend_id: int, user=Depends(get_user_required)):
    my_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        DELETE FROM friends
        WHERE (user_id=%s AND friend_id=%s) OR (user_id=%s AND friend_id=%s)
    """, (my_id, friend_id, friend_id, my_id))
    conn.commit(); conn.close()
    return {"pesan": "Teman berhasil dihapus"}


@router.get("/friends/saya", tags=["Friends"])
def daftar_teman(user=Depends(get_user_required)):
    my_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.username, u.xp, u.coins, u.streak_days, u.active_title,
               (SELECT COUNT(*) FROM user_challenges uc WHERE uc.user_id=u.id AND uc.selesai=1) AS ch_selesai
        FROM friends f
        JOIN users u ON (CASE WHEN f.user_id=%s THEN f.friend_id ELSE f.user_id END = u.id)
        WHERE (f.user_id=%s OR f.friend_id=%s) AND f.status='accepted' AND u.is_banned=0
        ORDER BY u.xp DESC
    """, (my_id, my_id, my_id))
    teman = cur.fetchall(); conn.close()
    return {
        "teman": [{"id": t["id"], "username": t["username"], "xp": t["xp"],
                   "coins": t["coins"] or 0, "streak_days": t["streak_days"],
                   "active_title": t["active_title"], "ch_selesai": t["ch_selesai"]}
                  for t in teman],
        "total": len(teman)
    }


@router.get("/friends/permintaan", tags=["Friends"])
def permintaan_masuk(user=Depends(get_user_required)):
    my_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.username, u.xp, u.active_title, f.created_at FROM friends f
        JOIN users u ON f.user_id=u.id WHERE f.friend_id=%s AND f.status='pending'
        ORDER BY f.created_at DESC
    """, (my_id,))
    rows = cur.fetchall(); conn.close()
    return {"permintaan": [{"id": r["id"], "username": r["username"], "xp": r["xp"],
                            "active_title": r["active_title"], "dikirim_at": _dt(r["created_at"])}
                           for r in rows], "total": len(rows)}


@router.get("/friends/leaderboard", tags=["Friends"])
def friend_leaderboard(user=Depends(get_user_required)):
    my_id = int(user["sub"])
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.username, u.xp, u.coins, u.streak_days, u.active_title,
               (SELECT COUNT(*) FROM user_challenges uc WHERE uc.user_id=u.id AND uc.selesai=1) AS ch_selesai,
               (SELECT COUNT(*) FROM user_lessons    ul WHERE ul.user_id=u.id AND ul.selesai=1) AS les_selesai
        FROM users u
        WHERE u.id=%s OR u.id IN (
            SELECT CASE WHEN f.user_id=%s THEN f.friend_id ELSE f.user_id END
            FROM friends f WHERE (f.user_id=%s OR f.friend_id=%s) AND f.status='accepted'
        )
        ORDER BY u.xp DESC
    """, (my_id, my_id, my_id, my_id))
    rows = cur.fetchall(); conn.close()
    return [{"rank": i+1, "id": r["id"], "username": r["username"], "xp": r["xp"],
             "coins": r["coins"] or 0, "streak_days": r["streak_days"],
             "active_title": r["active_title"], "ch_selesai": r["ch_selesai"],
             "les_selesai": r["les_selesai"], "is_me": r["id"] == my_id}
            for i, r in enumerate(rows)]


# ════════════════════════════════════════
# DUEL CHALLENGE 1v1 (Step 4)
# ════════════════════════════════════════

JUMLAH_SOAL_DUEL = 5
XP_MENANG_DUEL   = 30
XP_KALAH_DUEL    = 10
COIN_MENANG_DUEL = 15


def _is_teman(cur, uid1: int, uid2: int) -> bool:
    cur.execute("""
        SELECT id FROM friends
        WHERE ((user_id=%s AND friend_id=%s) OR (user_id=%s AND friend_id=%s)) AND status='accepted'
    """, (uid1, uid2, uid2, uid1))
    return cur.fetchone() is not None


@router.post("/duel/tantang/{target_id}", tags=["Duel"])
def tantang_duel(target_id: int, user=Depends(get_user_required)):
    my_id = int(user["sub"])
    if my_id == target_id:
        raise HTTPException(400, "Tidak bisa duel dengan diri sendiri")

    conn = get_db(); cur = conn.cursor()

    if not _is_teman(cur, my_id, target_id):
        conn.close(); raise HTTPException(400, "Kamu hanya bisa duel dengan teman")

    cur.execute("""
        SELECT id FROM duel_matches
        WHERE ((player1_id=%s AND player2_id=%s) OR (player1_id=%s AND player2_id=%s))
          AND status IN ('waiting','ongoing')
    """, (my_id, target_id, target_id, my_id))
    if cur.fetchone():
        conn.close(); raise HTTPException(400, "Sudah ada duel aktif dengan user ini")

    cur.execute("SELECT id, username FROM users WHERE id=%s AND is_banned=0", (target_id,))
    target = cur.fetchone()
    if not target:
        conn.close(); raise HTTPException(404, "User tidak ditemukan")

    cur.execute("SELECT id FROM challenges WHERE dipublikasi=1 ORDER BY RAND() LIMIT %s", (JUMLAH_SOAL_DUEL,))
    soal_rows = cur.fetchall()
    if len(soal_rows) < JUMLAH_SOAL_DUEL:
        conn.close(); raise HTTPException(400, f"Challenge tidak cukup. Butuh minimal {JUMLAH_SOAL_DUEL} challenge aktif")

    soal_ids = json.dumps([r["id"] for r in soal_rows])
    now      = datetime.now().isoformat()

    cur.execute("""
        INSERT INTO duel_matches (player1_id, player2_id, status, soal_ids, created_at)
        VALUES (%s, %s, 'waiting', %s, %s)
    """, (my_id, target_id, soal_ids, now))
    conn.commit()
    match_id = cur.lastrowid
    conn.close()

    return {"pesan": f"⚔️ Tantangan duel dikirim ke {target['username']}!", "match_id": match_id, "status": "waiting"}


@router.post("/duel/terima/{match_id}", tags=["Duel"])
def terima_duel(match_id: int, user=Depends(get_user_required)):
    my_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT * FROM duel_matches WHERE id=%s", (match_id,))
    match = cur.fetchone()
    if not match:
        conn.close(); raise HTTPException(404, "Match tidak ditemukan")
    if match["player2_id"] != my_id:
        conn.close(); raise HTTPException(403, "Kamu bukan lawan dalam duel ini")
    if match["status"] != "waiting":
        conn.close(); raise HTTPException(400, f"Duel sudah dalam status '{match['status']}'")

    now = datetime.now().isoformat()
    cur.execute("UPDATE duel_matches SET status='ongoing', started_at=%s WHERE id=%s", (now, match_id))
    conn.commit()

    soal_ids = json.loads(match["soal_ids"])
    cur.execute("""
        SELECT id, judul, deskripsi, kode_awal, contoh_input, contoh_output, tingkat
        FROM challenges WHERE id IN (%s)
    """ % ",".join(["%s"] * len(soal_ids)), soal_ids)
    soal_list = cur.fetchall(); conn.close()

    return {"pesan": "⚔️ Duel dimulai!", "match_id": match_id, "status": "ongoing", "soal": soal_list}


@router.post("/duel/tolak/{match_id}", tags=["Duel"])
def tolak_duel(match_id: int, user=Depends(get_user_required)):
    my_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT * FROM duel_matches WHERE id=%s AND status='waiting'", (match_id,))
    match = cur.fetchone()
    if not match:
        conn.close(); raise HTTPException(404, "Match tidak ditemukan")
    if match["player2_id"] != my_id:
        conn.close(); raise HTTPException(403, "Kamu bukan lawan dalam duel ini")
    cur.execute("UPDATE duel_matches SET status='ditolak' WHERE id=%s", (match_id,))
    conn.commit(); conn.close()
    return {"pesan": "Duel ditolak"}


@router.get("/duel/{match_id}", tags=["Duel"])
def detail_duel(match_id: int, user=Depends(get_user_required)):
    my_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT * FROM duel_matches WHERE id=%s", (match_id,))
    match = cur.fetchone()
    if not match:
        conn.close(); raise HTTPException(404, "Match tidak ditemukan")
    if match["player1_id"] != my_id and match["player2_id"] != my_id:
        conn.close(); raise HTTPException(403, "Kamu bukan peserta duel ini")

    cur.execute("SELECT id, username, xp, active_title FROM users WHERE id IN (%s,%s)",
                (match["player1_id"], match["player2_id"]))
    players = {r["id"]: r for r in cur.fetchall()}

    soal_ids = json.loads(match["soal_ids"])
    soal_list = []
    if soal_ids:
        cur.execute("""
            SELECT id, judul, deskripsi, kode_awal, contoh_input, contoh_output, tingkat
            FROM challenges WHERE id IN (%s)
        """ % ",".join(["%s"] * len(soal_ids)), soal_ids)
        soal_list = cur.fetchall()

    cur.execute("SELECT user_id, challenge_id, benar FROM duel_answers WHERE match_id=%s", (match_id,))
    jawaban_rows = cur.fetchall()
    jawaban_map  = {(r["user_id"], r["challenge_id"]): r["benar"] for r in jawaban_rows}
    conn.close()

    p1 = players.get(match["player1_id"], {})
    p2 = players.get(match["player2_id"], {})

    return {
        "match_id": match["id"], "status": match["status"],
        "score1": match["score1"], "score2": match["score2"],
        "winner_id": match["winner_id"],
        "started_at": _dt(match.get("started_at")), "finished_at": _dt(match["finished_at"]),
        "player1": {"id": p1.get("id"), "username": p1.get("username"), "active_title": p1.get("active_title")},
        "player2": {"id": p2.get("id"), "username": p2.get("username"), "active_title": p2.get("active_title")},
        "soal": soal_list,
        "jawaban": {f"{uid}_{chid}": bool(benar) for (uid, chid), benar in jawaban_map.items()},
        "is_player1": my_id == match["player1_id"],
    }


@router.post("/duel/{match_id}/submit/{challenge_id}", tags=["Duel"])
def submit_jawaban_duel(match_id: int, challenge_id: int, body: dict, user=Depends(get_user_required)):
    my_id  = int(user["sub"])
    benar  = bool(body.get("benar", False))
    conn   = get_db(); cur = conn.cursor()

    cur.execute("SELECT * FROM duel_matches WHERE id=%s AND status='ongoing'", (match_id,))
    match = cur.fetchone()
    if not match:
        conn.close(); raise HTTPException(400, "Match tidak aktif")
    if match["player1_id"] != my_id and match["player2_id"] != my_id:
        conn.close(); raise HTTPException(403, "Kamu bukan peserta duel ini")

    soal_ids = json.loads(match["soal_ids"])
    if challenge_id not in soal_ids:
        conn.close(); raise HTTPException(400, "Soal tidak termasuk dalam duel ini")

    now = datetime.now().isoformat()
    cur.execute("""
        INSERT IGNORE INTO duel_answers (match_id, user_id, challenge_id, benar, answered_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (match_id, my_id, challenge_id, 1 if benar else 0, now))
    conn.commit()

    is_p1       = my_id == match["player1_id"]
    kolom_score = "score1" if is_p1 else "score2"
    lawan_id    = match["player2_id"] if is_p1 else match["player1_id"]

    cur.execute("SELECT COUNT(*) AS total FROM duel_answers WHERE match_id=%s AND user_id=%s AND benar=1",
                (match_id, my_id))
    score_saya = cur.fetchone()["total"]
    cur.execute(f"UPDATE duel_matches SET {kolom_score}=%s WHERE id=%s", (score_saya, match_id))
    conn.commit()

    cur.execute("SELECT COUNT(*) AS total FROM duel_answers WHERE match_id=%s AND user_id=%s", (match_id, my_id))
    jawab_saya  = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM duel_answers WHERE match_id=%s AND user_id=%s", (match_id, lawan_id))
    jawab_lawan = cur.fetchone()["total"]

    hasil_duel = None

    if jawab_saya >= len(soal_ids) and jawab_lawan >= len(soal_ids):
        cur.execute("SELECT score1, score2 FROM duel_matches WHERE id=%s", (match_id,))
        scores  = cur.fetchone()
        s1, s2  = scores["score1"], scores["score2"]
        winner_id = match["player1_id"] if s1 > s2 else (match["player2_id"] if s2 > s1 else None)

        cur.execute("UPDATE duel_matches SET status='selesai', winner_id=%s, finished_at=%s WHERE id=%s",
                    (winner_id, now, match_id))

        p1_id = match["player1_id"]; p2_id = match["player2_id"]
        if winner_id:
            loser_id = p2_id if winner_id == p1_id else p1_id
            cur.execute("UPDATE users SET xp=xp+%s, coins=coins+%s WHERE id=%s",
                        (XP_MENANG_DUEL, COIN_MENANG_DUEL, winner_id))
            cur.execute("UPDATE users SET xp=xp+%s WHERE id=%s", (XP_KALAH_DUEL, loser_id))
            badge_baru = _cek_dan_beri_badge(cur, winner_id)
        else:
            cur.execute("UPDATE users SET xp=xp+%s WHERE id=%s", (XP_KALAH_DUEL, p1_id))
            cur.execute("UPDATE users SET xp=xp+%s WHERE id=%s", (XP_KALAH_DUEL, p2_id))
            badge_baru = []

        conn.commit()
        hasil_duel = {
            "selesai": True, "score1": s1, "score2": s2, "winner_id": winner_id,
            "badge_baru": badge_baru, "xp_menang": XP_MENANG_DUEL,
            "xp_kalah": XP_KALAH_DUEL, "coin_menang": COIN_MENANG_DUEL,
        }
    else:
        conn.commit()

    conn.close()
    return {"benar": benar, "score_saya": score_saya, "soal_selesai": jawab_saya,
            "total_soal": len(soal_ids), "hasil_duel": hasil_duel}


@router.get("/duel/riwayat/saya", tags=["Duel"])
def riwayat_duel(user=Depends(get_user_required)):
    my_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT dm.id, dm.status, dm.score1, dm.score2, dm.winner_id,
               dm.created_at, dm.finished_at,
               u1.username AS player1_name, u1.active_title AS p1_title,
               u2.username AS player2_name, u2.active_title AS p2_title,
               dm.player1_id, dm.player2_id
        FROM duel_matches dm
        JOIN users u1 ON dm.player1_id=u1.id JOIN users u2 ON dm.player2_id=u2.id
        WHERE dm.player1_id=%s OR dm.player2_id=%s ORDER BY dm.created_at DESC LIMIT 10
    """, (my_id, my_id))
    rows = cur.fetchall(); conn.close()

    result = []
    for r in rows:
        is_p1 = r["player1_id"] == my_id
        hasil = ("menang" if r["winner_id"] == my_id else "seri" if r["winner_id"] is None else "kalah") if r["status"] == "selesai" else r["status"]
        result.append({
            "match_id": r["id"], "status": r["status"], "hasil": hasil,
            "lawan": r["player2_name"] if is_p1 else r["player1_name"],
            "lawan_title": r["p2_title"] if is_p1 else r["p1_title"],
            "score_saya": r["score1"] if is_p1 else r["score2"],
            "score_lawan": r["score2"] if is_p1 else r["score1"],
            "created_at": _dt(r["created_at"]), "finished_at": _dt(r["finished_at"]),
        })
    return result


@router.get("/duel/notifikasi/saya", tags=["Duel"])
def notifikasi_duel(user=Depends(get_user_required)):
    my_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT dm.id, dm.created_at, u.username AS penantang, u.active_title
        FROM duel_matches dm JOIN users u ON dm.player1_id=u.id
        WHERE dm.player2_id=%s AND dm.status='waiting' ORDER BY dm.created_at DESC
    """, (my_id,))
    tantangan_masuk = cur.fetchall()
    cur.execute("""
        SELECT dm.id, u1.username AS player1, u2.username AS player2
        FROM duel_matches dm JOIN users u1 ON dm.player1_id=u1.id JOIN users u2 ON dm.player2_id=u2.id
        WHERE (dm.player1_id=%s OR dm.player2_id=%s) AND dm.status='ongoing'
    """, (my_id, my_id))
    ongoing = cur.fetchall(); conn.close()
    return {
        "tantangan_masuk": [{"match_id": r["id"], "penantang": r["username"],
                              "penantang_title": r["active_title"], "dikirim_at": _dt(r["created_at"])}
                             for r in tantangan_masuk],
        "ongoing": [{"match_id": r["id"], "player1": r["player1"], "player2": r["player2"]} for r in ongoing],
        "total_notifikasi": len(tantangan_masuk) + len(ongoing),
    }


# ════════════════════════════════════════
# DAILY CHALLENGE (Step 5)
# ════════════════════════════════════════

DAILY_XP_BONUS   = 50
DAILY_COIN_BONUS = 25


def _get_atau_buat_daily(cur) -> dict:
    today = date.today().isoformat()
    cur.execute("""
        SELECT dc.id, dc.tanggal, dc.challenge_id, dc.xp_bonus, dc.coin_bonus,
               c.judul, c.deskripsi, c.kode_awal, c.contoh_input, c.contoh_output, c.tingkat
        FROM daily_challenges dc
        JOIN challenges c ON dc.challenge_id = c.id
        WHERE dc.tanggal = %s
    """, (today,))
    existing = cur.fetchone()
    if existing:
        return existing

    cur.execute("SELECT id FROM challenges WHERE dipublikasi=1 ORDER BY RAND() LIMIT 1")
    ch = cur.fetchone()
    if not ch:
        return None

    now = datetime.now().isoformat()
    cur.execute("""
        INSERT IGNORE INTO daily_challenges (tanggal, challenge_id, xp_bonus, coin_bonus, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (today, ch["id"], DAILY_XP_BONUS, DAILY_COIN_BONUS, now))

    cur.execute("""
        SELECT dc.id, dc.tanggal, dc.challenge_id, dc.xp_bonus, dc.coin_bonus,
               c.judul, c.deskripsi, c.kode_awal, c.contoh_input, c.contoh_output, c.tingkat
        FROM daily_challenges dc
        JOIN challenges c ON dc.challenge_id = c.id
        WHERE dc.tanggal = %s
    """, (today,))
    return cur.fetchone()


def _hitung_daily_streak(cur, user_id: int) -> int:
    cur.execute("""
        SELECT tanggal FROM user_daily_challenges
        WHERE user_id = %s ORDER BY tanggal DESC LIMIT 40
    """, (user_id,))
    rows = cur.fetchall()
    if not rows:
        return 0

    streak = 0
    cek    = date.today()

    for r in rows:
        tgl = r["tanggal"]
        if not isinstance(tgl, date):
            tgl = date.fromisoformat(str(tgl))
        if tgl == cek:
            streak += 1
            cek = cek - timedelta(days=1)
        elif tgl < cek:
            break

    return streak


@router.get("/daily", tags=["Daily Challenge"])
def get_daily_challenge(user=Depends(get_user_optional)):
    conn = get_db()
    cur  = conn.cursor()

    daily = _get_atau_buat_daily(cur)
    if not daily:
        conn.commit(); conn.close()
        raise HTTPException(status_code=503, detail="Belum ada challenge tersedia. Minta admin untuk menambahkan challenge.")

    today = date.today().isoformat()
    now          = datetime.now()
    tengah_malam = datetime(now.year, now.month, now.day) + timedelta(days=1)
    sisa_detik   = int((tengah_malam - now).total_seconds())

    sudah_selesai = False
    daily_streak  = 0
    if user:
        uid = int(user["sub"])
        cur.execute("SELECT completed_at FROM user_daily_challenges WHERE user_id=%s AND tanggal=%s", (uid, today))
        sudah_selesai = cur.fetchone() is not None
        daily_streak  = _hitung_daily_streak(cur, uid)

    cur.execute("SELECT COUNT(*) AS total FROM user_daily_challenges WHERE tanggal=%s", (today,))
    total_selesai = cur.fetchone()["total"]

    conn.commit(); conn.close()

    return {
        "tanggal":       today,
        "challenge_id":  daily["challenge_id"],
        "judul":         daily["judul"],
        "deskripsi":     daily["deskripsi"],
        "kode_awal":     daily["kode_awal"],
        "contoh_input":  daily["contoh_input"],
        "contoh_output": daily["contoh_output"],
        "tingkat":       daily["tingkat"],
        "xp_bonus":      daily["xp_bonus"],
        "coin_bonus":    daily["coin_bonus"],
        "sudah_selesai": sudah_selesai,
        "daily_streak":  daily_streak,
        "sisa_detik":    sisa_detik,
        "total_selesai": total_selesai,
    }


@router.post("/daily/selesai", tags=["Daily Challenge"])
def selesaikan_daily(user=Depends(get_user_required)):
    user_id = int(user["sub"])
    today   = date.today().isoformat()
    conn    = get_db()
    cur     = conn.cursor()

    daily = _get_atau_buat_daily(cur)
    if not daily:
        conn.commit(); conn.close()
        raise HTTPException(status_code=503, detail="Belum ada challenge tersedia")

    cur.execute("SELECT completed_at FROM user_daily_challenges WHERE user_id=%s AND tanggal=%s",
                (user_id, today))
    if cur.fetchone():
        cur.execute("SELECT xp, coins FROM users WHERE id=%s", (user_id,))
        u = cur.fetchone()
        daily_streak = _hitung_daily_streak(cur, user_id)
        conn.close()
        return {
            "pesan":          "Daily challenge hari ini sudah diklaim sebelumnya",
            "sudah_diklaim":  True,
            "xp_diperoleh":   0,
            "coin_diperoleh": 0,
            "xp_total":       u["xp"],
            "coins_total":    u["coins"] or 0,
            "daily_streak":   daily_streak,
            "badge_baru":     [],
        }

    now = datetime.now().isoformat()
    cur.execute("INSERT IGNORE INTO user_daily_challenges (user_id, tanggal, completed_at) VALUES (%s,%s,%s)",
                (user_id, today, now))
    cur.execute("UPDATE users SET xp=xp+%s, coins=coins+%s WHERE id=%s",
                (daily["xp_bonus"], daily["coin_bonus"], user_id))

    badge_baru = _cek_dan_beri_badge(cur, user_id)
    conn.commit()

    cur.execute("SELECT xp, coins FROM users WHERE id=%s", (user_id,))
    u = cur.fetchone()
    daily_streak = _hitung_daily_streak(cur, user_id)
    level_info   = _hitung_level(u["xp"])
    conn.close()

    return {
        "pesan":          f"🌟 Daily Challenge selesai! +{daily['xp_bonus']} XP +{daily['coin_bonus']} Coins",
        "sudah_diklaim":  False,
        "xp_diperoleh":   daily["xp_bonus"],
        "coin_diperoleh": daily["coin_bonus"],
        "xp_total":       u["xp"],
        "coins_total":    u["coins"] or 0,
        "daily_streak":   daily_streak,
        "badge_baru":     badge_baru,
        **level_info,
    }


@router.get("/daily/riwayat", tags=["Daily Challenge"])
def riwayat_daily(user=Depends(get_user_required)):
    user_id = int(user["sub"])
    conn    = get_db(); cur = conn.cursor()

    cur.execute("""
        SELECT udc.tanggal, udc.completed_at, c.judul, c.tingkat
        FROM user_daily_challenges udc
        JOIN daily_challenges dc ON udc.tanggal = dc.tanggal
        JOIN challenges c ON dc.challenge_id = c.id
        WHERE udc.user_id = %s ORDER BY udc.tanggal DESC LIMIT 30
    """, (user_id,))
    rows = cur.fetchall()
    daily_streak = _hitung_daily_streak(cur, user_id)
    conn.close()

    return {
        "daily_streak": daily_streak,
        "total":        len(rows),
        "riwayat": [{"tanggal": _dt(r["tanggal"]), "completed_at": _dt(r["completed_at"]),
                     "judul": r["judul"], "tingkat": r["tingkat"]} for r in rows]
    }


# ════════════════════════════════════════
# PELAJARAN
# ════════════════════════════════════════

@router.get("/lessons", tags=["Pelajaran"])
def daftar_pelajaran(user=Depends(get_user_optional)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, judul, deskripsi, xp_reward, urutan FROM lessons WHERE dipublikasi=1 ORDER BY urutan")
    rows = cur.fetchall()
    selesai_ids = set()
    if user:
        cur.execute("SELECT lesson_id FROM user_lessons WHERE user_id=%s AND selesai=1", (int(user["sub"]),))
        selesai_ids = {r["lesson_id"] for r in cur.fetchall()}
    conn.close()
    return [{"id": r["id"], "judul": r["judul"], "deskripsi": r["deskripsi"], "xp_reward": r["xp_reward"],
             "urutan": r["urutan"], "selesai": r["id"] in selesai_ids,
             "terkunci": (not user) and r["urutan"] > 1}
            for r in rows]


@router.get("/lesson/{lesson_id}", tags=["Pelajaran"])
def detail_pelajaran(lesson_id: int, user=Depends(get_user_optional)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT * FROM lessons WHERE id=%s AND dipublikasi=1", (lesson_id,))
    lesson = cur.fetchone()
    if not lesson:
        conn.close(); raise HTTPException(404, "Pelajaran tidak ditemukan")
    if not user and lesson["urutan"] > 1:
        conn.close(); raise HTTPException(403, "Silakan login")
    selesai = False
    if user:
        cur.execute("SELECT selesai FROM user_lessons WHERE user_id=%s AND lesson_id=%s", (int(user["sub"]), lesson_id))
        row = cur.fetchone(); selesai = bool(row and row["selesai"])
    conn.close()
    return {"id": lesson["id"], "judul": lesson["judul"], "deskripsi": lesson["deskripsi"],
            "konten": lesson["konten"], "kode_contoh": lesson["kode_contoh"],
            "output_contoh": lesson["output_contoh"], "xp_reward": lesson["xp_reward"],
            "urutan": lesson["urutan"], "selesai": selesai}


@router.post("/lesson/{lesson_id}/selesai", tags=["Pelajaran"])
def tandai_pelajaran_selesai(lesson_id: int, user=Depends(get_user_required)):
    user_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT selesai FROM user_lessons WHERE user_id=%s AND lesson_id=%s", (user_id, lesson_id))
    if (row := cur.fetchone()) and row["selesai"]:
        conn.close(); return {"pesan": "Sudah diselesaikan sebelumnya"}
    cur.execute("SELECT xp_reward FROM lessons WHERE id=%s", (lesson_id,))
    lesson = cur.fetchone()
    if not lesson:
        conn.close(); raise HTTPException(404, "Pelajaran tidak ditemukan")
    xp = lesson["xp_reward"]; now = datetime.now().isoformat()
    cur.execute("""
        INSERT INTO user_lessons(user_id,lesson_id,selesai,completed_at) VALUES(%s,%s,1,%s)
        ON DUPLICATE KEY UPDATE selesai=1,completed_at=%s
    """, (user_id, lesson_id, now, now))
    cur.execute("UPDATE users SET xp=xp+%s WHERE id=%s", (xp, user_id))
    badge_baru = _cek_dan_beri_badge(cur, user_id)
    conn.commit(); conn.close()
    return {"pesan": f"Pelajaran selesai! +{xp} XP diperoleh", "xp_diperoleh": xp, "badge_baru": badge_baru}


# ════════════════════════════════════════
# TANTANGAN
# ════════════════════════════════════════

@router.get("/challenges", tags=["Tantangan"])
def daftar_tantangan(user=Depends(get_user_optional)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, judul, deskripsi, tingkat, xp_reward FROM challenges WHERE dipublikasi=1 ORDER BY id")
    rows = cur.fetchall()
    selesai_ids = set()
    if user:
        cur.execute("SELECT challenge_id FROM user_challenges WHERE user_id=%s AND selesai=1", (int(user["sub"]),))
        selesai_ids = {r["challenge_id"] for r in cur.fetchall()}
    conn.close()
    return [{"id": r["id"], "judul": r["judul"], "deskripsi": r["deskripsi"], "tingkat": r["tingkat"],
             "xp_reward": r["xp_reward"], "coin_reward": _coin_untuk_tingkat(r["tingkat"]),
             "selesai": r["id"] in selesai_ids, "terkunci": (not user) and i >= 1}
            for i, r in enumerate(rows)]


@router.get("/challenge/{ch_id}", tags=["Tantangan"])
def detail_tantangan(ch_id: int, user=Depends(get_user_optional)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT * FROM challenges WHERE id=%s AND dipublikasi=1", (ch_id,))
    ch = cur.fetchone()
    if not ch:
        conn.close(); raise HTTPException(404, "Tantangan tidak ditemukan")
    if not user and ch_id > 1:
        conn.close(); raise HTTPException(403, "Silakan login")
    selesai = False
    if user:
        cur.execute("SELECT selesai FROM user_challenges WHERE user_id=%s AND challenge_id=%s", (int(user["sub"]), ch_id))
        row = cur.fetchone(); selesai = bool(row and row["selesai"])
    conn.close()
    return {"id": ch["id"], "judul": ch["judul"], "deskripsi": ch["deskripsi"], "kode_awal": ch["kode_awal"],
            "contoh_input": ch["contoh_input"], "contoh_output": ch["contoh_output"], "tingkat": ch["tingkat"],
            "xp_reward": ch["xp_reward"], "coin_reward": _coin_untuk_tingkat(ch["tingkat"]), "selesai": selesai}


@router.post("/challenge/{ch_id}/selesai", tags=["Tantangan"])
def tandai_tantangan_selesai(ch_id: int, user=Depends(get_user_required)):
    user_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT selesai FROM user_challenges WHERE user_id=%s AND challenge_id=%s", (user_id, ch_id))
    row = cur.fetchone()
    if row and row["selesai"]:
        cur.execute("SELECT xp, coins, streak_days FROM users WHERE id=%s", (user_id,))
        u = cur.fetchone(); conn.close()
        return {"pesan": "Sudah diselesaikan sebelumnya", "xp_diperoleh": 0, "coin_diperoleh": 0,
                "xp_total": u["xp"], "coins_total": u["coins"] or 0, "streak_baru": u["streak_days"],
                "naik_level": False, "badge_baru": [], "sudah_selesai_sebelumnya": True, "penjelasan": "",
                **_hitung_level(u["xp"])}
    cur.execute("SELECT xp_reward, judul, contoh_output, tingkat FROM challenges WHERE id=%s", (ch_id,))
    ch = cur.fetchone()
    if not ch:
        conn.close(); raise HTTPException(404, "Tantangan tidak ditemukan")
    xp_reward   = ch["xp_reward"]
    coin_reward = _coin_untuk_tingkat(ch["tingkat"])
    now_str     = datetime.now().isoformat()
    today       = date.today().isoformat()
    yesterday   = (date.today() - timedelta(days=1)).isoformat()
    cur.execute("""
        INSERT INTO user_challenges(user_id,challenge_id,selesai,completed_at) VALUES(%s,%s,1,%s)
        ON DUPLICATE KEY UPDATE selesai=1,completed_at=%s
    """, (user_id, ch_id, now_str, now_str))
    cur.execute("SELECT xp, coins, streak_days, last_challenge_date FROM users WHERE id=%s", (user_id,))
    u = cur.fetchone()
    xp_lama   = u["xp"]; coins_lama = u["coins"] or 0; streak = u["streak_days"]
    raw_last  = u["last_challenge_date"]
    last_date = raw_last.isoformat() if hasattr(raw_last, "isoformat") else (str(raw_last) if raw_last else None)
    if last_date == today:
        pass
    elif last_date == yesterday:
        streak += 1
    else:
        streak = 1
    xp_baru    = xp_lama + xp_reward
    coins_baru = coins_lama + coin_reward
    cur.execute("UPDATE users SET xp=%s, coins=%s, streak_days=%s, last_challenge_date=%s WHERE id=%s",
                (xp_baru, coins_baru, streak, today, user_id))
    badge_baru    = _cek_dan_beri_badge(cur, user_id)
    conn.commit(); conn.close()
    level_sebelum = _hitung_level(xp_lama)["level_sekarang"]
    level_info    = _hitung_level(xp_baru)
    naik_level    = level_info["level_sekarang"] > level_sebelum
    return {"pesan": f"🎉 Tantangan '{ch['judul']}' selesai!", "xp_diperoleh": xp_reward,
            "coin_diperoleh": coin_reward, "xp_total": xp_baru, "coins_total": coins_baru,
            "streak_baru": streak, "naik_level": naik_level, "badge_baru": badge_baru,
            "sudah_selesai_sebelumnya": False, "penjelasan": ch["contoh_output"] or "", **level_info}


# ════════════════════════════════════════
# CODE RUNNER
# ════════════════════════════════════════

BANNED_KEYWORDS = [
    "import os", "import sys", "import subprocess", "__import__",
    "eval(", "exec(", "open(", "shutil", "socket", "requests"
]

@router.post("/run-code", response_model=RunCodeOutput, tags=["Code Runner"])
def run_code(data: RunCodeInput, user=Depends(get_user_optional)):
    kode = data.kode
    for keyword in BANNED_KEYWORDS:
        if keyword.lower() in kode.lower():
            return RunCodeOutput(output="", error=f"⛔ Kode mengandung operasi yang tidak diizinkan: '{keyword}'")
    if len(kode) > 5000:
        return RunCodeOutput(output="", error="⛔ Kode terlalu panjang (maksimal 5000 karakter)")
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(kode); tmp_path = f.name
        mulai  = time.time()
        result = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True, timeout=5)
        waktu  = round(time.time() - mulai, 3)
        os.unlink(tmp_path)
        if result.returncode != 0:
            return RunCodeOutput(output=result.stdout, error=result.stderr, waktu_eksekusi=waktu)
        return RunCodeOutput(output=result.stdout, waktu_eksekusi=waktu)
    except subprocess.TimeoutExpired:
        try: os.unlink(tmp_path)
        except: pass
        return RunCodeOutput(output="", error="⏱ Waktu habis! Kode berjalan lebih dari 5 detik.")
    except Exception as e:
        return RunCodeOutput(output="", error=f"Error internal: {str(e)}")


# ════════════════════════════════════════
# KOMUNITAS — POSTS
# ════════════════════════════════════════

@router.get("/posts", tags=["Komunitas"])
def daftar_post(halaman: int = 1, per_halaman: int = 10, user=Depends(get_user_optional)):
    offset = (halaman - 1) * per_halaman; conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.judul, p.konten, p.kode_snippet, p.output_preview, p.created_at,
               u.username AS penulis,
               (SELECT COUNT(*) FROM likes    l WHERE l.post_id=p.id) AS jumlah_like,
               (SELECT COUNT(*) FROM komentar k WHERE k.post_id=p.id) AS jumlah_komentar
        FROM posts p JOIN users u ON p.user_id=u.id WHERE p.is_hidden=0
        ORDER BY p.created_at DESC LIMIT %s OFFSET %s
    """, (per_halaman, offset))
    rows = cur.fetchall()
    cur.execute("SELECT COUNT(*) AS total FROM posts WHERE is_hidden=0")
    total = cur.fetchone()["total"]
    user_likes = set()
    if user:
        cur.execute("SELECT post_id FROM likes WHERE user_id=%s", (int(user["sub"]),))
        user_likes = {r["post_id"] for r in cur.fetchall()}
    conn.close()
    return {"total": total, "halaman": halaman, "per_halaman": per_halaman,
            "posts": [{"id": r["id"], "judul": r["judul"], "konten": r["konten"],
                       "kode_snippet": r["kode_snippet"], "output_preview": r["output_preview"],
                       "created_at": _dt(r["created_at"]), "penulis": r["penulis"],
                       "jumlah_like": r["jumlah_like"], "jumlah_komentar": r["jumlah_komentar"],
                       "sudah_dilike": r["id"] in user_likes}
                      for r in rows]}


@router.post("/posts", tags=["Komunitas"])
def buat_post(data: PostBaru, user=Depends(get_user_required)):
    user_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("INSERT INTO posts(user_id,judul,konten,kode_snippet,output_preview) VALUES(%s,%s,%s,%s,%s)",
                (user_id, data.judul, data.konten, data.kode_snippet, data.output_preview))
    post_id = cur.lastrowid
    cur.execute("UPDATE users SET xp=xp+5 WHERE id=%s", (user_id,))
    badge_baru = _cek_dan_beri_badge(cur, user_id)
    conn.commit(); conn.close()
    return {"pesan": "Post berhasil dibuat! +5 XP", "post_id": post_id, "badge_baru": badge_baru}


@router.get("/posts/{post_id}", tags=["Komunitas"])
def detail_post(post_id: int, user=Depends(get_user_optional)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        SELECT p.*, u.username AS penulis,
               (SELECT COUNT(*) FROM likes l WHERE l.post_id=p.id) AS jumlah_like
        FROM posts p JOIN users u ON p.user_id=u.id WHERE p.id=%s AND p.is_hidden=0
    """, (post_id,))
    post = cur.fetchone()
    if not post:
        conn.close(); raise HTTPException(404, "Post tidak ditemukan")
    cur.execute("""
        SELECT k.id, k.isi, k.created_at, u.username AS penulis
        FROM komentar k JOIN users u ON k.user_id=u.id WHERE k.post_id=%s ORDER BY k.created_at
    """, (post_id,))
    komentar_list = cur.fetchall()
    sudah_dilike = False
    if user:
        cur.execute("SELECT id FROM likes WHERE user_id=%s AND post_id=%s", (int(user["sub"]), post_id))
        sudah_dilike = cur.fetchone() is not None
    conn.close()
    return {"id": post["id"], "judul": post["judul"], "konten": post["konten"],
            "kode_snippet": post["kode_snippet"], "output_preview": post["output_preview"],
            "created_at": _dt(post["created_at"]), "penulis": post["penulis"],
            "jumlah_like": post["jumlah_like"], "sudah_dilike": sudah_dilike,
            "komentar": [_row_to_dict(k) for k in komentar_list]}


@router.post("/posts/{post_id}/like", tags=["Komunitas"])
def toggle_like(post_id: int, user=Depends(get_user_required)):
    user_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id FROM likes WHERE user_id=%s AND post_id=%s", (user_id, post_id))
    if cur.fetchone():
        cur.execute("DELETE FROM likes WHERE user_id=%s AND post_id=%s", (user_id, post_id))
        conn.commit()
        cur.execute("SELECT COUNT(*) AS total FROM likes WHERE post_id=%s", (post_id,))
        t = cur.fetchone()["total"]; conn.close()
        return {"aksi": "unlike", "jumlah_like": t}
    cur.execute("INSERT INTO likes(user_id,post_id) VALUES(%s,%s)", (user_id, post_id))
    conn.commit()
    cur.execute("SELECT COUNT(*) AS total FROM likes WHERE post_id=%s", (post_id,))
    t = cur.fetchone()["total"]; conn.close()
    return {"aksi": "like", "jumlah_like": t}


@router.post("/posts/{post_id}/komentar", tags=["Komunitas"])
def tambah_komentar(post_id: int, data: KomentarBaru, user=Depends(get_user_required)):
    user_id = int(user["sub"]); conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id FROM posts WHERE id=%s", (post_id,))
    if not cur.fetchone():
        conn.close(); raise HTTPException(404, "Post tidak ditemukan")
    cur.execute("INSERT INTO komentar(post_id,user_id,isi) VALUES(%s,%s,%s)", (post_id, user_id, data.isi))
    conn.commit(); kid = cur.lastrowid; conn.close()
    return {"pesan": "Komentar berhasil ditambahkan", "komentar_id": kid}


# ════════════════════════════════════════
# ADMIN
# ════════════════════════════════════════

@router.get("/admin/stats", tags=["Admin"])
def admin_stats(admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS total FROM users");              tu = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM lessons");            tl = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM challenges");         tc = cur.fetchone()["total"]
    cur.execute("SELECT COUNT(*) AS total FROM posts WHERE is_hidden=0"); tp = cur.fetchone()["total"]
    cur.execute("SELECT COALESCE(SUM(xp),0) AS total FROM users");  tx = cur.fetchone()["total"]
    cur.execute("""
        SELECT COUNT(DISTINCT user_id) AS total FROM (
            SELECT user_id FROM user_lessons    WHERE completed_at>=DATE_SUB(NOW(),INTERVAL 7 DAY)
            UNION SELECT user_id FROM user_challenges WHERE completed_at>=DATE_SUB(NOW(),INTERVAL 7 DAY)
        ) a
    """)
    ua = cur.fetchone()["total"]
    conn.close()
    return {"total_users": tu, "total_lessons": tl, "total_challenges": tc, "total_posts": tp,
            "total_xp_diberikan": tx, "user_aktif_7_hari": ua}


@router.get("/admin/users", tags=["Admin"])
def admin_daftar_user(halaman: int = 1, per_halaman: int = 20, cari: str = "", admin=Depends(get_admin_required)):
    offset = (halaman - 1) * per_halaman; conn = get_db(); cur = conn.cursor()
    if cari:
        like = f"%{cari}%"
        cur.execute("""
            SELECT id,username,email,xp,coins,streak_days,is_admin,is_banned,created_at
            FROM users WHERE username LIKE %s OR email LIKE %s
            ORDER BY created_at DESC LIMIT %s OFFSET %s
        """, (like, like, per_halaman, offset))
        rows = cur.fetchall()
        cur.execute("SELECT COUNT(*) AS total FROM users WHERE username LIKE %s OR email LIKE %s", (like, like))
    else:
        cur.execute("""
            SELECT id,username,email,xp,coins,streak_days,is_admin,is_banned,created_at
            FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s
        """, (per_halaman, offset))
        rows = cur.fetchall()
        cur.execute("SELECT COUNT(*) AS total FROM users")
    total = cur.fetchone()["total"]; conn.close()
    return {"total": total, "halaman": halaman, "per_halaman": per_halaman,
            "users": [{"id": r["id"], "username": r["username"], "email": r["email"], "xp": r["xp"],
                       "coins": r["coins"] or 0, "streak_days": r["streak_days"],
                       "is_admin": bool(r["is_admin"]), "is_banned": bool(r["is_banned"]),
                       "created_at": _dt(r["created_at"])}
                      for r in rows]}


@router.patch("/admin/users/{user_id}", tags=["Admin"])
def admin_update_user(user_id: int, data: AdminUserUpdate, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE id=%s", (user_id,))
    target = cur.fetchone()
    if not target:
        conn.close(); raise HTTPException(404, "User tidak ditemukan")
    updates, values = [], []
    if data.is_admin  is not None: updates.append("is_admin=%s");  values.append(1 if data.is_admin else 0)
    if data.is_banned is not None: updates.append("is_banned=%s"); values.append(1 if data.is_banned else 0)
    if data.xp        is not None: updates.append("xp=%s");        values.append(data.xp)
    if not updates:
        conn.close(); return {"pesan": "Tidak ada perubahan"}
    values.append(user_id)
    cur.execute(f"UPDATE users SET {', '.join(updates)} WHERE id=%s", values)
    conn.commit(); conn.close()
    return {"pesan": f"User '{target['username']}' berhasil diperbarui"}


@router.delete("/admin/users/{user_id}", tags=["Admin"])
def admin_hapus_user(user_id: int, admin=Depends(get_admin_required)):
    if user_id == int(admin["sub"]):
        raise HTTPException(400, "Tidak bisa hapus akun sendiri")
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE id=%s", (user_id,))
    target = cur.fetchone()
    if not target:
        conn.close(); raise HTTPException(404, "User tidak ditemukan")
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit(); conn.close()
    return {"pesan": f"User '{target['username']}' berhasil dihapus"}


@router.get("/admin/lessons", tags=["Admin"])
def admin_daftar_lesson(admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id,judul,deskripsi,xp_reward,urutan,dipublikasi,created_at FROM lessons ORDER BY urutan")
    rows = cur.fetchall(); conn.close()
    return [_row_to_dict(r) for r in rows]


@router.post("/admin/lessons", tags=["Admin"])
def admin_buat_lesson(data: LessonInput, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        INSERT INTO lessons(judul,deskripsi,konten,kode_contoh,output_contoh,xp_reward,urutan,dipublikasi)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """, (data.judul, data.deskripsi, data.konten, data.kode_contoh, data.output_contoh,
          data.xp_reward, data.urutan, 1 if data.dipublikasi else 0))
    conn.commit(); lid = cur.lastrowid; conn.close()
    return {"pesan": "Lesson dibuat", "lesson_id": lid}


@router.put("/admin/lessons/{lesson_id}", tags=["Admin"])
def admin_edit_lesson(lesson_id: int, data: LessonInput, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id FROM lessons WHERE id=%s", (lesson_id,))
    if not cur.fetchone():
        conn.close(); raise HTTPException(404, "Lesson tidak ditemukan")
    cur.execute("""
        UPDATE lessons SET judul=%s,deskripsi=%s,konten=%s,kode_contoh=%s,output_contoh=%s,
        xp_reward=%s,urutan=%s,dipublikasi=%s WHERE id=%s
    """, (data.judul, data.deskripsi, data.konten, data.kode_contoh, data.output_contoh,
          data.xp_reward, data.urutan, 1 if data.dipublikasi else 0, lesson_id))
    conn.commit(); conn.close()
    return {"pesan": "Lesson diperbarui"}


@router.delete("/admin/lessons/{lesson_id}", tags=["Admin"])
def admin_hapus_lesson(lesson_id: int, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT judul FROM lessons WHERE id=%s", (lesson_id,))
    l = cur.fetchone()
    if not l:
        conn.close(); raise HTTPException(404, "Lesson tidak ditemukan")
    cur.execute("DELETE FROM lessons WHERE id=%s", (lesson_id,))
    conn.commit(); conn.close()
    return {"pesan": f"Lesson '{l['judul']}' dihapus"}


@router.get("/admin/challenges", tags=["Admin"])
def admin_daftar_challenge(admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id,judul,deskripsi,tingkat,xp_reward,dipublikasi,created_at FROM challenges ORDER BY id")
    rows = cur.fetchall(); conn.close()
    return [_row_to_dict(r) for r in rows]


@router.post("/admin/challenges", tags=["Admin"])
def admin_buat_challenge(data: ChallengeInput, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("""
        INSERT INTO challenges(judul,deskripsi,kode_awal,contoh_input,contoh_output,tingkat,xp_reward,dipublikasi)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """, (data.judul, data.deskripsi, data.kode_awal, data.contoh_input, data.contoh_output,
          data.tingkat, data.xp_reward, 1 if data.dipublikasi else 0))
    conn.commit(); cid = cur.lastrowid; conn.close()
    return {"pesan": "Challenge dibuat", "challenge_id": cid}


@router.put("/admin/challenges/{ch_id}", tags=["Admin"])
def admin_edit_challenge(ch_id: int, data: ChallengeInput, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id FROM challenges WHERE id=%s", (ch_id,))
    if not cur.fetchone():
        conn.close(); raise HTTPException(404, "Challenge tidak ditemukan")
    cur.execute("""
        UPDATE challenges SET judul=%s,deskripsi=%s,kode_awal=%s,contoh_input=%s,contoh_output=%s,
        tingkat=%s,xp_reward=%s,dipublikasi=%s WHERE id=%s
    """, (data.judul, data.deskripsi, data.kode_awal, data.contoh_input, data.contoh_output,
          data.tingkat, data.xp_reward, 1 if data.dipublikasi else 0, ch_id))
    conn.commit(); conn.close()
    return {"pesan": "Challenge diperbarui"}


@router.delete("/admin/challenges/{ch_id}", tags=["Admin"])
def admin_hapus_challenge(ch_id: int, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT judul FROM challenges WHERE id=%s", (ch_id,))
    ch = cur.fetchone()
    if not ch:
        conn.close(); raise HTTPException(404, "Challenge tidak ditemukan")
    cur.execute("DELETE FROM challenges WHERE id=%s", (ch_id,))
    conn.commit(); conn.close()
    return {"pesan": f"Challenge '{ch['judul']}' dihapus"}


@router.get("/admin/posts", tags=["Admin"])
def admin_daftar_post(halaman: int = 1, per_halaman: int = 20, tampilkan: str = "semua",
                      admin=Depends(get_admin_required)):
    offset = (halaman - 1) * per_halaman; conn = get_db(); cur = conn.cursor()
    where  = {"tersembunyi": "WHERE p.is_hidden=1", "aktif": "WHERE p.is_hidden=0"}.get(tampilkan, "")
    cur.execute(f"""
        SELECT p.id, p.judul, p.konten, p.kode_snippet, p.created_at, p.is_hidden,
               u.username AS penulis,
               (SELECT COUNT(*) FROM likes    l WHERE l.post_id=p.id) AS jumlah_like,
               (SELECT COUNT(*) FROM komentar k WHERE k.post_id=p.id) AS jumlah_komentar
        FROM posts p JOIN users u ON p.user_id=u.id {where}
        ORDER BY p.created_at DESC LIMIT %s OFFSET %s
    """, (per_halaman, offset))
    rows = cur.fetchall()
    cur.execute(f"SELECT COUNT(*) AS total FROM posts p {where}")
    total = cur.fetchone()["total"]; conn.close()
    return {"total": total, "halaman": halaman, "per_halaman": per_halaman,
            "posts": [{"id": r["id"], "judul": r["judul"], "konten": r["konten"],
                       "kode_snippet": r["kode_snippet"], "created_at": _dt(r["created_at"]),
                       "is_hidden": bool(r["is_hidden"]), "penulis": r["penulis"],
                       "jumlah_like": r["jumlah_like"], "jumlah_komentar": r["jumlah_komentar"]}
                      for r in rows]}


@router.patch("/admin/posts/{post_id}/sembunyikan", tags=["Admin"])
def admin_sembunyikan_post(post_id: int, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, is_hidden FROM posts WHERE id=%s", (post_id,))
    p = cur.fetchone()
    if not p:
        conn.close(); raise HTTPException(404, "Post tidak ditemukan")
    ns = 0 if p["is_hidden"] else 1
    cur.execute("UPDATE posts SET is_hidden=%s WHERE id=%s", (ns, post_id))
    conn.commit(); conn.close()
    return {"pesan": f"Post {'disembunyikan' if ns else 'ditampilkan'}", "is_hidden": bool(ns)}


@router.delete("/admin/posts/{post_id}", tags=["Admin"])
def admin_hapus_post(post_id: int, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT judul FROM posts WHERE id=%s", (post_id,))
    p = cur.fetchone()
    if not p:
        conn.close(); raise HTTPException(404, "Post tidak ditemukan")
    cur.execute("DELETE FROM posts WHERE id=%s", (post_id,))
    conn.commit(); conn.close()
    return {"pesan": f"Post '{p['judul']}' dihapus"}


@router.post("/admin/buat-admin/{user_id}", tags=["Admin"])
def jadikan_admin(user_id: int, admin=Depends(get_admin_required)):
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin FROM users WHERE id=%s", (user_id,))
    target = cur.fetchone()
    if not target:
        conn.close(); raise HTTPException(404, "User tidak ditemukan")
    if target["is_admin"]:
        conn.close(); return {"pesan": f"'{target['username']}' sudah admin"}
    cur.execute("UPDATE users SET is_admin=1 WHERE id=%s", (user_id,))
    conn.commit(); conn.close()
    return {"pesan": f"'{target['username']}' berhasil dijadikan admin"}