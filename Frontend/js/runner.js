/**
 * JastCodeLab — runner.js (FIXED)
 * ================================
 * Semua logika Code Runner:
 * - Monaco Editor
 * - Jalankan kode via backend
 * - Sidebar & navbar
 * - Sample kode (7 contoh)
 * - Keyboard shortcut Ctrl+Enter
 */

// ════════════════════════════════════════
// SAMPLE KODE
// ════════════════════════════════════════

const SAMPLES = {
  hello: `# Hello World — JastCodeLab
print("Halo, Dunia!")
print("Selamat datang di Code Runner!")

nama = "JastCodeLab"
tahun = 2025
print(f"Halo dari {nama}, tahun {tahun}!")
`,

  variabel: `# Variabel dan Tipe Data di Python
nama    = "Budi Santoso"
umur    = 17
tinggi  = 165.5
aktif   = True

print("=== Data Siswa ===")
print(f"Nama   : {nama}")
print(f"Umur   : {umur} tahun")
print(f"Tinggi : {tinggi} cm")
print(f"Aktif  : {aktif}")
print(f"Tipe nama  : {type(nama)}")
print(f"Tipe umur  : {type(umur)}")
print(f"Tipe tinggi: {type(tinggi)}")
print(f"Tipe aktif : {type(aktif)}")
`,

  loop: `# Perulangan (for & while)

# For loop dengan range
print("Angka 1 sampai 5:")
for i in range(1, 6):
    print(f"  {i}")

# While loop
print("\\nHitung mundur:")
n = 5
while n > 0:
    print(f"  {n}...")
    n -= 1
print("  🚀 Mulai!")

# List comprehension
print("\\nKuadrat 1-5:")
kuadrat = [x**2 for x in range(1, 6)]
print(f"  {kuadrat}")

# Loop dengan enumerate
buah = ["apel", "mangga", "jeruk"]
print("\\nDaftar buah:")
for i, b in enumerate(buah, start=1):
    print(f"  {i}. {b}")
`,

  fungsi: `# Fungsi di Python

def hitung_luas(panjang, lebar):
    """Hitung luas persegi panjang."""
    return panjang * lebar

def sapa(nama, salam="Halo"):
    """Fungsi sapa dengan parameter default."""
    return f"{salam}, {nama}! 👋"

def faktorial(n):
    """Hitung faktorial secara rekursif."""
    if n <= 1:
        return 1
    return n * faktorial(n - 1)

# Fungsi lambda
kuadrat = lambda x: x ** 2
genap   = lambda x: x % 2 == 0

# Test semua fungsi
print(f"Luas 5x3     : {hitung_luas(5, 3)}")
print(f"Luas 10x7    : {hitung_luas(10, 7)}")
print(f"Sapa default : {sapa('Budi')}")
print(f"Sapa custom  : {sapa('Siti', 'Selamat pagi')}")
print(f"5! = {faktorial(5)}")
print(f"7! = {faktorial(7)}")
print(f"Kuadrat 9    : {kuadrat(9)}")
print(f"Apakah 8 genap? {genap(8)}")
`,

  kelas: `# OOP — Class dan Object di Python

class Mahasiswa:
    jumlah = 0  # class variable

    def __init__(self, nama, nim):
        self.nama  = nama
        self.nim   = nim
        self.nilai = []
        Mahasiswa.jumlah += 1

    def tambah_nilai(self, n):
        self.nilai.append(n)

    @property
    def ipk(self):
        if not self.nilai:
            return 0.0
        return round(sum(self.nilai) / len(self.nilai), 2)

    def __str__(self):
        return f"[{self.nim}] {self.nama} — IPK: {self.ipk}"


# Inheritance
class MahasiswaBerprestasi(Mahasiswa):
    def __init__(self, nama, nim, beasiswa):
        super().__init__(nama, nim)
        self.beasiswa = beasiswa

    def __str__(self):
        return super().__str__() + f" 🏆 ({self.beasiswa})"


# Buat objek
m1 = Mahasiswa("Budi Santoso", "2024001")
m1.tambah_nilai(85)
m1.tambah_nilai(90)
m1.tambah_nilai(88)

m2 = MahasiswaBerprestasi("Siti Rahayu", "2024002", "Beasiswa Penuh")
m2.tambah_nilai(95)
m2.tambah_nilai(98)
m2.tambah_nilai(97)

print("=== Data Mahasiswa ===")
print(m1)
print(m2)
print(f"Total terdaftar: {Mahasiswa.jumlah} mahasiswa")
`,

  list_dict: `# List, Tuple, Dictionary, dan Set

# ── LIST ──
nilai = [85, 92, 78, 95, 88, 70, 99]
print("=== LIST ===")
print(f"Semua nilai  : {nilai}")
print(f"Terbesar     : {max(nilai)}")
print(f"Terkecil     : {min(nilai)}")
print(f"Rata-rata    : {sum(nilai)/len(nilai):.1f}")
print(f"Diurutkan    : {sorted(nilai)}")

nilai.append(100)
print(f"Setelah append 100: {nilai}")

# ── DICTIONARY ──
print("\\n=== DICTIONARY ===")
profil = {
    "nama"  : "Jastin",
    "level" : 5,
    "xp"    : 1250,
    "badge" : ["Pemula", "Rajin Belajar"],
}
for k, v in profil.items():
    print(f"  {k:8}: {v}")

# Update dictionary
profil["xp"] += 150
profil["level"] = 6
print(f"\\nSetelah update XP: {profil['xp']} XP (Level {profil['level']})")

# ── SET ──
print("\\n=== SET (hapus duplikat) ===")
angka = [1, 2, 3, 2, 4, 3, 5, 1]
unik  = sorted(set(angka))
print(f"Asli  : {angka}")
print(f"Unik  : {unik}")
`,

  error: `# Error Handling — try / except / finally

def bagi(a, b):
    try:
        hasil = a / b
        return hasil
    except ZeroDivisionError:
        print(f"  ⚠️  Tidak bisa membagi {a} dengan 0!")
        return None

def konversi_int(nilai_str):
    try:
        return int(nilai_str)
    except ValueError:
        print(f"  ⚠️  '{nilai_str}' bukan angka valid!")
        return None
    finally:
        print(f"  → Selesai memproses '{nilai_str}'")

# Test pembagian
print("=== Test Pembagian ===")
print(f"10 / 2 = {bagi(10, 2)}")
print(f"5  / 0 = {bagi(5, 0)}")
print(f"9  / 3 = {bagi(9, 3)}")

# Test konversi
print("\\n=== Test Konversi String ke Int ===")
tes = ["42", "abc", "100", "3.14"]
for t in tes:
    hasil = konversi_int(t)
    if hasil is not None:
        print(f"  ✅ Hasil: {hasil}")
`,
};

