/**
 * JastCodeLab — Sidebar Auto-Patch
 * =================================
 * Tambahkan ini di SEMUA file Frontend setelah auth.js:
 *   <script src="js/sidebar-patch.js"></script>
 *
 * File ini akan:
 * 1. Mengganti semua nav-item di sidebar dengan menu lengkap
 * 2. Menambahkan menu yang kurang (Daily Challenge, Teman, Shop)
 * 3. Mengganti nama "Kode Runner" → "Code Runner" secara konsisten
 * 4. Membuat sidebar selalu terbuka di desktop
 * 5. Menandai menu aktif berdasarkan halaman saat ini
 */

(function() {
  'use strict';

  // Daftar menu lengkap
  const MENU_ITEMS = [
    { href: 'index.html',      label: 'Beranda',         icon: '<path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>' },
    { href: 'learn.html',      label: 'Belajar',          icon: '<path d="M2 3h6a4 4 0 014 4v14a3 3 0 00-3-3H2z"/><path d="M22 3h-6a4 4 0 00-4 4v14a3 3 0 013-3h7z"/>' },
    { href: 'daily.html',      label: 'Daily Challenge',  icon: '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>' },
    { href: 'runner.html',     label: 'Code Runner',      icon: '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>' },
    { href: 'challenges.html', label: 'Tantangan',        icon: '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>' },
    { href: 'community.html',  label: 'Komunitas',        icon: '<path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>' },
    { divider: true },
    { href: 'friends.html',    label: 'Teman',            icon: '<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/>' },
    { href: 'shop.html',       label: 'Shop',             icon: '<path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 01-8 0"/>' },
  ];

  // Deteksi halaman aktif dari URL
  function getActivePage() {
    const path = window.location.pathname;
    const file = path.split('/').pop() || 'index.html';
    return file;
  }

  // Buat nav item HTML
  function makeNavItem(item, activePage) {
    if (item.divider) {
      return '<div style="height:1px;background:rgba(255,255,255,.07);margin:6px 4px;"></div>';
    }
    const isActive = item.href === activePage;
    const activeClass = isActive ? ' active' : '';
    return `<li><a href="${item.href}" class="nav-item${activeClass}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${item.icon}</svg>${item.label}</a></li>`;
  }

  // Inject menu ke sidebar
  function injectSidebarMenu() {
    const sbNav = document.querySelector('.sb-nav');
    if (!sbNav) return;

    const activePage = getActivePage();

    // Buat semua nav items
    let navHTML = MENU_ITEMS.map(item => makeNavItem(item, activePage)).join('\n');

    // Tambah divider dan item akun
    navHTML += `
      <div style="height:1px;background:rgba(255,255,255,.07);margin:6px 4px;"></div>
      <li id="navLoginLi"><a href="login.html" class="nav-item"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>Masuk</a></li>
      <li id="navProfilLi" style="display:none;"><a href="profile.html" class="nav-item${'profile.html' === activePage ? ' active' : ''}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>Profil Saya</a></li>
    `;

    sbNav.innerHTML = navHTML;
  }

  // Fix nama "Kode Runner" → "Code Runner" di semua elemen teks
  function fixCodeRunnerLabel() {
    // Fix di nav items
    document.querySelectorAll('.nav-item').forEach(el => {
      if (el.textContent.includes('Kode Runner')) {
        el.innerHTML = el.innerHTML.replace('Kode Runner', 'Code Runner');
      }
    });

    // Fix di topbar title
    document.querySelectorAll('.topbar-title, .topbar-title *').forEach(el => {
      if (el.childNodes) {
        el.childNodes.forEach(node => {
          if (node.nodeType === 3 && node.textContent.includes('Kode Runner')) {
            node.textContent = node.textContent.replace('Kode Runner', 'Code Runner');
          }
        });
      }
    });
  }

  // Tambah close button jika belum ada
  function ensureCloseButton() {
    const sbLogo = document.querySelector('.sb-logo');
    if (!sbLogo) return;
    if (!document.getElementById('closeSidebarBtn')) {
      const btn = document.createElement('button');
      btn.id = 'closeSidebarBtn';
      btn.className = 'close-btn';
      btn.setAttribute('onclick', 'tutupSidebar()');
      btn.style.cssText = 'background:none;border:none;cursor:pointer;color:var(--txt3);padding:4px;border-radius:5px;display:none;';
      btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';
      sbLogo.appendChild(btn);
    }
  }

  // Tambah streak wrap jika belum ada
  function ensureStreakWrap() {
    const sbBottom = document.querySelector('.sb-bottom');
    if (!sbBottom) return;
    if (!document.getElementById('streakWrap')) {
      const wrap = document.createElement('div');
      wrap.id = 'streakWrap';
      wrap.className = 'streak-wrap';
      wrap.style.display = 'none';
      wrap.innerHTML = `
        <span style="font-size:18px;">🔥</span>
        <div>
          <div style="font-family:var(--fn-display);font-size:14px;font-weight:800;color:var(--orange);" id="navStreakDays">0 Hari</div>
          <div style="font-size:10px;color:var(--txt3);font-family:var(--fn-mono);">Streak Aktif</div>
        </div>
      `;
      sbBottom.insertBefore(wrap, sbBottom.firstChild);
    }
  }

  // Override sidebar functions untuk desktop always-open
  window.toggleSidebar = function() {
    if (window.innerWidth > 768) return;
    window._sidebarOpen = !window._sidebarOpen;
    applyNewSidebar();
  };

  window.tutupSidebar = function() {
    if (window.innerWidth > 768) return;
    window._sidebarOpen = false;
    applyNewSidebar();
  };

  function applyNewSidebar() {
    const sb  = document.getElementById('sidebar');
    const ma  = document.getElementById('mainArea');
    const mob = window.innerWidth <= 768;

    if (!sb || !ma) return;

    // Cari overlay (berbagai nama yang dipakai)
    const ov = document.getElementById('sbOverlay') ||
               document.getElementById('overlay') ||
               document.getElementById('sidebarOverlay');

    const cb = document.getElementById('closeSidebarBtn');

    if (!mob) {
      // Desktop: SELALU terbuka
      sb.classList.remove('hidden', 'sb-hidden');
      sb.classList.add('show', 'sb-show');
      if (ov) ov.classList.remove('show');
      ma.classList.remove('full');
      ma.style.marginLeft = '220px';
      if (cb) cb.style.display = 'none';
    } else {
      // Mobile: bisa toggle
      if (cb) cb.style.display = 'flex';
      if (window._sidebarOpen) {
        sb.classList.remove('hidden', 'sb-hidden');
        sb.classList.add('show', 'sb-show');
        if (ov) ov.classList.add('show');
        ma.classList.add('full');
      } else {
        sb.classList.add('hidden', 'sb-hidden');
        sb.classList.remove('show', 'sb-show');
        if (ov) ov.classList.remove('show');
        ma.classList.remove('full');
      }
    }
  }

  // Override applySidebar juga
  window.applySidebar = applyNewSidebar;

  window.addEventListener('resize', applyNewSidebar);

  // Init
  window._sidebarOpen = false; // default mobile tertutup

  function init() {
    injectSidebarMenu();
    ensureCloseButton();
    ensureStreakWrap();
    fixCodeRunnerLabel();

    // Init sidebar state
    window._sidebarOpen = window.innerWidth > 768;
    applyNewSidebar();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Jalankan lagi setelah load penuh (untuk menangani halaman yang lambat)
  window.addEventListener('load', function() {
    applyNewSidebar();
    fixCodeRunnerLabel();
  });

})();