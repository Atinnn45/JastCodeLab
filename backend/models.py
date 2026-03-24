"""
JastCodeLab — Model Data (Pydantic Schemas)
"""

from pydantic import BaseModel, field_validator
from typing import Optional
import re


# ════════════════════════════════════════
# AUTH
# ════════════════════════════════════════

class RegisterInput(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username minimal 3 karakter")
        if len(v) > 30:
            raise ValueError("Username maksimal 30 karakter")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username hanya boleh huruf, angka, dan underscore")
        return v

    @field_validator("email")
    @classmethod
    def email_valid(cls, v):
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Format email tidak valid")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if len(v) < 6:
            raise ValueError("Password minimal 6 karakter")
        return v


class LoginInput(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
    user_id: int
    username: str
    xp: int
    streak_days: int
    is_admin: bool = False


# ════════════════════════════════════════
# LESSONS
# ════════════════════════════════════════

class LessonRingkas(BaseModel):
    id: int
    judul: str
    deskripsi: str
    xp_reward: int
    urutan: int
    selesai: bool = False


class LessonDetail(BaseModel):
    id: int
    judul: str
    deskripsi: str
    konten: str
    kode_contoh: str
    output_contoh: str
    xp_reward: int
    urutan: int
    selesai: bool = False


# Input untuk admin membuat / mengedit lesson
class LessonInput(BaseModel):
    judul: str
    deskripsi: str
    konten: str
    kode_contoh: str = ""
    output_contoh: str = ""
    xp_reward: int = 20
    urutan: int = 0
    dipublikasi: bool = True

    @field_validator("judul")
    @classmethod
    def judul_valid(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Judul minimal 3 karakter")
        if len(v) > 200:
            raise ValueError("Judul maksimal 200 karakter")
        return v

    @field_validator("konten")
    @classmethod
    def konten_valid(cls, v):
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Konten minimal 10 karakter")
        return v

    @field_validator("xp_reward")
    @classmethod
    def xp_valid(cls, v):
        if v < 0:
            raise ValueError("XP reward tidak boleh negatif")
        if v > 1000:
            raise ValueError("XP reward maksimal 1000")
        return v


# ════════════════════════════════════════
# CHALLENGES
# ════════════════════════════════════════

class ChallengeRingkas(BaseModel):
    id: int
    judul: str
    deskripsi: str
    tingkat: str
    xp_reward: int
    selesai: bool = False


class ChallengeDetail(BaseModel):
    id: int
    judul: str
    deskripsi: str
    kode_awal: str
    contoh_input: str
    contoh_output: str
    tingkat: str
    xp_reward: int
    selesai: bool = False


# Input untuk admin membuat / mengedit challenge
class ChallengeInput(BaseModel):
    judul: str
    deskripsi: str
    kode_awal: str = ""
    contoh_input: str = ""
    contoh_output: str = ""
    tingkat: str = "mudah"
    xp_reward: int = 30
    dipublikasi: bool = True

    @field_validator("judul")
    @classmethod
    def judul_valid(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Judul minimal 3 karakter")
        return v

    @field_validator("tingkat")
    @classmethod
    def tingkat_valid(cls, v):
        allowed = {"mudah", "menengah", "sulit"}
        if v.lower() not in allowed:
            raise ValueError(f"Tingkat harus salah satu dari: {', '.join(allowed)}")
        return v.lower()

    @field_validator("xp_reward")
    @classmethod
    def xp_valid(cls, v):
        if v < 0:
            raise ValueError("XP reward tidak boleh negatif")
        return v


# ════════════════════════════════════════
# CODE RUNNER
# ════════════════════════════════════════

class RunCodeInput(BaseModel):
    kode: str
    challenge_id: Optional[int] = None


class RunCodeOutput(BaseModel):
    output: str
    error: Optional[str] = None
    waktu_eksekusi: float = 0.0


# ════════════════════════════════════════
# POSTS (KOMUNITAS)
# ════════════════════════════════════════

class PostBaru(BaseModel):
    judul: str
    konten: str
    kode_snippet: str = ""
    output_preview: str = ""

    @field_validator("judul")
    @classmethod
    def judul_valid(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Judul minimal 3 karakter")
        if len(v) > 200:
            raise ValueError("Judul maksimal 200 karakter")
        return v

    @field_validator("konten")
    @classmethod
    def konten_valid(cls, v):
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Konten minimal 10 karakter")
        return v


class KomentarBaru(BaseModel):
    isi: str

    @field_validator("isi")
    @classmethod
    def isi_valid(cls, v):
        v = v.strip()
        if len(v) < 1:
            raise ValueError("Komentar tidak boleh kosong")
        return v


# ════════════════════════════════════════
# USER
# ════════════════════════════════════════

class ProfilUser(BaseModel):
    id: int
    username: str
    xp: int
    streak_days: int
    created_at: str
    is_admin: bool = False
    is_banned: bool = False
    jumlah_pelajaran_selesai: int = 0
    jumlah_tantangan_selesai: int = 0
    jumlah_post: int = 0


# ════════════════════════════════════════
# ADMIN
# ════════════════════════════════════════

class AdminUserUpdate(BaseModel):
    """Admin mengubah status user."""
    is_admin: Optional[bool] = None
    is_banned: Optional[bool] = None
    xp: Optional[int] = None

    @field_validator("xp")
    @classmethod
    def xp_valid(cls, v):
        if v is not None and v < 0:
            raise ValueError("XP tidak boleh negatif")
        return v


class AdminStats(BaseModel):
    """Statistik untuk dashboard admin."""
    total_users: int
    total_lessons: int
    total_challenges: int
    total_posts: int
    total_xp_diberikan: int
    user_aktif_7_hari: int

# ════════════════════════════════════════
# CHALLENGE FEEDBACK (Step 1)
# ════════════════════════════════════════

class ChallengeSelesaiResponse(BaseModel):
    """Response lengkap setelah user menyelesaikan challenge."""
    pesan: str
    xp_diperoleh: int
    xp_total: int
    streak_baru: int
    level_sekarang: int
    level_berikutnya: int
    xp_untuk_level_ini: int      # XP awal level sekarang
    xp_untuk_naik_level: int     # XP yang dibutuhkan untuk naik ke level berikutnya
    progress_persen: float        # 0.0 – 100.0
    naik_level: bool              # True jika baru saja naik level
    sudah_selesai_sebelumnya: bool = False