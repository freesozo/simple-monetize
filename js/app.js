(function () {
  'use strict';

  let products = [];
  let config = {};
  let currentCategory = 'all';

  // ===== Init =====
  async function init() {
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
  }

  // ===== Index Page =====
  function initIndexPage() {
    renderCategories();
    renderFeatured();
    renderProducts(products);
    initSearch();
  }

  function renderCategories() {
    const grid = document.getElementById('categoryGrid');
    if (!grid) return;
    config.categories.forEach(cat => {
      const btn = document.createElement('button');
      btn.className = 'category-btn';
      btn.dataset.category = cat.id;
      btn.textContent = cat.icon + ' ' + cat.name;
      btn.addEventListener('click', () => {
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = cat.id;
        filterProducts();
      });
      grid.appendChild(btn);
    });
    // "all" button handler
    grid.querySelector('[data-category="all"]').addEventListener('click', () => {
      document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
      grid.querySelector('[data-category="all"]').classList.add('active');
      currentCategory = 'all';
      filterProducts();
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

  function renderProducts(list) {
    const grid = document.getElementById('productGrid');
    const noResults = document.getElementById('noResults');
    if (!grid) return;
    const active = list.filter(p => p.status === 'active');
    if (active.length === 0) {
      grid.innerHTML = '';
      noResults.style.display = 'block';
      return;
    }
    noResults.style.display = 'none';
    grid.innerHTML = active.map(p => createProductCard(p, false)).join('');
  }

  function createProductCard(product, isFeatured) {
    const catName = getCategoryName(product.category);
    const stars = '★'.repeat(Math.floor(product.rating)) + (product.rating % 1 >= 0.5 ? '☆' : '');
    const featuredClass = (isFeatured || product.featured) ? ' featured' : '';
    const affiliateLink = product.affiliateUrl || product.officialUrl;
    return `
      <div class="product-card${featuredClass}">
        <div class="card-body">
          <span class="card-category">${catName}</span>
          <h3 class="card-title">${escapeHtml(product.name)}</h3>
          <p class="card-summary">${escapeHtml(product.summary)}</p>
          <div class="card-meta">
            <span class="card-rating">${stars} ${product.rating}</span>
            <span class="card-price">${escapeHtml(product.price)}</span>
          </div>
          <div class="card-actions">
            <a href="review.html?id=${product.id}" class="btn btn-outline">詳細を見る</a>
            <a href="${escapeHtml(affiliateLink)}" class="btn btn-primary" target="_blank" rel="noopener noreferrer nofollow" onclick="trackClick('${product.id}')">公式サイト →</a>
          </div>
        </div>
      </div>`;
  }

  function filterProducts() {
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
    renderProducts(filtered);
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
      loading.innerHTML = '<p>ツールが見つかりませんでした。<br><a href="index.html">← ホームに戻る</a></p>';
      return;
    }

    // Update meta
    document.title = product.name + ' レビュー｜おすすめツール比較ナビ';
    const pageUrl = 'https://tools.freesozo.com/review.html?id=' + product.id;
    const metaDesc = product.name + 'を徹底レビュー。' + product.summary;
    document.querySelector('meta[name="description"]')?.setAttribute('content', metaDesc);
    document.querySelector('meta[property="og:title"]')?.setAttribute('content', product.name + ' レビュー');
    document.querySelector('meta[property="og:description"]')?.setAttribute('content', metaDesc);
    document.querySelector('meta[property="og:url"]')?.setAttribute('content', pageUrl);
    document.querySelector('link[rel="canonical"]')?.setAttribute('href', pageUrl);
    // JSON-LD Product structured data
    const jsonLd = document.createElement('script');
    jsonLd.type = 'application/ld+json';
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
    // BreadcrumbList
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
    const catName = getCategoryName(product.category);
    const stars = '★'.repeat(Math.floor(product.rating)) + (product.rating % 1 >= 0.5 ? '☆' : '');

    // Breadcrumb
    document.getElementById('breadcrumbCategory').textContent = catName;
    document.getElementById('breadcrumbName').textContent = product.name;

    // Header
    document.getElementById('reviewTitle').textContent = product.name;
    document.getElementById('reviewRating').textContent = stars + ' ' + product.rating;
    document.getElementById('reviewPrice').textContent = product.price;

    // Description
    document.getElementById('reviewDescription').innerHTML = '<p>' + escapeHtml(product.description) + '</p>';

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
    document.getElementById('ctaTitle').textContent = product.name + ' を試す';
    const ctaBtn = document.getElementById('ctaAffiliate');
    ctaBtn.href = affiliateLink;
    ctaBtn.addEventListener('click', () => trackClick(product.id));
    document.getElementById('ctaOfficial').href = product.officialUrl;

    // Related
    const related = products.filter(p => p.category === product.category && p.id !== product.id && p.status === 'active');
    document.getElementById('relatedGrid').innerHTML = related.map(p => createProductCard(p, false)).join('');

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
      // GA event
      if (typeof gtag === 'function') {
        gtag('event', 'affiliate_click', { product_id: productId });
      }
    } catch (e) { /* ignore */ }
  };

  // ===== Helpers =====
  function getCategoryName(catId) {
    const cat = config.categories?.find(c => c.id === catId);
    return cat ? cat.name : catId;
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
