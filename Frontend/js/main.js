/**
 * JastCodeLab — main.js
 * =====================
 * Script utama yang dijalankan di setiap halaman.
 * Berisi:
 *  - Inisialisasi otomatis per halaman
 *  - Integrasi code runner (runner.html)
 *  - Integrasi profil (profile.html)
 *  - Integrasi leaderboard
 *  - Helper UI bersama
 *
 * Bergantung pada: api.js dan auth.js — muat keduanya lebih dulu.
 *
 * CATATAN: learn.html memiliki script sendiri yang lebih lengkap.
 *          main.js TIDAK mendefinisikan ulang fungsi lesson agar tidak konflik.
 */

// ─────────────────────────────────────────────
// JALANKAN SAAT DOM SIAP
// ─────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  const halaman = getNamaHalaman();

  // Isi navbar dengan data user di semua halaman
  isiNavbarUser();

  // Tampilkan / sembunyikan tombol login & logout di navbar
  aturNavbarLoginLogout();

  // Jalankan fungsi khusus sesuai halaman
  switch (halaman) {
    case "index.html":
    case "":
      initBeranda();
      break;

    case "login.html":
      initLogin();
      break;

    case "register.html":
      initRegister();
      break;

    case "learn.html":
      // learn.html punya script inline sendiri yang lengkap.
      // main.js tidak perlu melakukan apa-apa di sini agar tidak konflik.
      break;

    case "runner.html":
      initRunner();
      break;

    case "profile.html":
      initProfil();
      break;

    case "community.html":
      // community.html punya script sendiri
      break;

    case "challenges.html":
      // challenges.html punya script sendiri
      break;
  }
});


// ─────────────────────────────────────────────
// HELPER — nama halaman saat ini
// ─────────────────────────────────────────────

function getNamaHalaman() {
  return window.location.pathname.split("/").pop() || "index.html";
}


// ─────────────────────────────────────────────
// NAVBAR — isi data user
// ─────────────────────────────────────────────

function isiNavbarUser() {
  const user = getUser();
  if (!user) return;

  const elUsername = document.getElementById("navUsername");
  const elStreak   = document.getElementById("navStreak");
  const elXP       = document.getElementById("navXP");
  const elAvatar   = document.getElementById("navAvatar");

  if (elUsername) elUsername.textContent = user.username;
  if (elStreak)   elStreak.textContent   = `${user.streak_days ?? 0} Hari`;
  if (elXP)       elXP.textContent       = `⚡ ${user.xp ?? 0} XP`;
  if (elAvatar)   elAvatar.textContent   = user.username.charAt(0).toUpperCase();
}


// ─────────────────────────────────────────────
// NAVBAR — login/logout toggle
// ─────────────────────────────────────────────

function aturNavbarLoginLogout() {
  const elLoginLi  = document.getElementById("navLoginLi");
  const elLogoutBtn = document.getElementById("navLogoutBtn");
  const elProfilLi = document.getElementById("navProfilLi");

  const loginStatus = sudahLogin();

  if (elLoginLi)   elLoginLi.style.display  = loginStatus ? "none" : "";
  if (elLogoutBtn) elLogoutBtn.style.display = loginStatus ? ""     : "none";
  if (elProfilLi)  elProfilLi.style.display  = loginStatus ? ""     : "none";

  // Pasang event handler logout
  if (elLogoutBtn && !elLogoutBtn._logoutBound) {
    elLogoutBtn.addEventListener("click", logout);
    elLogoutBtn._logoutBound = true;
  }
}


// ─────────────────────────────────────────────
// HALAMAN: BERANDA (index.html)
// ─────────────────────────────────────────────

async function initBeranda() {
  if (sudahLogin()) {
    try {
      const profil = await getProfile();
      if (profil) {
        isiNavbarUser();

        const elXPSambutan    = document.getElementById("xpSambutan");
        const elStreakSambutan = document.getElementById("streakSambutan");
        if (elXPSambutan)     elXPSambutan.textContent     = profil.xp;
        if (elStreakSambutan) elStreakSambutan.textContent  = profil.streak_days;
      }
    } catch (_) { /* tidak wajib */ }
  }

  const elLB = document.getElementById("leaderboardRingkas");
  if (elLB) {
    await muatLeaderboard("leaderboardRingkas", 5);
  }
}


// ─────────────────────────────────────────────
// HALAMAN: LOGIN (login.html)
// ─────────────────────────────────────────────

