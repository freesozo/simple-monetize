(function() {
  'use strict';

  // ── Tool Plans Data ──
  // Product IDs match data/products.json exactly
  const TOOL_PLANS = {
    server: [
      { id: 'lolipop', name: 'ロリポップ!', nameEn: 'Lolipop!', plan: 'ハイスピード', planEn: 'Hi-Speed', monthlyPrice: 550, performance: 3, features: ['WordPress対応', 'SSD 400GB'], featuresEn: ['WordPress Ready', 'SSD 400GB'] },
      { id: 'colorfulbox', name: 'カラフルボックス', nameEn: 'ColorfulBox', plan: 'BOX2', planEn: 'BOX2', monthlyPrice: 968, performance: 4, features: ['LiteSpeed', '自動バックアップ'], featuresEn: ['LiteSpeed', 'Auto Backup'] },
      { id: 'xserver', name: 'エックスサーバー', nameEn: 'Xserver', plan: 'スタンダード', planEn: 'Standard', monthlyPrice: 1100, performance: 5, features: ['安定性No.1', 'サポート充実'], featuresEn: ['Top Stability', 'Great Support'] },
      { id: 'conoha-wing', name: 'ConoHa WING', nameEn: 'ConoHa WING', plan: 'ベーシック', planEn: 'Basic', monthlyPrice: 1320, performance: 5, features: ['国内最速級', 'ドメイン無料'], featuresEn: ['Fastest in JP', 'Free Domain'] }
    ],
    vpn: [
      { id: 'surfshark', name: 'Surfshark', nameEn: 'Surfshark', plan: '2年プラン', planEn: '2-Year Plan', monthlyPrice: 328, performance: 4, features: ['デバイス無制限', 'コスパ最強'], featuresEn: ['Unlimited Devices', 'Best Value'] },
      { id: 'millenvpn', name: 'MillenVPN', nameEn: 'MillenVPN', plan: '2年プラン', planEn: '2-Year Plan', monthlyPrice: 396, performance: 4, features: ['日本企業運営', 'ノーログ'], featuresEn: ['Japanese Company', 'No-Log'] },
      { id: 'nordvpn', name: 'NordVPN', nameEn: 'NordVPN', plan: '2年プラン', planEn: '2-Year Plan', monthlyPrice: 640, performance: 5, features: ['世界最大級', '60カ国対応'], featuresEn: ['World\'s Largest', '60 Countries'] }
    ],
    ai: [
      { id: 'gemini-advanced', name: 'Gemini', nameEn: 'Gemini', plan: 'Advanced', planEn: 'Advanced', monthlyPrice: 2900, performance: 4, features: ['Google連携', '長いコンテキスト'], featuresEn: ['Google Integration', 'Long Context'] },
      { id: 'chatgpt-plus', name: 'ChatGPT', nameEn: 'ChatGPT', plan: 'Plus', planEn: 'Plus', monthlyPrice: 3000, performance: 5, features: ['GPT-4o', '画像生成'], featuresEn: ['GPT-4o', 'Image Generation'] },
      { id: 'claude-pro', name: 'Claude', nameEn: 'Claude', plan: 'Pro', planEn: 'Pro', monthlyPrice: 3000, performance: 5, features: ['長文対応', 'コーディング'], featuresEn: ['Long Text', 'Coding'] }
    ],
    design: [
      { id: 'canva-pro', name: 'Canva', nameEn: 'Canva', plan: 'Pro', planEn: 'Pro', monthlyPrice: 1500, performance: 5, features: ['テンプレート豊富', 'チーム共有'], featuresEn: ['Rich Templates', 'Team Sharing'] },
      { id: 'figma', name: 'Figma', nameEn: 'Figma', plan: 'Professional', planEn: 'Professional', monthlyPrice: 1800, performance: 5, features: ['UI/UXデザイン', '共同編集'], featuresEn: ['UI/UX Design', 'Collaboration'] }
    ],
    learning: [
      { id: 'schoo', name: 'Schoo', nameEn: 'Schoo', plan: 'プレミアム', planEn: 'Premium', monthlyPrice: 980, performance: 3, features: ['生放送無料', '日本語コンテンツ'], featuresEn: ['Free Live Classes', 'Japanese Content'] },
      { id: 'udemy', name: 'Udemy', nameEn: 'Udemy', plan: '個別購入', planEn: 'Per Course', monthlyPrice: 1500, performance: 4, features: ['セール時90%OFF', '買い切り'], featuresEn: ['90% OFF Sales', 'One-time Purchase'] }
    ]
  };

  const CATEGORY_LABELS = {
    ja: { server: 'レンタルサーバー', vpn: 'VPN', ai: 'AIツール', design: 'デザインツール', learning: '学習サービス' },
    en: { server: 'Web Hosting', vpn: 'VPN', ai: 'AI Tools', design: 'Design Tools', learning: 'Learning' }
  };

  const PLAN_LABELS = {
    ja: [
      { label: 'コスパ最強プラン', tag: '最安' },
      { label: 'バランスプラン', tag: 'おすすめ' },
      { label: 'ハイスペックプラン', tag: '高性能' }
    ],
    en: [
      { label: 'Best Value Plan', tag: 'Cheapest' },
      { label: 'Balanced Plan', tag: 'Recommended' },
      { label: 'High-Spec Plan', tag: 'Top Tier' }
    ]
  };

  function getLang() {
    return (typeof I18n !== 'undefined' && I18n.getLang) ? I18n.getLang() : 'ja';
  }

  function simulate() {
    var budget = parseInt(document.getElementById('budgetInput').value) || 0;
    var selectedCats = [];
    var checkboxes = document.querySelectorAll('#simCategories input:checked');
    for (var i = 0; i < checkboxes.length; i++) {
      selectedCats.push(checkboxes[i].value);
    }
    var priorityEl = document.querySelector('#simPriority input:checked');
    var priority = priorityEl ? priorityEl.value : 'balance';
    var lang = getLang();

    if (selectedCats.length === 0) {
      alert(lang === 'en' ? 'Please select at least one category.' : '最低1つのカテゴリを選択してください');
      return;
    }

    // Sort each category by priority
    var sortedPlans = {};
    for (var c = 0; c < selectedCats.length; c++) {
      var cat = selectedCats[c];
      var plans = (TOOL_PLANS[cat] || []).slice();
      if (priority === 'cost') {
        plans.sort(function(a, b) { return a.monthlyPrice - b.monthlyPrice; });
      } else if (priority === 'performance') {
        plans.sort(function(a, b) { return b.performance - a.performance || a.monthlyPrice - b.monthlyPrice; });
      } else {
        // balance: performance per yen
        plans.sort(function(a, b) { return (b.performance / b.monthlyPrice) - (a.performance / a.monthlyPrice); });
      }
      sortedPlans[cat] = plans;
    }

    var combos = generateCombos(sortedPlans, selectedCats, budget);
    renderResults(combos, budget, selectedCats, lang);

    // Track in GA
    if (typeof gtag === 'function') {
      gtag('event', 'simulate', {
        event_category: 'simulator',
        event_label: selectedCats.join(','),
        value: budget
      });
    }
  }

  function generateCombos(sortedPlans, categories, budget) {
    var results = [];

    // Plan 1: Cheapest per category (index 0 after cost sort)
    var cheapPlan = [];
    for (var i = 0; i < categories.length; i++) {
      var arr = sortedPlans[categories[i]];
      if (arr && arr[0]) cheapPlan.push({ cat: categories[i], tool: arr[0] });
    }
    var cheapTotal = 0;
    for (var j = 0; j < cheapPlan.length; j++) cheapTotal += cheapPlan[j].tool.monthlyPrice;
    if (cheapPlan.length === categories.length) {
      results.push({ planIndex: 0, items: cheapPlan, total: cheapTotal, withinBudget: cheapTotal <= budget });
    }

    // Plan 2: Mid-range (2nd option if available, else 1st)
    var midPlan = [];
    for (var i = 0; i < categories.length; i++) {
      var arr = sortedPlans[categories[i]];
      var pick = (arr && arr[1]) ? arr[1] : (arr ? arr[0] : null);
      if (pick) midPlan.push({ cat: categories[i], tool: pick });
    }
    var midTotal = 0;
    for (var j = 0; j < midPlan.length; j++) midTotal += midPlan[j].tool.monthlyPrice;
    if (midPlan.length === categories.length && midTotal !== cheapTotal) {
      results.push({ planIndex: 1, items: midPlan, total: midTotal, withinBudget: midTotal <= budget });
    }

    // Plan 3: Premium (last = most expensive/best perf)
    var premPlan = [];
    for (var i = 0; i < categories.length; i++) {
      var arr = sortedPlans[categories[i]];
      var pick = arr ? arr[arr.length - 1] : null;
      if (pick) premPlan.push({ cat: categories[i], tool: pick });
    }
    var premTotal = 0;
    for (var j = 0; j < premPlan.length; j++) premTotal += premPlan[j].tool.monthlyPrice;
    if (premPlan.length === categories.length && premTotal !== midTotal && premTotal !== cheapTotal) {
      results.push({ planIndex: 2, items: premPlan, total: premTotal, withinBudget: premTotal <= budget });
    }

    return results;
  }

  function renderResults(combos, budget, categories, lang) {
    var container = document.getElementById('simulatorResults');
    container.style.display = '';

    if (combos.length === 0) {
      container.innerHTML = '<p class="sim-no-result">' +
        (lang === 'en' ? 'No matching tools found for the selected categories.' : '選択されたカテゴリにマッチするツールが見つかりませんでした。') +
        '</p>';
      return;
    }

    var catLabels = CATEGORY_LABELS[lang] || CATEGORY_LABELS.ja;
    var planLabels = PLAN_LABELS[lang] || PLAN_LABELS.ja;

    var html = '<h2>' + (lang === 'en' ? 'Recommended Combinations' : 'あなたにおすすめの組み合わせ') + '</h2>';
    html += '<p class="sim-budget-label">' + (lang === 'en' ? 'Budget: ' : '予算: ') + '&yen;' + budget.toLocaleString() + (lang === 'en' ? '/mo' : '/月') + '</p>';

    for (var c = 0; c < combos.length; c++) {
      var combo = combos[c];
      var pl = planLabels[combo.planIndex] || planLabels[0];
      var budgetClass = combo.withinBudget ? 'within-budget' : 'over-budget';
      var budgetBadge = combo.withinBudget
        ? (lang === 'en' ? 'Within Budget' : '予算内')
        : (lang === 'en' ? 'Over Budget' : '予算超過');
      var badgeIcon = combo.withinBudget ? '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>' : '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';

      var diff = combo.total - budget;
      var diffStr = '';
      if (combo.withinBudget) {
        diffStr = '<span class="sim-diff sim-diff-under">' + (lang === 'en' ? 'Save ' : '') + '&yen;' + Math.abs(diff).toLocaleString() + (lang === 'en' ? ' left' : ' 余り') + '</span>';
      } else {
        diffStr = '<span class="sim-diff sim-diff-over">' + (lang === 'en' ? '' : '') + '+&yen;' + diff.toLocaleString() + (lang === 'en' ? ' over' : ' 超過') + '</span>';
      }

      html += '<div class="sim-plan ' + budgetClass + '">';
      html += '<div class="sim-plan-header">';
      html += '<span class="sim-plan-tag">' + pl.tag + '</span>';
      html += '<h3>' + pl.label + '</h3>';
      html += '<span class="sim-plan-total">' + (lang === 'en' ? '' : '月額 ') + '&yen;' + combo.total.toLocaleString() + (lang === 'en' ? '/mo' : '') + '</span>';
      html += diffStr;
      html += '<span class="sim-budget-badge ' + budgetClass + '">' + badgeIcon + ' ' + budgetBadge + '</span>';
      html += '</div>';
      html += '<div class="sim-plan-items">';

      for (var i = 0; i < combo.items.length; i++) {
        var item = combo.items[i];
        var tool = item.tool;
        var toolName = lang === 'en' ? tool.nameEn : tool.name;
        var toolPlan = lang === 'en' ? tool.planEn : tool.plan;
        var toolFeatures = lang === 'en' ? tool.featuresEn : tool.features;
        var catLabel = catLabels[item.cat] || item.cat;
        var detailLabel = lang === 'en' ? 'Details' : '詳しく見る';

        html += '<div class="sim-plan-item">';
        html += '<div class="sim-item-cat">' + catLabel + '</div>';
        html += '<div class="sim-item-info">';
        html += '<strong>' + toolName + '</strong>';
        html += '<span class="sim-item-plan">' + toolPlan + '</span>';
        html += '<span class="sim-item-price">&yen;' + tool.monthlyPrice.toLocaleString() + (lang === 'en' ? '/mo' : '/月') + '</span>';
        html += '</div>';
        html += '<div class="sim-item-features">';
        for (var f = 0; f < toolFeatures.length; f++) {
          html += '<span class="sim-feature">' + toolFeatures[f] + '</span>';
        }
        html += '</div>';
        html += '<a href="tool/' + tool.id + '.html" class="sim-item-link">' + detailLabel + ' &rarr;</a>';
        html += '</div>';
      }

      html += '</div></div>';
    }

    html += '<div class="sim-actions">';
    html += '<button class="btn-simulate-again" id="simAgainBtn">' + (lang === 'en' ? 'Try Again' : 'もう一度シミュレーション') + '</button>';
    html += '</div>';

    container.innerHTML = html;

    // Scroll to results
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });

    document.getElementById('simAgainBtn').addEventListener('click', function() {
      container.style.display = 'none';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── Init ──
  document.addEventListener('DOMContentLoaded', function() {
    // Simulate button
    document.getElementById('simulateBtn').addEventListener('click', simulate);

    // Enter key on budget input
    document.getElementById('budgetInput').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') simulate();
    });

    // Budget presets
    var presets = document.querySelectorAll('.budget-preset');
    for (var i = 0; i < presets.length; i++) {
      presets[i].addEventListener('click', function() {
        document.getElementById('budgetInput').value = this.getAttribute('data-amount');
        // Remove active from all, add to clicked
        for (var j = 0; j < presets.length; j++) presets[j].classList.remove('active');
        this.classList.add('active');
      });
    }
    // Mark default preset active
    var defaultPreset = document.querySelector('.budget-preset[data-amount="3000"]');
    if (defaultPreset) defaultPreset.classList.add('active');

    // Checkbox visual toggle
    var catChecks = document.querySelectorAll('.sim-cat-check input');
    for (var i = 0; i < catChecks.length; i++) {
      catChecks[i].addEventListener('change', function() {
        this.parentElement.classList.toggle('checked', this.checked);
      });
      // Init state
      if (catChecks[i].checked) catChecks[i].parentElement.classList.add('checked');
    }

    // Radio visual toggle
    var radioInputs = document.querySelectorAll('.sim-radio input');
    for (var i = 0; i < radioInputs.length; i++) {
      radioInputs[i].addEventListener('change', function() {
        var radios = document.querySelectorAll('.sim-radio');
        for (var j = 0; j < radios.length; j++) radios[j].classList.remove('checked');
        this.parentElement.classList.add('checked');
      });
      if (radioInputs[i].checked) radioInputs[i].parentElement.classList.add('checked');
    }

    // Theme toggle
    var themeBtn = document.getElementById('themeBtn');
    if (themeBtn) {
      themeBtn.addEventListener('click', function() {
        var html = document.documentElement;
        var next = html.dataset.theme === 'dark' ? 'light' : 'dark';
        html.dataset.theme = next;
        localStorage.setItem('theme', next);
      });
    }

    // Language toggle
    var langBtn = document.getElementById('langBtn');
    if (langBtn && typeof I18n !== 'undefined') {
      langBtn.addEventListener('click', function() {
        I18n.toggle();
      });
    }

    // Back to top
    var backToTop = document.getElementById('backToTop');
    if (backToTop) {
      window.addEventListener('scroll', function() {
        backToTop.style.display = window.scrollY > 300 ? 'block' : 'none';
      });
      backToTop.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    // i18n apply
    if (typeof I18n !== 'undefined' && I18n.applyAll) {
      I18n.applyAll();
    }
  });
})();
