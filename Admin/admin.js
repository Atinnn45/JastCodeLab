/**
 * JastCodeLab — admin.js
 * Helper bersama untuk semua halaman admin.
 * Muat file ini di setiap halaman admin.
 */

const ADMIN_BASE      = "https://jastcodelab-production.up.railway.app";
const ADMIN_TOKEN_KEY = "jcl_token";
const ADMIN_SB_KEY    = "jcl_admin_sb";

// ════════════════════════════════════════
// AUTH CHECK
// ════════════════════════════════════════

function getAdminToken() {
  return localStorage.getItem(ADMIN_TOKEN_KEY);
}

function getAdminPayload() {
  const token = getAdminToken();
  if (!token) return null;
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;
    // FIX: padding Base64 yang benar
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded  = base64 + "=".repeat((4 - base64.length % 4) % 4);
    return JSON.parse(atob(padded));
  } catch {
    return null;
  }
}

function getAdminName() {
  return getAdminPayload()?.username || "Admin";
}

function requireAdmin() {
  const payload = getAdminPayload();
  if (!payload) {
    alert("Silakan login terlebih dahulu.");
    window.location.href = "/login.html";
    return;
  }
  if (!payload.is_admin) {
    alert("Akses ditolak. Akun ini bukan admin.");
    window.location.href = "/login.html";
  }
}

function adminLogout() {
  if (confirm("Yakin ingin keluar dari panel admin?")) {
    localStorage.removeItem(ADMIN_TOKEN_KEY);
    window.location.href = "/login.html";
  }
}

// ════════════════════════════════════════
// API FETCH
// ════════════════════════════════════════

async function adminFetch(endpoint, method = "GET", body = null) {
  const token = getAdminToken();

  // FIX: jika tidak ada token, langsung lempar error yang jelas
  if (!token) {
    throw new Error("Token tidak ditemukan. Silakan login ulang.");
  }

  const headers = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  };

  const opts = { method, headers };
  if (body !== null) opts.body = JSON.stringify(body);

  try {
    const res = await fetch(`${ADMIN_BASE}${endpoint}`, opts);

    // FIX: parse JSON terlebih dahulu sebelum cek status
    let data = null;
    const ct = res.headers.get("Content-Type") || "";
    if (ct.includes("application/json")) {
      data = await res.json();
    }

    // FIX: tangani 401 khusus — arahkan ke login
    if (res.status === 401) {
      localStorage.removeItem(ADMIN_TOKEN_KEY);
      alert("Sesi habis. Silakan login ulang.");
      window.location.href = "/login.html";
      throw new Error("Sesi habis");
    }

    if (!res.ok) {
      throw new Error(data?.detail || data?.message || `Error ${res.status}: ${res.statusText}`);
    }

    return data;

  } catch (err) {
    // FIX: bedakan error jaringan vs error dari server
    if (err instanceof TypeError && err.message.toLowerCase().includes("fetch")) {
      throw new Error("Tidak bisa terhubung ke server. Pastikan backend berjalan di " + ADMIN_BASE);
    }
    throw err;
  }
}


// ════════════════════════════════════════
// SIDEBAR TOGGLE
// ════════════════════════════════════════

// FIX: baca state sidebar dari localStorage agar persisten
let _sidebarOpen = localStorage.getItem(ADMIN_SB_KEY) !== "0";

function toggleSidebar() {
  _sidebarOpen = !_sidebarOpen;
  localStorage.setItem(ADMIN_SB_KEY, _sidebarOpen ? "1" : "0");
  applySidebar();
}

function applySidebar() {
  const sb  = document.getElementById("adminSidebar");
  const ma  = document.querySelector(".admin-main");
  if (!sb || !ma) return;

  const mob = window.innerWidth <= 768;

  if (_sidebarOpen) {
    // Buka sidebar
    sb.classList.remove("hidden");
    if (mob) {
      sb.classList.add("show");
      ma.classList.add("full");
    } else {
      sb.classList.remove("show"); // tidak butuh class show di desktop
      ma.classList.remove("full");
      ma.style.marginLeft = "220px";
    }
  } else {
    // Tutup sidebar
    sb.classList.remove("show");
    sb.classList.add("hidden");
    ma.classList.add("full");
    if (!mob) ma.style.marginLeft = "0";
  }
}

// FIX: update sidebar saat resize window
window.addEventListener("resize", () => {
  applySidebar();
});

// FIX: tutup sidebar mobile jika klik di luar
document.addEventListener("click", (e) => {
  if (window.innerWidth > 768) return;
  const sb = document.getElementById("adminSidebar");
  if (!sb) return;
  // Klik di luar sidebar saat mobile → tutup
  if (_sidebarOpen && !sb.contains(e.target)) {
    const toggle = document.querySelector(".topbar-toggle");
    if (toggle && toggle.contains(e.target)) return; // biarkan toggle handle
    _sidebarOpen = false;
    localStorage.setItem(ADMIN_SB_KEY, "0");
    applySidebar();
  }
}, true);


