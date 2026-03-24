/**
 * JastCodeLab — shared.js
 * Sidebar, streak, toast, helpers
 * Dimuat setelah api.js dan auth.js
 */

// ─── SIDEBAR ───────────────────────────────
const _SB_KEY = "jcl_sb";
let _sbOpen = true;

function toggleSidebar() {
  _sbOpen = !_sbOpen;
  _applySb();
  localStorage.setItem(_SB_KEY, _sbOpen ? "1" : "0");
}
function tutupSidebar() {
  _sbOpen = false;
  _applySb();
}
function _applySb() {
  const sb = document.getElementById("sidebar");
  const ma = document.getElementById("mainArea");
  const ov = document.getElementById("sbOverlay");
  if (!sb) return;
  const mob = window.innerWidth <= 768;
  if (_sbOpen) {
    sb.classList.remove("sb-hidden");
    sb.classList.add("sb-show");
    if (mob) { if (ov) ov.classList.add("ov-show"); if (ma) ma.style.marginLeft = "0"; }
    else { if (ov) ov.classList.remove("ov-show"); if (ma) ma.style.marginLeft = "220px"; }
  } else {
    sb.classList.add("sb-hidden");
    sb.classList.remove("sb-show");
    if (ov) ov.classList.remove("ov-show");
    if (ma) ma.style.marginLeft = "0";
  }
}
function _initSb() {
  const saved = localStorage.getItem(_SB_KEY);
  _sbOpen = window.innerWidth <= 768 ? false : (saved === null ? true : saved === "1");
  _applySb();
  window.addEventListener("resize", () => {
    if (window.innerWidth > 768 && document.getElementById("sbOverlay")) {
      document.getElementById("sbOverlay").classList.remove("ov-show");
    }
    _applySb();
  });
}

// ─── STREAK (muncul hanya jika > 0) ────────
function _updateStreak(days) {
  const wrap = document.getElementById("streakWrap");
  if (!wrap) return;
  if (!days || days <= 0) { wrap.style.display = "none"; return; }
  wrap.style.display = "flex";
  const elDays = document.getElementById("sbStreakDays");
  const elLbl  = document.getElementById("sbStreakLbl");
  if (elDays) elDays.textContent = `${days} Hari`;
  if (elLbl) {
    if (days >= 30)      elLbl.textContent = "Streak Legenda! 🔥";
    else if (days >= 14) elLbl.textContent = "Streak 2 Minggu!";
    else if (days >= 7)  elLbl.textContent = "Streak Seminggu!";
    else if (days >= 3)  elLbl.textContent = "Streak Aktif";
    else                 elLbl.textContent = "Streak Aktif";
  }
  // Warna naik sesuai level
  if (days >= 7) {
    wrap.style.background = "rgba(251,191,36,0.1)";
    wrap.style.borderColor = "rgba(251,191,36,0.25)";
    if (elDays) elDays.style.color = "#fbbf24";
  }
}

// ─── NAVBAR USER ───────────────────────────
function updateNavUser() {
  const user = getUser();
  const ok   = sudahLogin();
  const liLogin  = document.getElementById("navLiLogin");
  const liProfil = document.getElementById("navLiProfil");
  const btnKlr   = document.getElementById("navBtnKeluar");
  const guestBnr = document.getElementById("guestBanner");
  if (liLogin)  liLogin.style.display  = ok ? "none" : "";
  if (liProfil) liProfil.style.display = ok ? ""     : "none";
  if (btnKlr)   btnKlr.style.display   = ok ? ""     : "none";
  if (guestBnr) guestBnr.style.display = ok ? "none" : "flex";
  if (user) {
    const ini = user.username.charAt(0).toUpperCase();
    const set = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
    set("navUsername", user.username);
    set("navAvatar", ini);
    set("navAvatarTop", ini);
    set("navXP", `⚡ ${user.xp} XP`);
    _updateStreak(user.streak_days || 0);
  } else {
    _updateStreak(0);
  }
}

// ─── TOAST ─────────────────────────────────
function tampilToast(msg, type = "info", ms = 3500) {
  let c = document.getElementById("toastContainer");
  if (!c) {
    c = document.createElement("div");
    c.id = "toastContainer";
    document.body.appendChild(c);
  }
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = (type === "success" ? "✓ " : type === "error" ? "✕ " : "ℹ ") + msg;
  c.appendChild(el);
  setTimeout(() => { el.style.opacity = "0"; el.style.transition = "opacity .3s"; setTimeout(() => el.remove(), 300); }, ms);
}

// ─── HELPERS ───────────────────────────────
function escHtml(s) {
  return String(s ?? "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}
function formatTgl(iso) {
  if (!iso) return "";
  try {
    const d = new Date(iso.replace(" ","T")), n = new Date(), s = Math.floor((n-d)/1000);
    if (s < 60) return "baru saja";
    if (s < 3600) return Math.floor(s/60) + " menit lalu";
    if (s < 86400) return Math.floor(s/3600) + " jam lalu";
    return Math.floor(s/86400) + " hari lalu";
  } catch { return iso; }
}
function warnaAvatar(str) {
  const p = ["linear-gradient(135deg,#6366f1,#8b5cf6)","linear-gradient(135deg,#10b981,#059669)","linear-gradient(135deg,#f59e0b,#d97706)","linear-gradient(135deg,#3b82f6,#2563eb)","linear-gradient(135deg,#ec4899,#db2777)","linear-gradient(135deg,#14b8a6,#0d9488)"];
  let h = 0; for (const c of str) h = (h*31 + c.charCodeAt(0)) % p.length;
  return p[h];
}

// ─── AUTO INIT ─────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  _initSb();
  updateNavUser();
  // Overlay click
  const ov = document.getElementById("sbOverlay");
  if (ov) ov.addEventListener("click", tutupSidebar);
  // Logout btn
  const btnKlr = document.getElementById("navBtnKeluar");
  if (btnKlr) btnKlr.addEventListener("click", logout);
  // Refresh profil background
  if (sudahLogin()) {
    ApiUser.getProfil().then(p => { updateUserStats(p.xp, p.streak_days); updateNavUser(); }).catch(()=>{});
  }
});