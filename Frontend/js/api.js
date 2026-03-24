/**
 * JastCodeLab — api.js
 * =====================
 * API client terpusat untuk semua request ke backend FastAPI.
 * Semua fungsi mengembalikan data langsung atau melempar Error.
 */

// ─────────────────────────────────────────────
// KONFIGURASI
// ─────────────────────────────────────────────

const BASE_URL = "https://jastcodelab-production.up.railway.app";


// ─────────────────────────────────────────────
// HELPER UTAMA — semua request lewat sini
// ─────────────────────────────────────────────

/**
 * Kirim HTTP request ke backend.
 *
 * @param {string} endpoint   - path, contoh: "/login"
 * @param {string} method     - "GET" | "POST" | "PUT" | "DELETE"
 * @param {object|null} body  - data yang dikirim (otomatis di-JSON-kan)
 * @param {boolean} withAuth  - apakah perlu sertakan Bearer token?
 * @returns {Promise<any>}    - data JSON dari response
 * @throws {Error}            - pesan error dari backend atau jaringan
 */
async function apiFetch(endpoint, method = "GET", body = null, withAuth = false) {
  const headers = { "Content-Type": "application/json" };

  if (withAuth) {
    const token = localStorage.getItem("jcl_token");
    if (!token) {
      throw new Error("Kamu belum login. Silakan login terlebih dahulu.");
    }
    headers["Authorization"] = `Bearer ${token}`;
  }

  const options = { method, headers };
  if (body !== null) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, options);

    let data = null;
    const contentType = response.headers.get("Content-Type") || "";
    if (contentType.includes("application/json")) {
      data = await response.json();
    }

    if (!response.ok) {
      const pesanError =
        data?.detail ||
        data?.message ||
        `Error ${response.status}: ${response.statusText}`;
      throw new Error(pesanError);
    }

    return data;

  } catch (err) {
    if (err instanceof TypeError && err.message.includes("fetch")) {
      throw new Error(
        "Tidak bisa terhubung ke server."
      );
    }
    throw err;
  }
}

/**
 * Kirim request dengan token jika ada, tanpa token jika tidak.
 * Dipakai untuk endpoint yang bersifat opsional auth
 * (guest bisa akses, tapi user login dapat data lebih lengkap).
 *
 * @param {string} endpoint
 * @param {string} method
 * @param {object|null} body
 * @returns {Promise<any>}
 */
async function apiFetchOptionalAuth(endpoint, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };

  // Sertakan token JIKA ada — backend akan tahu user login
  const token = localStorage.getItem("jcl_token");
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const options = { method, headers };
  if (body !== null) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, options);

    let data = null;
    const contentType = response.headers.get("Content-Type") || "";
    if (contentType.includes("application/json")) {
      data = await response.json();
    }

    if (!response.ok) {
      const pesanError =
        data?.detail ||
        data?.message ||
        `Error ${response.status}: ${response.statusText}`;
      throw new Error(pesanError);
    }

    return data;

  } catch (err) {
    if (err instanceof TypeError && err.message.includes("fetch")) {
      throw new Error(
        "Tidak bisa terhubung ke server."
      );
    }
    throw err;
  }
}


// ─────────────────────────────────────────────
// MODUL AUTH — Register & Login
// ─────────────────────────────────────────────

const ApiAuth = {
  /**
   * Daftarkan user baru.
   * POST /register
   */
  async register(username, email, password) {
    return apiFetch("/register", "POST", { username, email, password });
  },

  /**
   * Login user yang sudah ada.
   * POST /login
   */
  async login(username, password) {
    return apiFetch("/login", "POST", { username, password });
  },
};


// ─────────────────────────────────────────────
// MODUL USER — Profil & Leaderboard
// ─────────────────────────────────────────────

const ApiUser = {
  /**
   * Ambil data profil user yang sedang login.
   * GET /profil  (butuh token)
   */
  async getProfil() {
    return apiFetch("/profil", "GET", null, true);
  },

  /**
   * Ambil papan peringkat 10 user teratas.
   * GET /leaderboard
   */
  async getLeaderboard() {
    return apiFetch("/leaderboard", "GET", null, false);
  },
};