// ════════════════════════════════════════
// TOAST
// ════════════════════════════════════════

function tampilToast(pesan, tipe = "info", durasi = 3500) {
  let c = document.getElementById("toastContainer");

  // Buat container jika belum ada
  if (!c) {
    c = document.createElement("div");
    c.id = "toastContainer";
    c.style.cssText =
      "position:fixed;bottom:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:8px;";
    document.body.appendChild(c);
  }

  const el = document.createElement("div");
  const warna =
    tipe === "success" ? "#34d399" :
    tipe === "error"   ? "#f87171" :
    tipe === "warning" ? "#fb923c" :
    "#4f8ef7";

  el.style.cssText = `
    background: #111827;
    border: 1px solid ${warna}33;
    border-left: 3px solid ${warna};
    color: ${warna};
    padding: 12px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    max-width: 320px;
    box-shadow: 0 4px 16px rgba(0,0,0,.4);
    animation: fadeInRight .2s ease;
    pointer-events: none;
  `;
  el.textContent = pesan;
  c.appendChild(el);

  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transition = "opacity .3s";
    setTimeout(() => el.remove(), 300);
  }, durasi);
}


// ════════════════════════════════════════
// MODAL HELPERS
// ════════════════════════════════════════

function bukaModal(id) {
  const el = document.getElementById(id);
  if (el) {
    el.classList.add("show");
    // FIX: fokus ke input pertama di modal jika ada
    setTimeout(() => {
      const firstInput = el.querySelector("input:not([type=hidden]), textarea, select");
      if (firstInput) firstInput.focus();
    }, 50);
  }
}

function tutupModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove("show");
}

// Tutup modal jika klik overlay (bukan konten modal)
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("modal-overlay")) {
    e.target.classList.remove("show");
  }
});

// Tutup modal dengan tombol Escape
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    document.querySelectorAll(".modal-overlay.show")
      .forEach(m => m.classList.remove("show"));
  }
});


// ════════════════════════════════════════
// PAGINATION
// ════════════════════════════════════════

/**
 * Render tombol pagination.
 * FIX: tidak pakai .toString() — pakai nama fungsi sebagai string
 *
 * @param {string}   containerId   - id elemen container pagination
 * @param {number}   halaman       - halaman aktif saat ini
 * @param {number}   total         - total item
 * @param {number}   perHalaman    - item per halaman
 * @param {string}   namaFungsi    - nama fungsi yang dipanggil saat pindah halaman
 *                                   contoh: "muatUsers"
 */
function renderPagination(containerId, halaman, total, perHalaman, namaFungsi) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const totalHalaman = Math.ceil(total / perHalaman);

  // Sembunyikan jika hanya 1 halaman
  if (totalHalaman <= 1) {
    container.innerHTML = "";
    return;
  }

  let html = `
    <div class="pagination">
      <button class="page-btn" ${halaman === 1 ? "disabled" : ""}
        onclick="${namaFungsi}(${halaman - 1})">← Prev</button>
  `;

  for (let i = 1; i <= totalHalaman; i++) {
    const isAktif    = i === halaman;
    const isTepi     = i === 1 || i === totalHalaman;
    const isDekat    = Math.abs(i - halaman) <= 1;
    const isEllipsis = Math.abs(i - halaman) === 2;

    if (isAktif || isTepi || isDekat) {
      html += `<button class="page-btn ${isAktif ? "active" : ""}"
        onclick="${namaFungsi}(${i})">${i}</button>`;
    } else if (isEllipsis) {
      html += `<span style="color:var(--txt3);padding:0 4px;line-height:32px;">…</span>`;
    }
  }

  html += `
      <button class="page-btn" ${halaman === totalHalaman ? "disabled" : ""}
        onclick="${namaFungsi}(${halaman + 1})">Next →</button>
    </div>
  `;

  container.innerHTML = html;
}


// ════════════════════════════════════════
// HELPER UMUM
// ════════════════════════════════════════

function escHtml(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatTanggal(iso) {
  if (!iso) return "-";
  try {
    return new Date(iso.replace(" ", "T")).toLocaleDateString("id-ID", {
      day: "numeric", month: "short", year: "numeric",
    });
  } catch {
    return iso;
  }
}

/**
 * Debounce — delay eksekusi fungsi setelah user berhenti mengetik.
 * Dipakai untuk search input agar tidak terlalu banyak request.
 *
 * @param {Function} fn
 * @param {number}   delay - millisecond
 */
function debounce(fn, delay = 400) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// ── Inject animasi CSS yang dibutuhkan ──
(function () {
  const s = document.createElement("style");
  s.textContent = `
    @keyframes fadeInRight {
      from { opacity: 0; transform: translateX(12px); }
      to   { opacity: 1; transform: translateX(0); }
    }
  `;
  document.head.appendChild(s);
})();