// Kode default saat pertama buka
const KODE_DEFAULT = `# Selamat datang di JastCodeLab Code Runner! 🐍
# Tulis kode Python kamu di sini
# Tekan ▶ Jalankan atau Ctrl+Enter untuk menjalankan

def sapa(nama):
    return f"Halo, {nama}! Selamat belajar Python 🚀"

print(sapa("JastCodeLab"))

# Coba contoh di toolbar atas ↑
kuadrat = [x**2 for x in range(1, 6)]
print("Kuadrat 1-5:", kuadrat)
`;


// ════════════════════════════════════════
// STATE
// ════════════════════════════════════════

let monacoEditor = null;
let sidebarOpen  = true;
let sedangJalan  = false;


// ════════════════════════════════════════
// SIDEBAR — identik dengan index.html
// ════════════════════════════════════════

function toggleSidebar() {
  if (window.innerWidth > 768) return;
  sidebarOpen = !sidebarOpen;
  applySidebar();
}

function tutupSidebar() {
  if (window.innerWidth > 768) return;
  sidebarOpen = false;
  applySidebar();
}

function applySidebar() {
  const sb  = document.getElementById("sidebar");
  const ma  = document.getElementById("mainArea");
  const ov  = document.getElementById("overlay");
  const mob = window.innerWidth <= 768;

  if (!sb || !ma) return;

  if (!mob) {
    sb.classList.remove("hidden");
    ov.classList.remove("show");
    ma.classList.remove("full");
    ma.style.marginLeft = "220px";
    const cb = document.getElementById("closeSidebarBtn");
    if (cb) cb.style.display = "none";
  } else {
    const cb = document.getElementById("closeSidebarBtn");
    if (cb) cb.style.display = "flex";
    if (sidebarOpen) {
      sb.classList.remove("hidden"); sb.classList.add("show");
      ov.classList.add("show"); ma.classList.add("full");
    } else {
      sb.classList.add("hidden"); sb.classList.remove("show");
      ov.classList.remove("show"); ma.classList.remove("full");
    }
  }

  // Monaco harus relayout saat ukuran berubah
  if (monacoEditor) {
    setTimeout(() => monacoEditor.layout(), 300);
  }
}

