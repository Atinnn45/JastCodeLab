/**
 * JastCodeLab — auth.js
 * =====================
 * Menangani semua logika autentikasi:
 * - Register & login
 * - Simpan / ambil / hapus token dari localStorage
 * - Cek status login
 * - Redirect otomatis (admin → dashboard, user → beranda)
 *
 * File ini bergantung pada api.js — pastikan api.js dimuat lebih dulu.
 */

// ─────────────────────────────────────────────
// KUNCI localStorage
// ─────────────────────────────────────────────

const KEY_TOKEN    = "jcl_token";
const KEY_USER     = "jcl_user";      // objek user (id, username, xp, streak_days, is_admin)
const KEY_REDIRECT = "jcl_redirect";  // URL tujuan setelah login


// ─────────────────────────────────────────────
// SIMPAN & AMBIL DATA DARI localStorage
// ─────────────────────────────────────────────

/**
 * Simpan token dan data user setelah login/register berhasil.
 * FIX: tambah is_admin ke cache
 * @param {{ token, user_id, username, xp, streak_days, is_admin }} data
 */
function simpanSesiLogin(data) {
  localStorage.setItem(KEY_TOKEN, data.token);
  localStorage.setItem(KEY_USER, JSON.stringify({
    id:          data.user_id,
    username:    data.username,
    xp:          data.xp          ?? 0,
    streak_days: data.streak_days  ?? 0,
    is_admin:    data.is_admin     ?? false,  // ← FIX: simpan status admin
  }));
}

/**
 * Ambil token JWT dari localStorage.
 * @returns {string|null}
 */
function getToken() {
  return localStorage.getItem(KEY_TOKEN);
}

/**
 * Ambil data user yang tersimpan.
 * @returns {{ id, username, xp, streak_days, is_admin }|null}
 */