function initLogin() {
  redirectJikaSudahLogin();

  const form = document.getElementById("loginForm");
  if (form) {
    form.addEventListener("submit", handleLogin);
  }
}


// ─────────────────────────────────────────────
// HALAMAN: REGISTER (register.html)
// ─────────────────────────────────────────────

function initRegister() {
  redirectJikaSudahLogin();

  const form = document.getElementById("registerForm");
  if (form) {
    form.addEventListener("submit", handleRegister);
  }
}


// ─────────────────────────────────────────────
// HALAMAN: CODE RUNNER (runner.html)
// ─────────────────────────────────────────────

function initRunner() {
  const tombolJalankan  = document.getElementById("tombolJalankan");
  const tombolBersihkan = document.getElementById("tombolBersihkan");
  const editorKode      = document.getElementById("editorKode");

  if (tombolJalankan) {
    tombolJalankan.addEventListener("click", jalankanKode);
  }
  if (tombolBersihkan) {
    tombolBersihkan.addEventListener("click", bersihkanOutput);
  }

  if (editorKode) {
    editorKode.addEventListener("keydown", (e) => {
      // Ctrl + Enter → jalankan kode
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        jalankanKode();
      }
      // Tab → 4 spasi
      if (e.key === "Tab") {
        e.preventDefault();
        const mulai = editorKode.selectionStart;
        const akhir = editorKode.selectionEnd;
        editorKode.value =
          editorKode.value.substring(0, mulai) + "    " + editorKode.value.substring(akhir);
        editorKode.selectionStart = editorKode.selectionEnd = mulai + 4;
      }
    });
  }
}

async function jalankanKode() {
  const editorKode      = document.getElementById("editorKode");
  const elOutput        = document.getElementById("outputKode");
  const tombolJalankan  = document.getElementById("tombolJalankan");
  const elStatus        = document.getElementById("statusRunner");

  if (!editorKode || !elOutput) return;

  const kode = editorKode.value.trim();
  if (!kode) {
    tampilToast("Tulis kode Python terlebih dahulu.", "info");
    return;
  }

  if (tombolJalankan) {
    tombolJalankan.disabled    = true;
    tombolJalankan.textContent = "⏳ Menjalankan...";
  }
  if (elStatus) elStatus.textContent = "Menjalankan...";
  elOutput.textContent = "";
  elOutput.className   = "output-area memuat";

  try {
    const hasil = await ApiRunner.jalankan(kode);

    if (hasil.error) {
      elOutput.textContent = hasil.error;
      elOutput.className   = "output-area error";
      if (elStatus) elStatus.textContent = "⚠ Error";
    } else {
      elOutput.textContent = hasil.output || "(tidak ada output)";
      elOutput.className   = "output-area sukses";
      if (elStatus) {
        const detik = hasil.waktu_eksekusi ? ` · ${hasil.waktu_eksekusi}s` : "";
        elStatus.textContent = `✓ Selesai${detik}`;
      }
    }
  } catch (err) {
    elOutput.textContent = `Gagal terhubung ke backend:\n${err.message}`;
    elOutput.className   = "output-area error";
    if (elStatus) elStatus.textContent = "✕ Gagal";
  }

  if (tombolJalankan) {
    tombolJalankan.disabled    = false;
    tombolJalankan.textContent = "▶ Jalankan";
  }
}

function bersihkanOutput() {
  const elOutput = document.getElementById("outputKode");
  const elStatus = document.getElementById("statusRunner");
  if (elOutput) { elOutput.textContent = ""; elOutput.className = "output-area"; }
  if (elStatus) elStatus.textContent = "Siap";
}


// ─────────────────────────────────────────────
// HALAMAN: PROFIL (profile.html)
// ─────────────────────────────────────────────