window.addEventListener("resize", () => {
  sidebarOpen = window.innerWidth > 768;
  applySidebar();
});


// ════════════════════════════════════════
// UPDATE NAVBAR
// ════════════════════════════════════════

function updateNavUser() {
  const user     = getUser();
  const loggedIn = sudahLogin();

  const loginLi  = document.getElementById("navLoginLi");
  const profilLi = document.getElementById("navProfilLi");
  const logoutBtn = document.getElementById("navLogoutBtn");

  if (loginLi)   loginLi.style.display   = loggedIn ? "none" : "";
  if (profilLi)  profilLi.style.display  = loggedIn ? "" : "none";
  if (logoutBtn) logoutBtn.style.display = loggedIn ? "" : "none";

  if (!user) return;

  const inisial = user.username.charAt(0).toUpperCase();
  const el = (id) => document.getElementById(id);

  if (el("navUsername"))    el("navUsername").textContent = user.username;
  if (el("navAvatar"))      el("navAvatar").textContent   = inisial;
  if (el("topbarAvatar"))   el("topbarAvatar").textContent = inisial;
  if (el("navXP"))          el("navXP").textContent       = `⚡ ${user.xp ?? 0} XP`;

  const navCoins = el("navCoins");
  if (navCoins) {
    navCoins.textContent   = `🪙 ${user.coins ?? 0}`;
    navCoins.style.display = loggedIn ? "" : "none";
  }

  const navStreak  = el("navStreak");
  const streakWrap = el("streakWrap");
  if (navStreak)  navStreak.textContent       = `${user.streak_days ?? 0} Hari`;
  if (streakWrap) streakWrap.style.display    = (user.streak_days > 0) ? "flex" : "none";
}


// ════════════════════════════════════════
// MONACO EDITOR
// ════════════════════════════════════════

function initMonaco() {
  if (typeof require === "undefined") {
    console.error("Monaco loader tidak tersedia.");
    tampilkanFallbackEditor();
    return;
  }

  require.config({
    paths: { vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs" }
  });

  require(["vs/editor/editor.main"], () => {
    monaco.editor.defineTheme("jcl-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "comment",    foreground: "4a5472", fontStyle: "italic" },
        { token: "keyword",    foreground: "a78bfa", fontStyle: "bold"   },
        { token: "string",     foreground: "34d399" },
        { token: "number",     foreground: "fb923c" },
        { token: "function",   foreground: "4f8ef7" },
        { token: "identifier", foreground: "e8edf8" },
        { token: "delimiter",  foreground: "8b95b0" },
      ],
      colors: {
        "editor.background":           "#080c14",
        "editor.foreground":           "#e8edf8",
        "editor.lineHighlightBackground": "#0d1220",
        "editor.selectionBackground":  "#4f8ef730",
        "editorLineNumber.foreground": "#4a5472",
        "editorLineNumber.activeForeground": "#8b95b0",
        "editorCursor.foreground":     "#4f8ef7",
        "scrollbarSlider.background":  "#ffffff10",
        "scrollbarSlider.hoverBackground": "#ffffff18",
      },
    });

    monacoEditor = monaco.editor.create(
      document.getElementById("monacoContainer"),
      {
        value:             KODE_DEFAULT,
        language:          "python",
        theme:             "jcl-dark",
        fontSize:          13.5,
        fontFamily:        "'Roboto Mono', 'JetBrains Mono', 'Fira Code', monospace",
        fontLigatures:     true,
        lineNumbers:       "on",
        minimap:           { enabled: false },
        scrollBeyondLastLine: false,
        automaticLayout:   true,
        tabSize:           4,
        insertSpaces:      true,
        wordWrap:          "off",
        renderLineHighlight: "line",
        cursorBlinking:    "smooth",
        smoothScrolling:   true,
        padding:           { top: 14, bottom: 14 },
        suggest:           { showKeywords: true },
        quickSuggestions:  { other: true, comments: false, strings: false },
        overviewRulerLanes: 0,
        scrollbar: {
          vertical: "auto", horizontal: "auto",
          verticalScrollbarSize: 6, horizontalScrollbarSize: 6,
        },
      }
    );

    // Ctrl+Enter → jalankan
    monacoEditor.addCommand(
      monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter,
      jalankanKode
    );

    // Update info kursor
    monacoEditor.onDidChangeCursorPosition((e) => {
      const el = document.getElementById("infoKursor");
      if (el) el.textContent = `Baris ${e.position.lineNumber}, Kolom ${e.position.column}`;
    });

    // Update info jumlah baris
    monacoEditor.onDidChangeModelContent(updateInfoBaris);
    updateInfoBaris();

    console.log("✅ Monaco Editor siap.");
  });
}