// ─────────────────────────────────────────────
// MODUL PELAJARAN — Lessons
// ─────────────────────────────────────────────

const ApiLesson = {
  /**
   * Ambil daftar semua pelajaran.
   * GET /lessons
   *
   * PENTING: Menggunakan apiFetchOptionalAuth agar backend tahu
   * apakah user sudah login atau belum.
   * - Guest  → hanya lesson pertama terbuka
   * - Login  → semua lesson terbuka
   */
  async getDaftar() {
    return apiFetchOptionalAuth("/lessons", "GET", null);
  },

  /**
   * Ambil detail satu pelajaran.
   * GET /lesson/{id}
   *
   * Juga menggunakan optional auth agar akses lesson
   * disesuaikan dengan status login.
   */
  async getDetail(lessonId) {
    return apiFetchOptionalAuth(`/lesson/${lessonId}`, "GET", null);
  },

  /**
   * Tandai pelajaran sebagai selesai dan dapatkan XP.
   * POST /lesson/{id}/selesai  (butuh token)
   */
  async tandaiSelesai(lessonId) {
    return apiFetch(`/lesson/${lessonId}/selesai`, "POST", null, true);
  },
};


// ─────────────────────────────────────────────
// MODUL TANTANGAN — Challenges
// ─────────────────────────────────────────────

const ApiChallenge = {
  /**
   * Ambil daftar semua tantangan.
   * GET /challenges
   */
  async getDaftar() {
    return apiFetchOptionalAuth("/challenges", "GET", null);
  },

  /**
   * Ambil detail satu tantangan.
   * GET /challenge/{id}
   */
  async getDetail(challengeId) {
    return apiFetchOptionalAuth(`/challenge/${challengeId}`, "GET", null);
  },

  /**
   * Tandai tantangan sebagai selesai.
   * POST /challenge/{id}/selesai  (butuh token)
   */
  async tandaiSelesai(challengeId) {
    return apiFetch(`/challenge/${challengeId}/selesai`, "POST", null, true);
  },
};


// ─────────────────────────────────────────────
// MODUL CODE RUNNER
// ─────────────────────────────────────────────

const ApiRunner = {
  /**
   * Jalankan kode Python di backend.
   * POST /run-code
   */
  async jalankan(kode) {
    return apiFetch("/run-code", "POST", { kode });
  },
};


// ─────────────────────────────────────────────
// MODUL KOMUNITAS — Posts
// ─────────────────────────────────────────────

const ApiPost = {
  /**
   * Ambil daftar post komunitas.
   * GET /posts
   */
  async getDaftar(halaman = 1, perHalaman = 10) {
    return apiFetchOptionalAuth(`/posts?halaman=${halaman}&per_halaman=${perHalaman}`, "GET", null);
  },

  /**
   * Ambil detail satu post beserta komentar.
   * GET /posts/{id}
   */
  async getDetail(postId) {
    return apiFetchOptionalAuth(`/posts/${postId}`, "GET", null);
  },

  /**
   * Buat post baru (butuh login).
   * POST /posts
   */
  async buat(judul, konten, kodeSnippet = "", outputPreview = "") {
    return apiFetch("/posts", "POST", {
      judul,
      konten,
      kode_snippet: kodeSnippet,
      output_preview: outputPreview,
    }, true);
  },

  /**
   * Toggle like pada post (butuh login).
   * POST /posts/{id}/like
   */
  async toggleLike(postId) {
    return apiFetch(`/posts/${postId}/like`, "POST", null, true);
  },

  /**
   * Tambah komentar pada post (butuh login).
   * POST /posts/{id}/komentar
   */
  async tambahKomentar(postId, isi) {
    return apiFetch(`/posts/${postId}/komentar`, "POST", { isi }, true);
  },
};