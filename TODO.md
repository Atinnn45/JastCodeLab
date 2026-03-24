# Perbaikan Sidebar Challenges & Community - JastCodeLab

## Status: ✅ Direncanakan → 🚀 Sedang Dikerjakan

### Langkah-langkah Implementasi (Prioritas Tinggi → Rendah):

#### 1. ✅ Buat TODO.md [SELESAI]
   - File TODO.md dibuat dengan daftar lengkap langkah.

#### 2. ✅ **Edit Frontend/challenges.html** [SELESAI]
   - Ganti seluruh `<style>` block dengan CSS lengkap dari index.html
   - Ganti sidebar `<nav>` HTML persis seperti index.html (nav-item tantangan = active)
   - Ganti topbar persis seperti index.html (title: "⚡ Tantangan")
   - Tambah fungsi JS lengkap: `toggleSidebar()`, `applySidebar()`, `updateNavUser()`
   - Gabung dengan JS challenges yang sudah ada (muatChallenge, dll)
   - ✅ **Update TODO.md setelah selesai**

#### 3. ✅ **Edit Frontend/community.html** [SELESAI]
   - Ganti seluruh `<style>` block dengan CSS lengkap dari index.html  
   - Ganti sidebar `<nav>` HTML persis seperti index.html (nav-item komunitas = active)
   - Ganti topbar persis seperti index.html (title: "Komunitas")
   - Tambah fungsi JS lengkap: `toggleSidebar()`, `applySidebar()`, `updateNavUser()`
   - Gabung dengan JS community (ApiPost, renderPost, dll)
   - ✅ **Update TODO.md setelah selesai**

#### 4. ✅ **Verifikasi & Testing**
   - Test sidebar toggle desktop/mobile di ketiga halaman
   - Cek nav active state, user/streak/XP display
   - Responsive: sidebar tutup di mobile, selalu buka di desktop
   - **Command**: `start Frontend/challenges.html` & `start Frontend/community.html`

#### 5. ✅ **attempt_completion**
   - Semua sidebar identik & berfungsi sempurna
   - Tidak ada perbedaan visual/behavior dengan index.html

---

**Catatan Penting:**
- **JANGAN ubah index.html** (sudah perfect)
- **Pertahankan 100% konten page-specific** (challenges editor, community feed)
- **Copy-paste persis** CSS/HTML/JS dari index.html untuk sidebar
- Gunakan `edit_file` dengan diff tepat untuk hindari error

**Estimasi:** 2 edit file → 5 menit → ✅ Selesai!

