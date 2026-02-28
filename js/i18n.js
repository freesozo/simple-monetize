// i18n.js – 日英切替モジュール（ツール比較ナビ）
const I18n = (() => {
  const dict = {
    ja: {
      siteTitle: 'ツール比較ナビ',
      heroHeading: 'あなたに最適なツールが見つかる',
      heroSub: '人気のレンタルサーバー、VPN、学習サービス、AIツールなどを徹底比較。実際のユーザー視点でおすすめをご紹介します。',
      searchPlaceholder: 'ツール名やキーワードで検索...',
      navHome: 'ホーム',
      navCategory: 'カテゴリ',
      navAll: '全ツール',
      categoryAll: 'すべて',
      featuredHeading: '★ 特におすすめ',
      allToolsHeading: '全ツール一覧',
      noResults: '該当するツールが見つかりませんでした。',
      viewDetail: '詳細を見る',
      visitOfficial: '公式サイト →',
      // Review page
      loading: '読み込み中...',
      notFound: 'ツールが見つかりませんでした。',
      backHome: '← ホームに戻る',
      recommended: 'おすすめ',
      merit: 'メリット',
      demerit: 'デメリット',
      features: '主な機能・特徴',
      tryTool: 'を試す',
      checkOfficial: 'まずは公式サイトで詳細をチェック',
      goOfficial: '公式サイトを見る →',
      goOfficialDirect: '公式サイト（直接）',
      relatedTools: '関連ツール',
      // Breadcrumb
      breadcrumbHome: 'ホーム',
      // Footer
      footerHome: 'ホーム',
      footerPrivacy: 'プライバシーポリシー',
      footerSister: '姉妹サイト:',
      footerSisterName: 'フリー素材ポータル',
      footerAffiliate: '※ 当サイトはアフィリエイトプログラムに参加しています。',
      footerCopyright: '© 2026 おすすめツール比較ナビ',
      // Ad
      adSlot: '広告スペース',
      // Sort
      sortRating: '評価順',
      sortName: '名前順',
      // Favorites
      favOnly: '❤️ お気に入りのみ',
      favAdd: 'お気に入りに追加',
      favRemove: 'お気に入りから削除',
      // Theme
      lang: '🌐 English',
    },
    en: {
      siteTitle: 'Tool Compare Navi',
      heroHeading: 'Find the perfect tool for you',
      heroSub: 'Compare popular web hosting, VPN, learning platforms, AI tools and more. Honest recommendations from a real user perspective.',
      searchPlaceholder: 'Search by tool name or keyword...',
      navHome: 'Home',
      navCategory: 'Categories',
      navAll: 'All Tools',
      categoryAll: 'All',
      featuredHeading: '★ Top Picks',
      allToolsHeading: 'All Tools',
      noResults: 'No matching tools found.',
      viewDetail: 'Details',
      visitOfficial: 'Official Site →',
      // Review page
      loading: 'Loading...',
      notFound: 'Tool not found.',
      backHome: '← Back to Home',
      recommended: 'Recommended',
      merit: 'Pros',
      demerit: 'Cons',
      features: 'Key Features',
      tryTool: ' – Try it',
      checkOfficial: 'Check the official site for details',
      goOfficial: 'Visit Official Site →',
      goOfficialDirect: 'Official Site (Direct)',
      relatedTools: 'Related Tools',
      // Breadcrumb
      breadcrumbHome: 'Home',
      // Footer
      footerHome: 'Home',
      footerPrivacy: 'Privacy Policy',
      footerSister: 'Sister site:',
      footerSisterName: 'Free Asset Portal',
      footerAffiliate: '* This site participates in affiliate programs.',
      footerCopyright: '© 2026 Tool Compare Navi',
      // Ad
      adSlot: 'Ad Space',
      // Sort
      sortRating: 'By Rating',
      sortName: 'By Name',
      // Favorites
      favOnly: '❤️ Favorites Only',
      favAdd: 'Add to favorites',
      favRemove: 'Remove from favorites',
      // Theme
      lang: '🌐 日本語',
    }
  };

  let current = localStorage.getItem('lang') || 'ja';

  function getLang() { return current; }

  function setLang(lang) {
    current = lang;
    localStorage.setItem('lang', lang);
    document.documentElement.lang = lang;
    applyAll();
  }

  function t(key) {
    return (dict[current] && dict[current][key]) || key;
  }

  function toggle() {
    setLang(current === 'ja' ? 'en' : 'ja');
  }

  function applyAll() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = t(key);
      } else {
        el.textContent = t(key);
      }
    });
    window.dispatchEvent(new CustomEvent('langchange', { detail: { lang: current } }));
  }

  document.documentElement.lang = current;

  return { getLang, setLang, t, toggle, applyAll };
})();
