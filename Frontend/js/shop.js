/**
 * JastCodeLab — Shop Page Logic
 * Load setelah: api.js, auth.js, shared.js, sidebar-patch.js
 */

// ════════════════════════════════════════
// GLOBAL STATE
// ════════════════════════════════════════
let shopData = null;
let tabAktif = "semua";
let activeTitle = null;

/* ── TABS ── */
function gantiTab(btn) {
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  tabAktif = btn.dataset.tab;
  renderShop();
}

/* ── RENDER GRID ── */
function renderShop() {
  const grid = document.getElementById("shopGrid");
  if (!grid || !shopData) {
    grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--txt3);">Memuat...</div>`;
    return;
  }

  let items = shopData.items;
  if (tabAktif === "koleksi") items = items.filter(i => i.sudah_dibeli);

  if (items.length === 0) {
    grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;">
      <div class="ikon">${tabAktif === "koleksi" ? "📦" : "🛒"}</div>
      <p>${tabAktif === "koleksi" ? "Kamu belum punya koleksi. Beli item dulu!" : "Tidak ada item tersedia."}</p>
    </div>`;
    return;
  }

  grid.innerHTML = items.map(item => {
    const isActive = item.nilai === activeTitle;
    const isOwned = item.sudah_dibeli;
    const bisaBeli = !isOwned && (shopData.coins_user >= item.harga_coins);
    let cardClass = "item-card";
    if (isActive) cardClass += " active-item";
    else if (isOwned) cardClass += " owned";

    let btnHtml = "";
    if (isActive) {
      btnHtml = `<button class="btn-lepas" onclick="lepasTitleAktif()">Lepas</button>`;
    } else if (isOwned) {
      btnHtml = `<button class="btn-pakai" onclick="pakaiItem(${item.id})">Pakai</button>
                 <span class="owned-badge">✓ Dimiliki</span>`;
    } else {
      btnHtml = `<button class="btn-beli" onclick="beliItem(${item.id},this)" ${bisaBeli ? "" : "disabled"}>
        🪙 ${item.harga_coins.toLocaleString()} Beli
      </button>`;
    }

    return `
      <div class="${cardClass}" id="card-${item.id}">
        <div class="item-ikon">${item.ikon}</div>
        <div class="item-nama">${escHtml(item.nama)}</div>
        <div class="item-desc">${escHtml(item.deskripsi)}</div>
        <div class="item-preview">${escHtml(item.nilai)}</div>
        <div class="item-footer">
          ${isOwned ? btnHtml : `<div class="item-price">🪙 <span>${item.harga_coins.toLocaleString()}</span></div>`}
          ${!isOwned ? btnHtml : ""}
        </div>
      </div>`;
  }).join("");
}

/* ── BELI ITEM ── */
async function beliItem(id, btn) {
  if (!sudahLogin()) {
    tampilToast("Login dulu untuk membeli item!", "info");
    setTimeout(() => window.location.href = "login.html", 1200);
    return;
  }

  btn.disabled = true;
  btn.innerHTML = "⏳ Membeli...";

  try {
    const token = localStorage.getItem("jcl_token");
    const res = await fetch(`${API}/shop/beli/${id}`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();

    if (!res.ok) {
      tampilToast(data.detail || "Gagal membeli", "error");
      btn.disabled = false;
      btn.innerHTML = `🪙 ${shopData.items.find(i=>i.id===id).harga_coins.toLocaleString()} Beli`;
      return;
    }

    tampilToast(`✅ ${data.pesan}`, "success");
    shopData.coins_user = data.coins_sisa;
    updateCoinsDisplay(data.coins_sisa);

    // Update cache
    const item = shopData.items.find(i => i.id === id);
    if (item) item.sudah_dibeli = true;
    renderShop();

  } catch (e) {
    tampilToast("Gagal terhubung ke server", "error");
  } finally {
    btn.disabled = false;
    if (!btn.innerHTML.includes("Beli")) {
      const item = shopData.items.find(i => i.id === id);
      btn.innerHTML = `🪙 ${item.harga_coins.toLocaleString()} Beli`;
    }
  }
}

/* ── PAKAI ITEM ── */
async function pakaiItem(id) {
  if (!sudahLogin()) return;

  try {
    const token = localStorage.getItem("jcl_token");
    const res = await fetch(`${API}/shop/pakai/${id}`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();

    if (!res.ok) {
      tampilToast(data.detail || "Gagal pakai item", "error");
      return;
    }

    activeTitle = data.nilai;
    tampilToast(`🎭 ${data.pesan}`, "success");
    renderShop();

  } catch (e) {
    tampilToast("Gagal terhubung ke server", "error");
  }
}

/* ── LEPAS TITLE ── */
async function lepasTitleAktif() {
  if (!sudahLogin()) return;

  try {
    const token = localStorage.getItem("jcl_token");
    const res = await fetch(`${API}/shop/lepas-title`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` }
    });
    const data = await res.json();

    if (!res.ok) {
      tampilToast(data.detail || "Gagal", "error");
      return;
    }

    activeTitle = null;
    tampilToast("Title dilepas", "info");
    renderShop();

  } catch (e) {
    tampilToast("Gagal terhubung ke server", "error");
  }
}

/* ── UPDATE COINS DISPLAY ── */
function updateCoinsDisplay(coins) {
  document.getElementById("navCoins").textContent = `🪙 ${coins.toLocaleString()}`;
  document.getElementById("heroCoins").textContent = coins.toLocaleString();
}

/* ── LOAD DATA ── */
async function muatShop() {
  const grid = document.getElementById("shopGrid");
  grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--txt3);">
    <div style="font-size:2rem;margin-bottom:12px;">⏳</div>
    <div>Memuat toko...</div>
  </div>`;

  try {
    const token = localStorage.getItem("jcl_token");
    const headers = token ? { "Authorization": `Bearer ${token}` } : {};
    const res = await fetch(`${API}/shop`, { headers });
    shopData = await res.json();

    updateCoinsDisplay(shopData.coins_user || 0);

    // Ambil active title
    if (sudahLogin()) {
      try {
        const kolRes = await fetch(`${API}/shop/koleksi`, {
          headers: { "Authorization": `Bearer ${token}` }
        });
        const kol = await kolRes.json();
        activeTitle = kol.active_title || null;
      } catch {}
    }

    renderShop();

  } catch (e) {
    grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:60px;color:var(--red);">
      <div style="font-size:2.5rem;margin-bottom:16px;">💥</div>
      <div style="font-size:18px;font-weight:700;margin-bottom:8px;">Gagal memuat toko</div>
      <div style="color:var(--txt2);font-size:14px;">Pastikan backend berjalan di http://127.0.0.1:8000</div>
    </div>`;
  }
}

/* ── ESC HTML ── */
function escHtml(s) {
  return String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "<").replace(/>/g, ">");
}

// ════════════════════════════════════════
// INIT — HARUS SETELAH shared.js
// ════════════════════════════════════════
document.addEventListener("DOMContentLoaded", async () => {
  requireLogin();
  await muatShop();
});

