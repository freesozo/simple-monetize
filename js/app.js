(function () {
  'use strict';

  let products = [];
  let config = {};
  let currentCategory = 'all';
  let currentSort = 'rating';
  let showFavOnly = false;
  let favorites = JSON.parse(localStorage.getItem('toolFavorites') || '[]');
  let currentPage = 1;
  const perPage = 24;
  let lastFiltered = [];
  let currentPriceFilter = 'all';
  let activeTags = [];

  // SVG line icons for category tabs (stroke 1.5px, currentColor, monochrome)
  const CATEGORY_SVG = {
    server: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><circle cx="6" cy="6" r="1"/><circle cx="6" cy="18" r="1"/></svg>',
    vpn: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    learning: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    ai: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M9 9h6v6H9z"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>',
    design: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.93 0 1.5-.67 1.5-1.5 0-.39-.15-.74-.39-1.04-.24-.3-.39-.65-.39-1.04 0-.83.67-1.5 1.5-1.5H16c3.31 0 6-2.69 6-6 0-5.17-4.49-9-10-9z"/></svg>',
    cloud: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>',
    domain: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    sitebuilder: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>',
    ecommerce: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
    project: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 14l2 2 4-4"/></svg>',
    communication: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    security: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    seo: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>',
    video: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="2.18"/><path d="M7 2v20M17 2v20M2 12h20M2 7h5M2 17h5M17 17h5M17 7h5"/></svg>',
    photo: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>',
    accounting: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    marketing: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    password: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>',
    writing: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>'
  };

  // ===== Theme =====
  function initTheme() {
    const btn = document.getElementById('themeBtn');
    if (!btn) return;
    let theme = localStorage.getItem('theme');
    if (!theme) theme = window.matchMedia('(prefers-color-scheme:dark)').matches ? 'dark' : 'light';
    document.documentElement.dataset.theme = theme;
    btn.textContent = theme === 'dark' ? '☀️' : '🌙';
    btn.addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      localStorage.setItem('theme', next);
      btn.textContent = next === 'dark' ? '☀️' : '🌙';
    });
  }

  // ===== Language =====
  function initLang() {
    const btn = document.getElementById('langBtn');
    if (!btn) return;
    btn.textContent = I18n.t('lang');
    btn.addEventListener('click', () => {
      I18n.toggle();
      btn.textContent = I18n.t('lang');
      // Re-render dynamic content
      if (document.getElementById('productGrid')) {
        renderCategories();
        renderRecentlyViewed();
        renderFavoritesHome();
        renderFeatured();
        renderBlogHighlights();
        filterProducts();
      } else if (document.getElementById('reviewContent')) {
        initReviewPage();
      }
    });
    // Also listen for langchange event
    window.addEventListener('langchange', () => {
      btn.textContent = I18n.t('lang');
    });
  }

  // ===== Init =====
  async function init() {
    initTheme();

    // Resolve base path for data files (works from /blog/ subdirectory too)
    var basePath = '';
    var pathParts = location.pathname.split('/');
    if (pathParts.length > 2 && pathParts[pathParts.length - 2] !== '') {
      // We're in a subdirectory (e.g., /blog/xxx.html) → go up
      basePath = '../'.repeat(pathParts.length - 2);
    }
    try {
      const [prodRes, confRes] = await Promise.all([
        fetch(basePath + 'data/products.json'),
        fetch(basePath + 'data/config.json')
      ]);
      if (!prodRes.ok || !confRes.ok) throw new Error('HTTP ' + prodRes.status);
      products = (await prodRes.json()).products;
      config = await confRes.json();
    } catch (e) {
      console.error('Data load error:', e);
      showToast('データの読み込みに失敗しました');
      return;
    }

    if (document.getElementById('productGrid')) {
      initIndexPage();
    } else if (document.getElementById('reviewContent')) {
      initReviewPage();
    }
    renderBlogHighlights();
    initBackToTop();
    initLang();
    I18n.applyAll();
  }

  // ===== Favorites =====
  function isFav(id) { return favorites.includes(id); }
  function toggleFav(id) {
    if (isFav(id)) {
      favorites = favorites.filter(f => f !== id);
    } else {
      favorites.push(id);
    }
    localStorage.setItem('toolFavorites', JSON.stringify(favorites));
    // Re-render
    renderFeatured();
    renderRecentlyViewed();
    renderFavoritesHome();
    filterProducts();
  }
  window.toggleFav = toggleFav;

  // ===== Recently Viewed =====
  function trackRecentlyViewed(id) {
    let recent = JSON.parse(localStorage.getItem('recentlyViewed') || '[]');
    recent = recent.filter(r => r !== id);
    recent.unshift(id);
    if (recent.length > 8) recent = recent.slice(0, 8);
    localStorage.setItem('recentlyViewed', JSON.stringify(recent));
  }

  function renderRecentlyViewed() {
    const section = document.getElementById('recentSection');
    const grid = document.getElementById('recentGrid');
    if (!section || !grid) return;
    const recent = JSON.parse(localStorage.getItem('recentlyViewed') || '[]');
    const recentProducts = recent.map(id => products.find(p => p.id === id)).filter(p => p && p.status === 'active');
    if (recentProducts.length === 0) { section.style.display = 'none'; return; }
    section.style.display = '';
    grid.innerHTML = recentProducts.map(p => createProductCard(p, false)).join('');
  }

  function renderFavoritesHome() {
    const section = document.getElementById('favHomeSection');
    const grid = document.getElementById('favHomeGrid');
    if (!section || !grid) return;
    const favProducts = products.filter(p => isFav(p.id) && p.status === 'active');
    if (favProducts.length === 0) { section.style.display = 'none'; return; }
    section.style.display = '';
    grid.innerHTML = favProducts.map(p => createProductCard(p, false)).join('');
  }

  // ===== Index Page =====
  function initIndexPage() {
    // Category page support (e.g., ai.html)
    var pageCategory = document.getElementById('productGrid')?.dataset.category;
    if (pageCategory) currentCategory = pageCategory;

    renderCategories();
    renderSortBar();
    renderRecentlyViewed();
    renderFavoritesHome();
    renderFeatured();
    renderHiddenGems();
    filterProducts();
    initSearch();
    initFilters();
    initQuiz();
    // Load more
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) loadMoreBtn.addEventListener('click', loadMore);
  }

  function renderSortBar() {
    const container = document.getElementById('sortBar');
    if (!container) return;
    container.innerHTML = '';
    // Sort select
    const sel = document.createElement('select');
    sel.className = 'sort-select';
    sel.innerHTML = `<option value="rating">${I18n.t('sortRating')}</option><option value="name">${I18n.t('sortName')}</option>`;
    sel.value = currentSort;
    sel.addEventListener('change', () => { currentSort = sel.value; filterProducts(); });
    // Fav toggle
    const favBtn = document.createElement('button');
    favBtn.className = 'fav-filter-btn' + (showFavOnly ? ' active' : '');
    favBtn.textContent = I18n.t('favOnly');
    favBtn.addEventListener('click', () => {
      showFavOnly = !showFavOnly;
      favBtn.classList.toggle('active', showFavOnly);
      filterProducts();
    });
    container.appendChild(sel);
    container.appendChild(favBtn);
  }

  function renderCategories() {
    const grid = document.getElementById('categoryGrid');
    if (!grid) return;
    grid.innerHTML = '';
    // "All" button
    const allBtn = document.createElement('button');
    allBtn.className = 'category-btn' + (currentCategory === 'all' ? ' active' : '');
    allBtn.dataset.category = 'all';
    allBtn.textContent = I18n.t('categoryAll');
    allBtn.addEventListener('click', () => {
      document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
      allBtn.classList.add('active');
      currentCategory = 'all';
      filterProducts();
    });
    grid.appendChild(allBtn);

    config.categories.forEach(cat => {
      const btn = document.createElement('button');
      btn.className = 'category-btn' + (currentCategory === cat.id ? ' active' : '');
      btn.dataset.category = cat.id;
      const catName = I18n.getLang() === 'en' ? (cat.nameEn || cat.name) : cat.name;
      const svgIcon = CATEGORY_SVG[cat.id] || '';
      btn.innerHTML = svgIcon + ' ' + catName;
      btn.addEventListener('click', () => {
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = cat.id;
        filterProducts();
      });
      grid.appendChild(btn);
    });
  }

  function renderFeatured() {
    const grid = document.getElementById('featuredGrid');
    if (!grid) return;
    const titleEl = document.getElementById('featuredTitle');
    const featured = products.filter(p => p.featured && p.status === 'active');
    if (featured.length === 0) {
      if (titleEl) titleEl.style.display = 'none';
      grid.style.display = 'none';
      return;
    }
    grid.innerHTML = featured.map(p => createProductCard(p, true)).join('');
    if (fadeObserver) {
      grid.querySelectorAll('.product-card').forEach(function(card, i) {
        card.classList.add('fade-in-up');
        card.style.transitionDelay = i * 0.05 + 's';
        fadeObserver.observe(card);
      });
    }
  }

  function renderHiddenGems() {
    const section = document.getElementById('hiddenGemSection');
    const grid = document.getElementById('hiddenGemGrid');
    if (!section || !grid) return;
    const gems = products.filter(p => p.isHiddenGem && p.status === 'active');
    if (gems.length === 0) { section.style.display = 'none'; return; }
    section.style.display = '';
    grid.innerHTML = gems.map(p => createProductCard(p, false)).join('');
    if (fadeObserver) {
      grid.querySelectorAll('.product-card').forEach(function(card, i) {
        card.classList.add('fade-in-up');
        card.style.transitionDelay = i * 0.05 + 's';
        fadeObserver.observe(card);
      });
    }
  }

  function renderProducts(list, append) {
    const grid = document.getElementById('productGrid');
    const noResults = document.getElementById('noResults');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const resultCount = document.getElementById('resultCount');
    if (!grid) return;
    const active = list.filter(p => p.status === 'active');
    lastFiltered = active;
    if (active.length === 0) {
      grid.innerHTML = '';
      if (noResults) {
        noResults.style.display = 'block';
        noResults.querySelector('p').textContent = I18n.t('noResults');
      }
      if (loadMoreBtn) loadMoreBtn.style.display = 'none';
      if (resultCount) resultCount.textContent = '';
      return;
    }
    if (noResults) noResults.style.display = 'none';
    const shown = currentPage * perPage;
    const visible = active.slice(0, shown);
    if (append) {
      grid.innerHTML += active.slice(shown - perPage, shown).map(p => createProductCard(p, false)).join('');
    } else {
      grid.innerHTML = visible.map(p => createProductCard(p, false)).join('');
    }
    // Staggered fade-in for cards
    if (fadeObserver) {
      grid.querySelectorAll('.product-card').forEach(function(card, i) {
        if (!card.classList.contains('fade-in-up')) {
          card.classList.add('fade-in-up');
          card.style.transitionDelay = (i % 12) * 0.05 + 's';
          fadeObserver.observe(card);
        }
      });
    }
    // Load more button
    if (loadMoreBtn) {
      loadMoreBtn.style.display = shown < active.length ? 'inline-block' : 'none';
    }
    // Result count
    if (resultCount) {
      const showing = Math.min(shown, active.length);
      const lang = I18n.getLang();
      resultCount.textContent = lang === 'en'
        ? `Showing ${showing} of ${active.length} tools`
        : `${active.length}件中 ${showing}件を表示`;
    }
  }

  function formatVerifiedDate(dateStr) {
    if (!dateStr) return I18n.t('verifiedDefault');
    const d = new Date(dateStr);
    if (I18n.getLang() === 'en') {
      const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      return I18n.t('verifiedPrefix') + months[d.getMonth()] + ' ' + d.getFullYear();
    }
    return I18n.t('verifiedPrefix') + d.getFullYear() + '年' + (d.getMonth() + 1) + '月 ' + I18n.t('verifiedSuffix');
  }

  // Category colors for initials icon
  const CATEGORY_COLORS = {
    server:'#3d5a80', vpn:'#6d597a', learning:'#457b6e', ai:'#4a6fa5',
    design:'#8b7bb8', cloud:'#5c6b73', domain:'#2d3142', sitebuilder:'#9e8c6c',
    ecommerce:'#b56b4f', project:'#7d8570', communication:'#6a4c93',
    security:'#8b8589', seo:'#a68a64', video:'#b56b4f', photo:'#8b7bb8',
    accounting:'#2d3142', marketing:'#6d597a', password:'#5c6b73', writing:'#457b6e'
  };

  function getInitials(name) {
    // For ASCII names, take first 2 chars uppercase; for Japanese, take first 2 chars
    const clean = name.replace(/[^\w\u3000-\u9fff\uff00-\uffef]/g, '').trim();
    if (!clean) return name.substring(0, 2);
    return clean.substring(0, 2).toUpperCase();
  }

  function createProductCard(product, isFeatured) {
    const catName = getCategoryName(product.category);
    const isNew = product.dateAdded && (Date.now() - new Date(product.dateAdded).getTime()) < 30 * 86400000;
    const newBadge = isNew ? ' <span class="new-badge">NEW</span>' : '';
    const regionFlag = product.region === 'jp' ? '🇯🇵' : '🌐';
    const regionLabel = product.region === 'jp' ? (I18n.getLang() === 'en' ? 'Japan' : '日本') : (I18n.getLang() === 'en' ? 'Global' : '海外');
    const featuredClass = (isFeatured || product.featured) ? ' featured' : '';
    const affiliateLink = product.affiliateUrl || product.officialUrl;
    const faved = isFav(product.id);
    const favLabel = faved ? I18n.t('favRemove') : I18n.t('favAdd');
    const initials = getInitials(product.name);
    const catColor = CATEGORY_COLORS[product.category] || '#4a6fa5';
    return `
      <div class="product-card${featuredClass}" data-featured-label="${escapeHtml(I18n.getLang() === 'en' ? '★ Top Pick' : '★ おすすめ')}">
        <div class="card-body">
          <div class="card-top-row">
            <span class="card-category">${escapeHtml(catName)}${newBadge} <span class="card-region card-region-${product.region || 'global'}">${regionFlag} ${regionLabel}</span></span>
            <button class="fav-btn${faved ? ' active' : ''}" onclick="toggleFav('${product.id}')" title="${favLabel}">${faved ? '❤️' : '🤍'}</button>
          </div>
          <div class="card-identity">
            <span class="card-initials" style="background:${catColor}">${escapeHtml(initials)}</span>
            <div class="card-identity-info">
              <h3 class="card-title">${escapeHtml(product.name)}</h3>
              <span class="card-price">${escapeHtml(product.price)}</span>
            </div>
            <span class="card-score">★ ${product.rating}</span>
          </div>
          <p class="card-summary">${escapeHtml(I18n.getLang() === 'en' ? (product.summaryEn || product.summary) : product.summary)}</p>
          ${product.recommendedFor ? `<p class="card-recommended">${I18n.t('recommendedForLabel')} ${escapeHtml(product.recommendedFor)}</p>` : ''}
          <div class="card-actions">
            <a href="review.html?id=${product.id}" class="btn btn-outline">${I18n.t('viewDetail')}</a>
            <a href="${escapeHtml(affiliateLink)}" class="btn btn-primary" target="_blank" rel="noopener noreferrer nofollow" onclick="trackClick('${product.id}')">${I18n.t('visitOfficial')}</a>
          </div>
          <span class="card-verified">${formatVerifiedDate(product.lastChecked)}</span>
        </div>
      </div>`;
  }

  function initFilters() {
    // Price filter
    document.getElementById('priceFilters')?.addEventListener('click', (e) => {
      const chip = e.target.closest('[data-price]');
      if (!chip) return;
      document.querySelectorAll('#priceFilters .filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentPriceFilter = chip.dataset.price;
      filterProducts();
    });
    // Tag filter (multi-select)
    document.getElementById('tagFilters')?.addEventListener('click', (e) => {
      const chip = e.target.closest('[data-tag]');
      if (!chip) return;
      chip.classList.toggle('active');
      activeTags = [...document.querySelectorAll('#tagFilters .filter-chip.active')].map(c => c.dataset.tag);
      filterProducts();
    });
  }

  function parsePrice(priceStr) {
    if (!priceStr) return 0;
    if (priceStr.includes('無料')) return 0;
    const yen = priceStr.match(/[¥￥]([0-9,]+)/);
    if (yen) return parseInt(yen[1].replace(/,/g, ''));
    const dollar = priceStr.match(/\$([0-9.]+)/);
    if (dollar) return Math.round(parseFloat(dollar[1]) * 150);
    return 0;
  }

  function filterProducts() {
    currentPage = 1;
    const query = (document.getElementById('searchInput')?.value || '').toLowerCase();
    let filtered = products;
    if (currentCategory !== 'all') {
      filtered = filtered.filter(p => p.category === currentCategory);
    }
    if (query) {
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.summary.toLowerCase().includes(query) ||
        p.description.toLowerCase().includes(query)
      );
    }
    if (showFavOnly) {
      filtered = filtered.filter(p => isFav(p.id));
    }
    // Price filter
    if (currentPriceFilter !== 'all') {
      filtered = filtered.filter(p => {
        const price = parsePrice(p.price);
        switch (currentPriceFilter) {
          case 'free': return price === 0;
          case 'low': return price > 0 && price <= 1000;
          case 'mid': return price > 1000 && price <= 5000;
          case 'high': return price > 5000;
          default: return true;
        }
      });
    }
    // Tag filter (AND)
    if (activeTags.length > 0) {
      filtered = filtered.filter(p => {
        const tags = p.tags || [];
        return activeTags.every(t => tags.includes(t));
      });
    }
    // Sort
    if (currentSort === 'name') {
      filtered = [...filtered].sort((a, b) => a.name.localeCompare(b.name, 'ja'));
    } else {
      filtered = [...filtered].sort((a, b) => b.rating - a.rating);
    }
    renderProducts(filtered, false);
  }

  function loadMore() {
    currentPage++;
    renderProducts(lastFiltered, true);
  }

  function initSearch() {
    const input = document.getElementById('searchInput');
    const btn = document.getElementById('searchBtn');
    if (!input) return;
    input.addEventListener('input', debounce(filterProducts, 300));
    btn?.addEventListener('click', filterProducts);
  }

  // ===== Review Page =====
  function initReviewPage() {
    const id = new URLSearchParams(location.search).get('id');
    const product = products.find(p => p.id === id);
    const loading = document.getElementById('loading');
    const content = document.getElementById('reviewContent');

    if (!product) {
      loading.innerHTML = '<p>' + I18n.t('notFound') + '<br><a href="index.html">' + I18n.t('backHome') + '</a></p>';
      return;
    }

    // Track recently viewed
    trackRecentlyViewed(product.id);

    // Update meta
    document.title = product.name + (I18n.getLang() === 'en' ? ' Review | Tool Compare Navi' : ' レビュー｜おすすめツール比較ナビ');
    const pageUrl = 'https://tools.freesozo.com/review.html?id=' + product.id;
    const metaDesc = product.name + (I18n.getLang() === 'en' ? ' - Detailed review. ' : 'を徹底レビュー。') + product.summary;
    document.querySelector('meta[name="description"]')?.setAttribute('content', metaDesc);
    document.querySelector('meta[property="og:title"]')?.setAttribute('content', product.name + (I18n.getLang() === 'en' ? ' Review' : ' レビュー'));
    document.querySelector('meta[property="og:description"]')?.setAttribute('content', metaDesc);
    document.querySelector('meta[property="og:url"]')?.setAttribute('content', pageUrl);
    document.querySelector('link[rel="canonical"]')?.setAttribute('href', pageUrl);

    // JSON-LD (only add once)
    if (!document.querySelector('script[data-product-ld]')) {
      const jsonLd = document.createElement('script');
      jsonLd.type = 'application/ld+json';
      jsonLd.dataset.productLd = '1';
      jsonLd.textContent = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "description": product.description,
        "review": {
          "@type": "Review",
          "reviewRating": { "@type": "Rating", "ratingValue": product.rating, "bestRating": 5 },
          "author": { "@type": "Organization", "name": "おすすめツール比較ナビ" }
        },
        "aggregateRating": { "@type": "AggregateRating", "ratingValue": product.rating, "bestRating": 5, "ratingCount": 1 }
      });
      document.head.appendChild(jsonLd);

      const bcLd = document.createElement('script');
      bcLd.type = 'application/ld+json';
      bcLd.textContent = JSON.stringify({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://tools.freesozo.com/" },
          { "@type": "ListItem", "position": 2, "name": getCategoryName(product.category) },
          { "@type": "ListItem", "position": 3, "name": product.name }
        ]
      });
      document.head.appendChild(bcLd);
    }

    const catName = getCategoryName(product.category);
    const stars = '★'.repeat(Math.floor(product.rating)) + (product.rating % 1 >= 0.5 ? '☆' : '');

    // Breadcrumb
    document.getElementById('breadcrumbCategory').textContent = catName;
    document.getElementById('breadcrumbName').textContent = product.name;

    // Header
    document.getElementById('reviewTitle').textContent = product.name;
    document.getElementById('reviewRating').textContent = stars + ' ' + product.rating;
    document.getElementById('reviewPrice').textContent = product.price;
    document.getElementById('reviewBadge').textContent = I18n.t('recommended');

    // Description
    document.getElementById('reviewDescription').innerHTML = '<p>' + escapeHtml(I18n.getLang() === 'en' ? (product.descriptionEn || product.description) : product.description) + '</p>';

    // Pros/Cons labels
    document.getElementById('prosLabel').textContent = I18n.t('merit');
    document.getElementById('consLabel').textContent = I18n.t('demerit');
    document.getElementById('featuresLabel').textContent = I18n.t('features');

    // Pros
    document.getElementById('reviewPros').innerHTML =
      product.pros.map(p => '<li>' + escapeHtml(p) + '</li>').join('');

    // Cons
    document.getElementById('reviewCons').innerHTML =
      product.cons.map(c => '<li>' + escapeHtml(c) + '</li>').join('');

    // Features
    document.getElementById('reviewFeatures').innerHTML =
      product.features.map(f => '<li>' + escapeHtml(f) + '</li>').join('');

    // Free Features
    var freeFeatSection = document.getElementById('freeFeaturesSection');
    if (freeFeatSection && (product.freeFeatures?.length || product.freeLimit)) {
      freeFeatSection.style.display = '';
      if (product.freeLimit) {
        document.getElementById('freeLimitText').textContent = product.freeLimit;
      }
      if (product.freeFeatures?.length) {
        document.getElementById('reviewFreeFeatures').innerHTML =
          product.freeFeatures.map(f => '<li>' + escapeHtml(f) + '</li>').join('');
      }
    }

    // Verified date
    var verifiedEl = document.getElementById('reviewVerified');
    if (verifiedEl) {
      verifiedEl.textContent = I18n.t('lastVerifiedLabel') + ' ' + formatVerifiedDate(product.lastChecked);
    }

    // Recommended For
    var recoSection = document.getElementById('recommendedSection');
    if (recoSection && product.recommendedFor) {
      recoSection.style.display = '';
      document.getElementById('reviewRecommendedFor').textContent = product.recommendedFor;
    }

    // Alternatives
    var altSection = document.getElementById('alternativesSection');
    if (altSection && product.alternatives?.length) {
      var altProducts = product.alternatives.map(id => products.find(p => p.id === id)).filter(p => p && p.status === 'active');
      if (altProducts.length > 0) {
        altSection.style.display = '';
        document.getElementById('alternativesGrid').innerHTML = altProducts.map(p => createProductCard(p, false)).join('');
      }
    }

    // CTA
    const affiliateLink = product.affiliateUrl || product.officialUrl;
    document.getElementById('ctaTitle').textContent = product.name + I18n.t('tryTool');
    document.getElementById('ctaSubtext').textContent = I18n.t('checkOfficial');
    const ctaBtn = document.getElementById('ctaAffiliate');
    ctaBtn.href = affiliateLink;
    ctaBtn.textContent = I18n.t('goOfficial');
    ctaBtn.onclick = () => trackClick(product.id);
    const ctaOfficial = document.getElementById('ctaOfficial');
    ctaOfficial.href = product.officialUrl;
    ctaOfficial.textContent = I18n.t('goOfficialDirect');

    // Related
    const related = products.filter(p => p.category === product.category && p.id !== product.id && p.status === 'active').slice(0, 4);
    document.getElementById('relatedGrid').innerHTML = related.map(p => createProductCard(p, false)).join('');
    document.getElementById('relatedTitle').textContent = I18n.t('relatedTools');

    loading.style.display = 'none';
    content.style.display = 'block';
  }

  // ===== Affiliate Click Tracking =====
  window.trackClick = function (productId) {
    try {
      const clicks = JSON.parse(localStorage.getItem('affiliateClicks') || '{}');
      clicks[productId] = (clicks[productId] || 0) + 1;
      clicks._total = (clicks._total || 0) + 1;
      localStorage.setItem('affiliateClicks', JSON.stringify(clicks));
      if (typeof gtag === 'function') {
        gtag('event', 'affiliate_click', { product_id: productId });
      }
    } catch (e) { /* ignore */ }
  };

  // ===== Helpers =====
  function getCategoryName(catId) {
    const cat = config.categories?.find(c => c.id === catId);
    if (!cat) return catId;
    if (I18n.getLang() === 'en') return cat.nameEn || cat.name;
    return cat.name;
  }

  function escapeHtml(str) {
    if (!str) return '';
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  function debounce(fn, ms) {
    let t;
    return function () {
      clearTimeout(t);
      t = setTimeout(fn, ms);
    };
  }

  function showToast(msg) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
  }

  // ===== Blog Highlights =====
  function renderBlogHighlights() {
    const grid = document.getElementById('blogHighlightGrid');
    if (!grid) return;
    const articles = [
      {
        tag: I18n.getLang() === 'en' ? 'VS Comparison' : 'VS 比較',
        title: I18n.getLang() === 'en' ? 'NordVPN vs ExpressVPN – Which VPN Should You Choose?' : 'NordVPN vs ExpressVPN 徹底比較｜どっちを選ぶべき？',
        excerpt: I18n.getLang() === 'en' ? 'A detailed comparison of the two most popular VPNs. Speed, security, pricing, and features compared side by side.' : '人気VPN2社を速度・セキュリティ・料金・機能で徹底比較。あなたに最適なVPNがわかります。',
        meta: I18n.getLang() === 'en' ? 'VS Comparison | 2026-03' : 'VS比較 | 2026-03',
        url: 'blog/nordvpn-vs-expressvpn.html'
      },
      {
        tag: I18n.getLang() === 'en' ? 'AI Tools' : 'AIツール',
        title: I18n.getLang() === 'en' ? 'Claude Pro vs ChatGPT Plus – AI Tool Comparison 2026' : 'Claude Pro vs ChatGPT Plus｜AIツール徹底比較【2026年版】',
        excerpt: I18n.getLang() === 'en' ? 'Comparing the latest AI assistants. Features, pricing, and use cases to help you choose the right one.' : '最新AIアシスタントを機能・料金・活用シーンで比較。あなたに合ったAIツールが見つかります。',
        meta: I18n.getLang() === 'en' ? 'VS Comparison | 2026-03' : 'VS比較 | 2026-03',
        url: 'blog/claude-pro-vs-chatgpt-plus.html'
      },
      {
        tag: I18n.getLang() === 'en' ? 'Hosting' : 'サーバー',
        title: I18n.getLang() === 'en' ? 'Xserver vs ConoHa WING – Best Japanese Web Hosting' : 'エックスサーバー vs ConoHa WING｜レンタルサーバー比較',
        excerpt: I18n.getLang() === 'en' ? 'Japan\'s top two web hosting services compared. Speed, pricing, WordPress support and more.' : '日本の人気レンタルサーバー2社を速度・料金・WordPress対応で比較。',
        meta: I18n.getLang() === 'en' ? 'VS Comparison | 2026-03' : 'VS比較 | 2026-03',
        url: 'blog/xserver-vs-conoha-wing.html'
      }
    ];
    grid.innerHTML = articles.map(a => `
      <a href="${a.url}" class="blog-highlight-card">
        <span class="blog-highlight-tag">${a.tag}</span>
        <span class="blog-highlight-title">${a.title}</span>
        <p class="blog-highlight-excerpt">${a.excerpt}</p>
        <span class="blog-highlight-meta">${a.meta}</span>
      </a>
    `).join('');
  }

  function initBackToTop() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;
    window.addEventListener('scroll', () => {
      btn.classList.toggle('visible', window.scrollY > 400);
    });
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // ===== Quiz / Tool Finder =====
  const quizCategoryMap = {
    website: ['server', 'domain', 'sitebuilder'],
    security: ['vpn', 'security', 'password'],
    learning: ['learning'],
    content: ['design', 'video', 'photo', 'writing'],
    ai: ['ai'],
    business: ['ecommerce', 'project', 'accounting', 'marketing', 'communication'],
    cloud: ['cloud'],
    seo: ['seo'],
  };

  let quizState = { step: 0, q1: null, q2: null, q3: null };

  function initQuiz() {
    const startBtn = document.getElementById('quizStartBtn');
    const overlay = document.getElementById('quizOverlay');
    const closeBtn = document.getElementById('quizClose');
    if (!startBtn || !overlay) return;

    startBtn.addEventListener('click', () => {
      quizState = { step: 1, q1: null, q2: null, q3: null };
      overlay.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      renderQuizStep();
    });

    closeBtn.addEventListener('click', closeQuiz);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeQuiz();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && overlay.style.display === 'flex') closeQuiz();
    });
  }

  function closeQuiz() {
    const overlay = document.getElementById('quizOverlay');
    overlay.style.display = 'none';
    document.body.style.overflow = '';
  }

  function renderQuizProgress() {
    const container = document.getElementById('quizProgress');
    const labels = ['Q1', 'Q2', 'Q3', '✓'];
    container.innerHTML = labels.map((_, i) => {
      const stepNum = i + 1;
      let cls = 'quiz-dot';
      if (stepNum < quizState.step) cls += ' done';
      else if (stepNum === quizState.step) cls += ' active';
      return `<div class="${cls}"></div>`;
    }).join('');
  }

  function renderQuizStep() {
    renderQuizProgress();
    const content = document.getElementById('quizContent');
    if (quizState.step === 1) renderQ1(content);
    else if (quizState.step === 2) renderQ2(content);
    else if (quizState.step === 3) renderQ3(content);
    else if (quizState.step === 4) renderQuizResults(content);
  }

  function renderQ1(el) {
    const keys = ['quizQ1a','quizQ1b','quizQ1c','quizQ1d','quizQ1e','quizQ1f','quizQ1g','quizQ1h'];
    const values = ['website','security','learning','content','ai','business','cloud','seo'];
    el.innerHTML = `<h2>${I18n.t('quizQ1')}</h2>
      <div class="quiz-options">${keys.map((k, i) =>
        `<button class="quiz-option" data-value="${values[i]}">${I18n.t(k)}</button>`
      ).join('')}</div>`;
    el.querySelectorAll('.quiz-option').forEach(btn => {
      btn.addEventListener('click', () => {
        quizState.q1 = btn.dataset.value;
        quizState.step = 2;
        renderQuizStep();
      });
    });
  }

  function renderQ2(el) {
    const keys = ['quizQ2a','quizQ2b','quizQ2c'];
    const values = ['free','low','any'];
    el.innerHTML = `<h2>${I18n.t('quizQ2')}</h2>
      <div class="quiz-options">${keys.map((k, i) =>
        `<button class="quiz-option" data-value="${values[i]}">${I18n.t(k)}</button>`
      ).join('')}</div>
      <button class="quiz-back" id="quizBackBtn">${I18n.t('quizBack')}</button>`;
    el.querySelectorAll('.quiz-option').forEach(btn => {
      btn.addEventListener('click', () => {
        quizState.q2 = btn.dataset.value;
        quizState.step = 3;
        renderQuizStep();
      });
    });
    document.getElementById('quizBackBtn').addEventListener('click', () => {
      quizState.step = 1;
      renderQuizStep();
    });
  }

  function renderQ3(el) {
    const keys = ['quizQ3a','quizQ3b','quizQ3c'];
    const values = ['beginner','intermediate','advanced'];
    el.innerHTML = `<h2>${I18n.t('quizQ3')}</h2>
      <div class="quiz-options">${keys.map((k, i) =>
        `<button class="quiz-option" data-value="${values[i]}">${I18n.t(k)}</button>`
      ).join('')}</div>
      <button class="quiz-back" id="quizBackBtn">${I18n.t('quizBack')}</button>`;
    el.querySelectorAll('.quiz-option').forEach(btn => {
      btn.addEventListener('click', () => {
        quizState.q3 = btn.dataset.value;
        quizState.step = 4;
        renderQuizStep();
      });
    });
    document.getElementById('quizBackBtn').addEventListener('click', () => {
      quizState.step = 2;
      renderQuizStep();
    });
  }

  function parseMonthlyPrice(priceStr) {
    if (!priceStr) return Infinity;
    if (/^無料$/.test(priceStr) || /^無料（/.test(priceStr) || /^決済手数料/.test(priceStr)) return 0;
    if (priceStr.startsWith('無料')) return 0;
    const buyout = /買い切り/.test(priceStr);
    const yearly = /\/年/.test(priceStr);
    const match = priceStr.match(/([\d,]+(?:\.\d+)?)/);
    if (!match) return Infinity;
    let num = parseFloat(match[1].replace(/,/g, ''));
    if (priceStr.includes('$') || priceStr.includes('€')) num *= 150;
    if (buyout) num = num / 24;
    else if (yearly) num = num / 12;
    return num;
  }

  function scoreProducts(filtered) {
    return filtered.map(p => {
      let score = 0;
      const monthly = parseMonthlyPrice(p.price);

      // Q2: Budget
      if (quizState.q2 === 'free') {
        if (monthly === 0) score += 10;
        else if (monthly <= 1000) score += 4;
        else if (monthly <= 2000) score += 1;
      } else if (quizState.q2 === 'low') {
        if (monthly > 0 && monthly <= 2000) score += 10;
        else if (monthly === 0) score += 6;
        else if (monthly <= 5000) score += 2;
      }
      // 'any' → no budget filter

      // Q3: Experience level
      if (quizState.q3 === 'beginner') {
        if (p.featured) score += 5;
        score += Math.round(p.rating * 2);
      } else if (quizState.q3 === 'intermediate') {
        score += Math.round(p.rating * 1.5);
        if (p.features) score += Math.min(p.features.length, 4);
      } else if (quizState.q3 === 'advanced') {
        score += Math.round(p.rating);
        if (p.features) score += Math.min(p.features.length * 2, 10);
      }

      // Affiliate bonus
      if (p.affiliateUrl) score += 1;

      return { product: p, score };
    }).sort((a, b) => b.score - a.score);
  }

  function renderQuizResults(el) {
    const cats = quizCategoryMap[quizState.q1] || [];
    const filtered = products.filter(p => p.status === 'active' && cats.includes(p.category));
    const scored = scoreProducts(filtered);
    const top5 = scored.slice(0, 5);

    let html = `<h2 class="quiz-results-title">${I18n.t('quizResultTitle')}</h2>`;
    if (top5.length === 0) {
      html += `<p class="quiz-no-result">${I18n.t('quizNoResult')}</p>`;
    } else {
      html += '<div class="quiz-results-grid">' +
        top5.map(s => createProductCard(s.product, false)).join('') +
        '</div>';
    }
    html += `<button class="quiz-retry" id="quizRetryBtn">${I18n.t('quizRetry')}</button>`;
    el.innerHTML = html;

    document.getElementById('quizRetryBtn').addEventListener('click', () => {
      quizState = { step: 1, q1: null, q2: null, q3: null };
      renderQuizStep();
    });
  }

  // Re-render quiz on language change
  window.addEventListener('langchange', () => {
    const overlay = document.getElementById('quizOverlay');
    if (overlay && overlay.style.display === 'flex') {
      renderQuizStep();
    }
  });

  // Header scroll effect
  window.addEventListener('scroll', function() {
    var header = document.querySelector('.site-header');
    if (header) {
      header.classList.toggle('scrolled', window.scrollY > 50);
    }
  }, { passive: true });

  // IntersectionObserver for fade-in animations
  var fadeObserver = null;
  if (typeof IntersectionObserver !== 'undefined') {
    fadeObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          fadeObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
  }

  // ===== Start =====
  document.addEventListener('DOMContentLoaded', init);
})();