function tampilkanFallbackEditor() {
  const container = document.getElementById("monacoContainer");
  if (!container) return;
  container.innerHTML = `
    <textarea id="fallbackEditor" spellcheck="false" style="
      width:100%;height:100%;background:#080c14;color:#e8edf8;
      font-family:'Roboto Mono',monospace;font-size:13px;line-height:1.7;
      padding:16px;border:none;outline:none;resize:none;tab-size:4;
    " placeholder="# Tulis kode Python kamu di sini...">${KODE_DEFAULT}</textarea>
  `;
  const ta = document.getElementById("fallbackEditor");
  if (ta) {
    ta.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        e.preventDefault();
        const s = ta.selectionStart;
        ta.value = ta.value.substring(0, s) + "    " + ta.value.substring(ta.selectionEnd);
        ta.selectionStart = ta.selectionEnd = s + 4;
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault(); jalankanKode();
      }
    });
  }
}

function getKode() {
  if (monacoEditor) return monacoEditor.getValue();
  const fb = document.getElementById("fallbackEditor");
  return fb ? fb.value : "";
}

function updateInfoBaris() {
  if (!monacoEditor) return;
  const n  = monacoEditor.getModel()?.getLineCount() ?? 0;
  const el = document.getElementById("infoJumlahBaris");
  if (el) el.textContent = `${n} baris`;
}


// ════════════════════════════════════════
// MUAT SAMPLE
// ════════════════════════════════════════

function muatSample(nama) {
  const kode = SAMPLES[nama];
  if (!kode) {
    tampilToast(`Sample '${nama}' tidak ditemukan.`, "warning");
    return;
  }

  if (monacoEditor) {
    monacoEditor.setValue(kode);
    monacoEditor.setScrollTop(0);
    monacoEditor.focus();
  } else {
    const fb = document.getElementById("fallbackEditor");
    if (fb) { fb.value = kode; fb.focus(); }
  }

  bersihkanOutput();
  updateInfoBaris();
  tampilToast(`✅ Contoh "${nama}" dimuat!`, "success", 1500);
}


// ════════════════════════════════════════
// JALANKAN KODE
// ════════════════════════════════════════

async function jalankanKode() {
  if (sedangJalan) return;

  const kode = getKode().trim();
  if (!kode) {
    tampilToast("Tulis kode Python dulu ya!", "info");
    return;
  }

  const elOutput    = document.getElementById("outputKode");
  const elStatus    = document.getElementById("statusRunner");
  const elWaktu     = document.getElementById("infoWaktu");
  const elInfoOut   = document.getElementById("infoOutput");
  const btnJalankan = document.getElementById("tombolJalankan");

  sedangJalan = true;

  if (btnJalankan) {
    btnJalankan.disabled = true;
    btnJalankan.innerHTML = `<span class="spinner"></span> Menjalankan...`;
  }
  if (elStatus)  { elStatus.textContent = "● Menjalankan..."; elStatus.style.color = "#fb923c"; }
  if (elWaktu)   elWaktu.textContent  = "";
  if (elInfoOut) elInfoOut.textContent = "Menjalankan...";
  if (elOutput) {
    elOutput.innerHTML = `<div class="out-line out-dim"><span class="out-prefix">▶</span><span class="out-text">Menjalankan kode...</span></div>`;
  }

  try {
    const hasil = await ApiRunner.jalankan(kode);

    if (hasil.error && hasil.error.trim()) {
      renderOutput(elOutput, "error", hasil.output || "", hasil.error);
      if (elStatus)  { elStatus.textContent = "⚠ Error"; elStatus.style.color = "#f87171"; }
      if (elInfoOut) elInfoOut.textContent = "Selesai dengan error";
    } else {
      renderOutput(elOutput, "success", hasil.output || "");
      const detik = hasil.waktu_eksekusi ? `${hasil.waktu_eksekusi}s` : "";
      if (elStatus)  { elStatus.textContent = `✓ Selesai${detik ? ` · ${detik}` : ""}`; elStatus.style.color = "#34d399"; }
      if (elWaktu)   elWaktu.textContent = detik;
      const baris = (hasil.output || "").trim().split("\n").filter(l=>l).length;
      if (elInfoOut) elInfoOut.textContent = baris > 0 ? `${baris} baris output` : "Selesai (tanpa output)";
    }

  } catch (err) {
    if (elOutput) {
      elOutput.innerHTML = `
        <div class="out-line out-err"><span class="out-prefix">✕</span><span class="out-text">Gagal terhubung ke backend: ${escHtml(err.message)}</span></div>
        <div class="out-separator"></div>
        <div class="out-line out-dim"><span class="out-prefix">▶</span><span class="out-text">Pastikan backend sudah berjalan: cd backend → uvicorn main:app --reload</span></div>
      `;
    }
    if (elStatus)  { elStatus.textContent = "✕ Gagal"; elStatus.style.color = "#f87171"; }
    if (elInfoOut) elInfoOut.textContent = "Gagal terhubung";
  }

  sedangJalan = false;
  if (btnJalankan) {
    btnJalankan.disabled = false;
    btnJalankan.innerHTML = `
      <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      Jalankan <kbd>Ctrl+↵</kbd>
    `;
  }
}