async function initProfil() {
  requireLogin();

  const elNama      = document.getElementById("profilNama");
  const elXP        = document.getElementById("profilXP");
  const elStreak    = document.getElementById("profilStreak");
  const elEmail     = document.getElementById("profilEmail");
  const elBergabung = document.getElementById("profilBergabung");

  // Tampilkan cache dulu
  const userCache = getUser();
  if (userCache && elNama)   elNama.textContent   = userCache.username;
  if (userCache && elXP)     elXP.textContent     = `${userCache.xp} XP`;
  if (userCache && elStreak) elStreak.textContent = `🔥 ${userCache.streak_days} Hari`;

  // Muat data terbaru
  try {
    const profil = await getProfile();
    if (!profil) return;

    if (elNama)      elNama.textContent      = profil.username;
    if (elXP)        elXP.textContent        = `${profil.xp} XP`;
    if (elStreak)    elStreak.textContent    = `🔥 ${profil.streak_days} Hari Streak`;
    if (elEmail)     elEmail.textContent     = profil.email || "-";
    if (elBergabung) elBergabung.textContent = formatTanggal(profil.created_at);

    const elJmlLesson    = document.getElementById("jumlahPelajaran");
    const elJmlChallenge = document.getElementById("jumlahTantangan");
    const elJmlPost      = document.getElementById("jumlahPost");

    if (elJmlLesson)    elJmlLesson.textContent    = profil.jumlah_pelajaran_selesai ?? "-";
    if (elJmlChallenge) elJmlChallenge.textContent = profil.jumlah_tantangan_selesai ?? "-";
    if (elJmlPost)      elJmlPost.textContent      = profil.jumlah_post ?? "-";

    isiNavbarUser();
  } catch (err) {
    tampilToast("Gagal memuat profil: " + err.message, "error");
  }

  await muatLeaderboard("leaderboardProfil", 10);
}


// ─────────────────────────────────────────────
// LEADERBOARD
// ─────────────────────────────────────────────

async function muatLeaderboard(elId, batasItem = 10) {
  const container = document.getElementById(elId);
  if (!container) return;

  container.innerHTML = `<p style="color:var(--txt3);font-size:13px;">Memuat leaderboard...</p>`;

  try {
    const data = await ApiUser.getLeaderboard();
    const list = data.slice(0, batasItem);
    const userSaatIni = getUser();

    container.innerHTML = list.map((item) => {
      const ikon  = item.rank === 1 ? "🥇" : item.rank === 2 ? "🥈" : item.rank === 3 ? "🥉" : `#${item.rank}`;
      const aktif = userSaatIni && item.username === userSaatIni.username ? " lb-saya" : "";
      return `
        <div class="lb-item${aktif}">
          <span class="lb-rank">${ikon}</span>
          <span class="lb-username">${escHtml(item.username)}</span>
          <span class="lb-xp">${item.xp} XP</span>
          <span class="lb-streak">🔥 ${item.streak_days}</span>
        </div>
      `;
    }).join("") || `<p style="color:var(--txt3);">Belum ada data.</p>`;

  } catch (err) {
    container.innerHTML = `<p style="color:var(--red);font-size:13px;">Gagal memuat leaderboard.</p>`;
  }
}


// ─────────────────────────────────────────────
// HELPER UI BERSAMA
// ─────────────────────────────────────────────

function tampilToast(pesan, tipe = "info", durasi = 3500) {
  let container = document.getElementById("toastContainer");
  if (!container) {
    container = document.createElement("div");
    container.id = "toastContainer";
    container.style.cssText =
      "position:fixed;bottom:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:8px;";
    document.body.appendChild(container);
  }

  const el = document.createElement("div");
  const warna = tipe === "success" ? "#34d399" : tipe === "error" ? "#f87171" : "#4f8ef7";
  el.style.cssText = `
    background:#111827; border:1px solid ${warna}33; border-left:3px solid ${warna};
    color:${warna}; padding:12px 18px; border-radius:8px;
    font-size:13px; font-weight:500; max-width:320px;
    box-shadow:0 4px 16px rgba(0,0,0,.4);
    animation:fadeIn .2s ease;
  `;
  el.textContent = pesan;
  container.appendChild(el);

  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transition = "opacity .3s";
    setTimeout(() => el.remove(), 300);
  }, durasi);
}

function escHtml(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatTanggal(iso) {
  if (!iso) return "-";
  try {
    return new Date(iso.replace(" ", "T")).toLocaleDateString("id-ID", {
      day: "numeric", month: "long", year: "numeric",
    });
  } catch {
    return iso;
  }
}

function salinKode(btn) {
  const blok = btn.closest(".blok-kode");
  const kode = blok?.querySelector("pre")?.textContent || "";
  navigator.clipboard.writeText(kode).then(() => {
    btn.textContent = "✓ Disalin!";
    btn.style.color = "#34d399";
    setTimeout(() => {
      btn.textContent = "Salin";
      btn.style.color = "";
    }, 2000);
  });
}

// Animasi fadeIn toast
(function () {
  const style = document.createElement("style");
  style.textContent = `@keyframes fadeIn { from { opacity:0; transform:translateX(12px); } to { opacity:1; transform:translateX(0); } }`;
  document.head.appendChild(style);
})();
