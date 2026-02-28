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
        renderFeatured();
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

    try {
      const [prodRes, confRes] = await Promise.all([
        fetch('data/products.json'),
        fetch('data/config.json')
      ]);
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
    filterProducts();
  }
  window.toggleFav = toggleFav;

  // ===== Index Page =====
  function initIndexPage() {
    renderCategories();
    renderSortBar();
    renderFeatured();
    filterProducts();
    initSearch();
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
      btn.textContent = cat.icon + ' ' + catName;
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
    const featured = products.filter(p => p.featured && p.status === 'active');
    if (featured.length === 0) {
      document.getElementById('featuredTitle').style.display = 'none';
      grid.style.display = 'none';
      return;
    }
    grid.innerHTML = featured.map(p => createProductCard(p, true)).join('');
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

  function createProductCard(product, isFeatured) {
    const catName = getCategoryName(product.category);
    const stars = '★'.repeat(Math.floor(product.rating)) + (product.rating % 1 >= 0.5 ? '☆' : '');
    const featuredClass = (isFeatured || product.featured) ? ' featured' : '';
    const affiliateLink = product.affiliateUrl || product.officialUrl;
    const faved = isFav(product.id);
    const favLabel = faved ? I18n.t('favRemove') : I18n.t('favAdd');
    return `
      <div class="product-card${featuredClass}" data-featured-label="${escapeHtml(I18n.getLang() === 'en' ? '★ Top Pick' : '★ おすすめ')}">
        <div class="card-body">
          <div class="card-top-row">
            <span class="card-category">${escapeHtml(catName)}</span>
            <button class="fav-btn${faved ? ' active' : ''}" onclick="toggleFav('${product.id}')" title="${favLabel}">${faved ? '❤️' : '🤍'}</button>
          </div>
          <h3 class="card-title">${escapeHtml(product.name)}</h3>
          <p class="card-summary">${escapeHtml(I18n.getLang() === 'en' ? (product.summaryEn || product.summary) : product.summary)}</p>
          <div class="card-meta">
            <span class="card-rating">${stars} ${product.rating}</span>
            <span class="card-price">${escapeHtml(product.price)}</span>
          </div>
          <div class="card-actions">
            <a href="review.html?id=${product.id}" class="btn btn-outline">${I18n.t('viewDetail')}</a>
            <a href="${escapeHtml(affiliateLink)}" class="btn btn-primary" target="_blank" rel="noopener noreferrer nofollow" onclick="trackClick('${product.id}')">${I18n.t('visitOfficial')}</a>
          </div>
        </div>
      </div>`;
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
    const related = products.filter(p => p.category === product.category && p.id !== product.id && p.status === 'active');
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

  function initBackToTop() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;
    window.addEventListener('scroll', () => {
      btn.classList.toggle('visible', window.scrollY > 400);
    });
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // ===== Start =====
  document.addEventListener('DOMContentLoaded', init);
})();