function renderOutput(el, tipe, stdout, stderr = "") {
  if (!el) return;
  let html = "";
  if (stdout && stdout.trim()) {
    html += stdout.trimEnd().split("\n").map(b =>
      `<div class="out-line"><span class="out-prefix">▶</span><span class="out-text">${escHtml(b)}</span></div>`
    ).join("");
  }
  if (stderr && stderr.trim()) {
    if (html) html += `<div class="out-separator"></div>`;
    html += stderr.trimEnd().split("\n").map(b =>
      `<div class="out-line out-err"><span class="out-prefix">✕</span><span class="out-text">${escHtml(b)}</span></div>`
    ).join("");
  }
  if (!html) {
    html = `<div class="out-line out-dim"><span class="out-prefix">▶</span><span class="out-text">(tidak ada output)</span></div>`;
  }
  el.innerHTML = html;
}


// ════════════════════════════════════════
// BERSIHKAN OUTPUT
// ════════════════════════════════════════

function bersihkanOutput() {
  const el = document.getElementById("outputKode");
  if (el) {
    el.innerHTML = `<div class="out-line out-dim"><span class="out-prefix">▶</span><span class="out-text">Tekan ▶ Jalankan atau Ctrl+Enter untuk melihat output...</span></div>`;
  }
  const elInfoOut = document.getElementById("infoOutput");
  const elWaktu   = document.getElementById("infoWaktu");
  const elStatus  = document.getElementById("statusRunner");
  if (elInfoOut) elInfoOut.textContent = "Belum ada output";
  if (elWaktu)   elWaktu.textContent   = "";
  if (elStatus)  { elStatus.textContent = "● Siap"; elStatus.style.color = "var(--txt3)"; }
}


// ════════════════════════════════════════
// TOAST
// ════════════════════════════════════════

function tampilToast(pesan, tipe = "info", durasi = 3000) {
  let c = document.getElementById("toastContainer");
  if (!c) return;
  const el    = document.createElement("div");
  const warna = { success:"#34d399", error:"#f87171", warning:"#fb923c", info:"#4f8ef7" }[tipe] || "#4f8ef7";
  el.style.cssText = `background:#111827;border:1px solid ${warna}33;border-left:3px solid ${warna};color:${warna};padding:11px 16px;border-radius:8px;font-size:13px;font-weight:500;max-width:300px;box-shadow:0 4px 16px rgba(0,0,0,.4);animation:toastIn .2s ease;`;
  el.textContent = pesan;
  c.appendChild(el);
  setTimeout(() => {
    el.style.opacity = "0"; el.style.transition = "opacity .3s";
    setTimeout(() => el.remove(), 300);
  }, durasi);
}


// ════════════════════════════════════════
// HELPER
// ════════════════════════════════════════

function escHtml(s) {
  return String(s ?? "")
    .replace(/&/g,"&amp;").replace(/</g,"&lt;")
    .replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}


// ════════════════════════════════════════
// INIT
// ════════════════════════════════════════

document.addEventListener("DOMContentLoaded", async () => {
  // Sidebar
  sidebarOpen = window.innerWidth > 768;
  applySidebar();

  // Navbar
  updateNavUser();

  // Monaco
  initMonaco();

  // Refresh profil jika sudah login
  if (sudahLogin()) {
    try {
      const profil = await ApiUser.getProfil();
      if (typeof updateUserStats === "function") updateUserStats(profil.xp, profil.streak_days);
      updateNavUser();
    } catch(_) {}
  }
});