function getUser() {
  const raw = localStorage.getItem(KEY_USER);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

/**
 * Cek apakah user yang login adalah admin.
 * @returns {boolean}
 */
function isAdmin() {
  const user = getUser();
  return Boolean(user && user.is_admin);
}

/**
 * Update XP dan streak di cache lokal (tanpa perlu request ulang).
 * @param {number} xp
 * @param {number} streak
 */
function updateUserStats(xp, streak) {
  const user = getUser();
  if (!user) return;
  user.xp          = xp;
  user.streak_days = streak;
  localStorage.setItem(KEY_USER, JSON.stringify(user));
}

/**
 * Cek apakah user saat ini sudah login.
 * @returns {boolean}
 */
function sudahLogin() {
  return Boolean(getToken() && getUser());
}

/**
 * Hapus semua data sesi (logout).
 */
function hapusSesi() {
  localStorage.removeItem(KEY_TOKEN);
  localStorage.removeItem(KEY_USER);
}


// ─────────────────────────────────────────────
// HELPER — tentukan path relatif Admin/Frontend
// ─────────────────────────────────────────────

/**
 * Deteksi apakah halaman saat ini ada di folder Admin/ atau Frontend/.
 * Dipakai untuk menentukan path redirect yang benar.
 */
function _getBasePath() {
  const path = window.location.pathname;
  if (path.includes("/Admin/")) return "../Admin/";
  return "../Admin/"; // default dari Frontend ke Admin
}

/**
 * Redirect ke dashboard admin atau beranda user.
 * FIX: admin → Admin/dashboard.html, user biasa → index.html
 */
function _redirectSetelahLogin(data) {
  if (data.is_admin) {
    // Admin → arahkan ke Admin/dashboard.html
    // Dari Frontend/login.html, path relatifnya adalah ../Admin/dashboard.html
    window.location.href = "https://fantastic-axolotl-451a8f.netlify.app/dashboard.html";
  } else {
    // User biasa → arahkan ke beranda atau halaman sebelumnya
    const tujuan = sessionStorage.getItem(KEY_REDIRECT) || "index.html";
    sessionStorage.removeItem(KEY_REDIRECT);
    window.location.href = tujuan;
  }
}


// ─────────────────────────────────────────────
// REGISTER
// ─────────────────────────────────────────────

/**
 * Proses form register.
 * Dipanggil dari register.html saat form di-submit.
 * @param {Event} event - form submit event
 */
async function handleRegister(event) {
  event.preventDefault();

  const username   = document.getElementById("username").value.trim();
  const email      = document.getElementById("email").value.trim();
  const password   = document.getElementById("password").value;
  const konfirmasi = document.getElementById("konfirmasi")?.value || password;
  const btnEl      = document.getElementById("submitBtn");
  const alertEl    = document.getElementById("alertBox");

  // Reset pesan
  tampilkanAlert(alertEl, "", "");

  // Validasi sisi client
  if (!username || username.length < 3) {
    return tampilkanAlert(alertEl, "Username minimal 3 karakter.", "error");
  }
  if (!email || !email.includes("@")) {
    return tampilkanAlert(alertEl, "Format email tidak valid.", "error");
  }
  if (!password || password.length < 6) {
    return tampilkanAlert(alertEl, "Password minimal 6 karakter.", "error");
  }
  if (password !== konfirmasi) {
    return tampilkanAlert(alertEl, "Password dan konfirmasi tidak cocok.", "error");
  }

  // Kirim ke backend
  setButtonLoading(btnEl, true, "Mendaftar...");

  try {
    const data = await ApiAuth.register(username, email, password);

    // Simpan sesi & tampilkan sukses
    simpanSesiLogin(data);
    tampilkanAlert(alertEl, `🎉 Berhasil daftar! Selamat datang, ${data.username}!`, "success");

    // Register tidak bisa jadi admin langsung — selalu ke beranda
    setTimeout(() => {
      window.location.href = "index.html";
    }, 1000);

  } catch (err) {
    tampilkanAlert(alertEl, err.message, "error");
    setButtonLoading(btnEl, false, "Daftar Sekarang");
  }
}


// ─────────────────────────────────────────────
// LOGIN
// ─────────────────────────────────────────────

/**
 * Proses form login.
 * FIX: setelah login berhasil, cek is_admin:
 *   - Admin  → redirect ke Admin/dashboard.html
 *   - User   → redirect ke index.html (atau halaman sebelumnya)
 *
 * @param {Event} event - form submit event
 */
async function handleLogin(event) {
  event.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;
  const btnEl    = document.getElementById("submitBtn");
  const alertEl  = document.getElementById("alertBox");

  tampilkanAlert(alertEl, "", "");

  if (!username) {
    return tampilkanAlert(alertEl, "Username wajib diisi.", "error");
  }
  if (!password) {
    return tampilkanAlert(alertEl, "Password wajib diisi.", "error");
  }

  setButtonLoading(btnEl, true, "Masuk...");

  try {
    const data = await ApiAuth.login(username, password);

    // Simpan sesi (termasuk is_admin)
    simpanSesiLogin(data);

    // Pesan sambutan beda untuk admin dan user biasa
    const sambutan = data.is_admin
      ? `✓ Selamat datang Admin ${data.username}! Menuju Dashboard...`
      : `✓ Berhasil masuk! Halo, ${data.username}!`;
    tampilkanAlert(alertEl, sambutan, "success");

    // FIX: redirect berdasarkan role
    setTimeout(() => {
      _redirectSetelahLogin(data);
    }, 800);

  } catch (err) {
    tampilkanAlert(alertEl, err.message, "error");
    setButtonLoading(btnEl, false, "Masuk");
  }
}


// ─────────────────────────────────────────────
// LOGOUT
// ─────────────────────────────────────────────

/**
 * Logout user: hapus sesi dan redirect ke login.
 * Bisa dipanggil dari tombol logout di navbar/profil.
 */
function logout() {
  if (!confirm("Yakin ingin keluar dari JastCodeLab?")) return;
  hapusSesi();
  // Deteksi apakah sedang di folder Admin atau Frontend
  const path = window.location.pathname;
  if (path.includes("/Admin/")) {
    window.location.href = "../Frontend/login.html";
  } else {
    window.location.href = "login.html";
  }
}


// ─────────────────────────────────────────────
// GUARD HALAMAN (PROTEKSI ROUTE)
// ─────────────────────────────────────────────

/**
 * Paksa redirect ke login jika belum login.
 * Panggil di atas halaman yang butuh autentikasi.
 */
function requireLogin() {
  if (!sudahLogin()) {
    sessionStorage.setItem(KEY_REDIRECT, window.location.href);
    // Deteksi folder saat ini
    const path = window.location.pathname;
    if (path.includes("/Admin/")) {
      window.location.href = "../Frontend/login.html";
    } else {
      window.location.href = "login.html";
    }
  }
}

/**
 * Redirect ke beranda jika sudah login.
 * Panggil di login.html & register.html.
 * FIX: admin yang sudah login diarahkan ke dashboard, bukan index
 */
function redirectJikaSudahLogin() {
  if (sudahLogin()) {
    if (isAdmin()) {
      window.location.href = "../Admin/dashboard.html";
    } else {
      window.location.href = "index.html";
    }
  }
}


// ─────────────────────────────────────────────
// AMBIL PROFIL
// ─────────────────────────────────────────────

/**
 * Ambil data profil terbaru dari API, lalu perbarui cache lokal.
 * @returns {{ id, username, xp, streak_days, is_admin, ... }|null}
 */
async function getProfile() {
  if (!sudahLogin()) return null;

  try {
    const profil = await ApiUser.getProfil();

    // Perbarui cache lokal dengan data terbaru dari server
    updateUserStats(profil.xp, profil.streak_days);

    return profil;
  } catch (err) {
    // Jika token kedaluwarsa/tidak valid, logout otomatis
    if (err.message.includes("401") || err.message.toLowerCase().includes("login")) {
      hapusSesi();
      const path = window.location.pathname;
      window.location.href = path.includes("/Admin/")
        ? "../Frontend/login.html"
        : "login.html";
    }
    return null;
  }
}


// ─────────────────────────────────────────────
// UPDATE UI NAVBAR
// ─────────────────────────────────────────────

/**
 * Isi elemen navbar dengan data user yang sedang login.
 */
function isiNavbarUser() {
  const user = getUser();
  if (!user) return;

  const elUsername = document.getElementById("navUsername");
  const elXP       = document.getElementById("navXP");
  const elAvatar   = document.getElementById("navAvatar");
  const elStreak   = document.getElementById("navStreak");

  if (elUsername) elUsername.textContent = user.username;
  if (elXP)       elXP.textContent       = `⚡ ${user.xp} XP`;
  if (elStreak)   elStreak.textContent   = `🔥 ${user.streak_days} Hari`;
  if (elAvatar)   elAvatar.textContent   = user.username.charAt(0).toUpperCase();
}


// ─────────────────────────────────────────────
// HELPER UI
// ─────────────────────────────────────────────

/**
 * Tampilkan pesan alert di elemen yang ditentukan.
 */
function tampilkanAlert(el, pesan, tipe) {
  if (!el) return;
  el.textContent   = pesan;
  el.className     = `auth-alert${tipe ? " " + tipe : ""}`;
  el.style.display = pesan ? "block" : "none";
}

/**
 * Set tombol submit ke mode loading atau normal.
 */
function setButtonLoading(btn, loading, teksNormal) {
  if (!btn) return;
  btn.disabled    = loading;
  btn.textContent = loading ? "Memproses..." : teksNormal;
}
