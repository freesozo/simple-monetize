// i18n.js – 日英切替モジュール（ツール比較ナビ）
const I18n = (() => {
  const dict = {
    ja: {
      siteTitle: 'ツール比較ナビ',
      heroHeading: 'あなたに最適なツールが見つかる',
      heroSub: '人気のレンタルサーバー、VPN、学習サービス、AIツールなどを徹底比較。実際のユーザー視点でおすすめをご紹介します。',
      heroCta1: 'ツールを探す',
      heroCta2: '無料素材を探す',
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
      // Load more
      loadMore: 'もっと見る',
      // Personalized sections
      recentlyViewed: '最近チェックしたツール',
      favSection: '❤️ お気に入りツール',
      // Theme
      lang: '🌐 English',
      // Quiz
      quizBtn: '🔍 おすすめ診断',
      quizTitle: 'おすすめ診断',
      quizQ1: '何をしたいですか？',
      quizQ1a: '🌐 ウェブサイトを作る',
      quizQ1b: '🔒 セキュリティ',
      quizQ1c: '📚 スキルを学ぶ',
      quizQ1d: '🎨 コンテンツ制作',
      quizQ1e: '🤖 AIツール',
      quizQ1f: '💼 ビジネス運営',
      quizQ1g: '☁️ ファイル管理',
      quizQ1h: '📊 SEO強化',
      quizQ2: '予算は？',
      quizQ2a: '🆓 無料・フリーミアム',
      quizQ2b: '💰 低コスト（月¥2,000以下）',
      quizQ2c: '💎 予算は気にしない',
      quizQ3: '経験レベルは？',
      quizQ3a: '🌱 初心者',
      quizQ3b: '🌿 中級者',
      quizQ3c: '🌳 上級者',
      quizResultTitle: 'あなたにおすすめのツール',
      quizNoResult: '条件に合うツールが見つかりませんでした。',
      quizRetry: 'もう一度診断する',
      quizBack: '← 戻る',
      quizClose: '自分で見つける',
      // Logo
      logoPrefix: 'ツール比較',
      logoSuffix: 'ナビ',
      // Navigation
      navAI: '🤖 AIツール',
      navBlog: 'ブログ',
      // Blog page
      blogIndexTitle: 'ブログ記事一覧',
      blogIndexSub: 'ツールの比較・ランキング・特集記事を公開中。最新情報でお届けします。',
      blogToc: '目次',
      blogVisitOfficial: '公式サイトを見る',
      blogReadReview: '詳細レビューを読む →',
      blogSectionRanking: 'ランキング',
      blogSectionCategory: 'カテゴリ別比較',
      blogSectionFree: '無料ツール特集',
      blogSectionFeature: '特集記事',
      blogSectionVs: 'VS 比較',
      blogConclusion: 'まとめ',
      blogUpdated: '更新日',
      blogProducts: '製品',
      blogProductsCompare: '製品比較',
      blogReadTime: '読了: 約',
      blogMinutes: '分',
      blogArticles: '記事',
      blogMerit: 'メリット',
      blogDemerit: 'デメリット',
      blogFeatures: '主な機能・特徴',
      blogTableTool: 'ツール名',
      blogTablePrice: '料金',
      blogTableRating: '評価',
      blogTableFeatures: '特徴',
      blogTableComparison: '比較項目',
      blogTableRank: '順位',
      blogTableCategory: 'カテゴリ',
      blogRecommendedPoints: 'おすすめポイント',
      blogHowToChoose: 'の選び方',
      blogComparisonTable: '比較一覧表',
      blogOverview: '概要',
      blogComparisonOverview: '比較概要',
      blogSpecTable: 'スペック比較表',
      blogWhichToChoose: 'どちらを選ぶべき？',
      blogFreeHowToChoose: '無料で使える',
      blogFreeIntro: '無料で使える理由と注意点',
      blogFreeComparison: '無料ツール比較一覧',
      blogPaidComparison: '有料版との比較',
      blogRankingOverview: 'ランキング概要',
      blogRankingTable: 'TOP20一覧',
      // Filters
      filterPriceLabel: '料金帯',
      filterPriceAll: 'すべて',
      filterPriceFree: '無料',
      filterPriceLow: '〜¥1,000',
      filterPriceMid: '〜¥5,000',
      filterPriceHigh: '¥5,000〜',
      filterTagLabel: 'タグ',
      filterTagFree: '無料プランあり',
      filterTagJapanese: '日本語対応',
      filterTagAPI: 'API連携可',
      filterTagNoCard: 'カード不要',
      // Shutterstock banner
      ssBannerLabel: '📸 プロ品質の素材をお探しなら',
      ssBannerDesc: '写真・動画・音楽・イラスト3億点以上。ビジネスから個人利用まで対応。',
      ssBannerFeat1: '✅ 商用利用OK',
      ssBannerFeat2: '✅ 日本語サポート',
      ssBannerFeat3: '✅ 定額制プランあり',
      ssBannerCta: '無料トライアルを試す →',
      ssBannerNote: '※ 初月無料プランあり',
      // Sister site banner
      sisterBannerPrefix: '🎨 無料素材を探すなら →',
      sisterBannerName: 'フリー素材ポータル',
      sisterBannerSuffix: '- 200以上の無料素材サイトを比較',
      // AI page
      aiBreadcrumb: '🤖 AIツール比較',
      aiHeroTitle: '🤖 AIツール比較【2026年最新】',
      aiHeroDesc: 'ChatGPT・Claude・Gemini・Midjourney・GitHub Copilotなど、人気のAIツールを料金・機能・無料プランの有無で徹底比較。チャットAI、画像生成、コーディング支援、音声生成など用途別に最適なAIツールが見つかります。',
      aiSearchPlaceholder: 'AIツール名で検索...',
      // Privacy page
      privacyTitle: 'プライバシーポリシー',
      privacyIntro: '当サイト「おすすめツール比較ナビ」（以下「当サイト」、URL: https://tools.freesozo.com/）は、ユーザーのプライバシーを尊重し、個人情報の保護に努めています。本プライバシーポリシーでは、当サイトにおける情報の取り扱いについてご説明いたします。',
      privacyStorageHeading: '1. ローカルストレージの使用について',
      privacyStorageBody: '当サイトでは、より快適にご利用いただくために、お使いのブラウザのローカルストレージ（localStorage）に以下の情報を保存しています。これらの情報はすべてお使いのブラウザ内にのみ保存され、当サイトのサーバーに送信されることはありません。',
      privacyStorageFav: 'お気に入り登録したツールの情報',
      privacyStorageTheme: 'テーマ設定（ダークモード / ライトモード）',
      privacyStorageLang: '言語設定（日本語 / 英語）',
      privacyStorageRecent: '最近チェックしたツールの閲覧履歴',
      privacyStorageAffiliate: 'アフィリエイトリンクのクリック情報（匿名）',
      privacyStorageNote: 'これらのデータはブラウザの設定からいつでも削除することができます。個人を特定できる情報は一切収集しておりません。',
      privacyAnalyticsHeading: '2. アクセス解析について',
      privacyAnalyticsBody: '当サイトでは、Google アナリティクス（GA4）を使用してアクセス状況を把握しています。Google アナリティクスはトラフィックデータの収集のために Cookie を使用しています。このデータは匿名で収集されており、個人を特定するものではありません。この機能はブラウザの設定により Cookie を無効にすることで拒否できます。',
      privacyAnalyticsSeeAlso: '詳しくは',
      privacyAnalyticsSuffix: 'をご確認ください。',
      privacyGoogleLink: 'Google のプライバシーポリシー',
      privacyAdsHeading: '3. 広告について',
      privacyAdsBody: '当サイトでは、以下の第三者配信の広告サービスを利用しています。広告配信事業者は、ユーザーの興味に応じた広告を表示するために Cookie を使用することがあります。Cookie を無効にする設定や詳細は、各広告サービスのページまたは',
      privacyAdsLinkSuffix: 'をご確認ください。',
      privacyAffiliateHeading: '4. アフィリエイトプログラムについて',
      privacyAffiliateBody: '当サイトは以下のアフィリエイトプログラムに参加しています。当サイト経由でサービスにお申し込みいただいた場合、当サイトに紹介料が支払われることがあります。これによりユーザーに追加の費用が発生することはありません。',
      privacyAffiliateNote: 'アフィリエイトリンクを含むコンテンツには、その旨を明示しています。',
      privacyExternalHeading: '5. 外部リンクについて',
      privacyExternalBody: '当サイトには外部サービスへのリンクが多数含まれています。外部サイトにおけるプライバシーポリシーおよび利用規約は、各サイトの管理者が定めるものであり、当サイトの管理範囲外となります。',
      privacyDisclaimerHeading: '6. 免責事項',
      privacyDisclaimerBody: '当サイトに掲載されている情報は、正確性を保つよう努めておりますが、その内容について保証するものではありません。掲載されている料金・機能・サービス内容は変更される場合があります。ご利用前に必ず各サービスの公式サイトで最新情報をご確認ください。当サイトの情報を利用することによって生じたいかなる損害についても、責任を負いかねます。',
      privacyChangesHeading: '7. プライバシーポリシーの変更について',
      privacyChangesBody: '当サイトは、必要に応じて本プライバシーポリシーの内容を変更することがあります。変更後のプライバシーポリシーは、当ページに掲載した時点から効力を有するものとします。',
      privacyContactHeading: '8. お問い合わせ',
      privacyContactBody: 'プライバシーポリシーに関するお問い合わせは、',
      privacyContactLink: 'GitHub リポジトリの Issues ページ',
      privacyContactSuffix: 'よりお願いいたします。',
      privacyUpdated: '最終更新日: 2026年3月7日',
    },
    en: {
      siteTitle: 'Tool Compare Navi',
      heroHeading: 'Find the perfect tool for you',
      heroSub: 'Compare popular web hosting, VPN, learning platforms, AI tools and more. Honest recommendations from a real user perspective.',
      heroCta1: 'Browse Tools',
      heroCta2: 'Free Assets',
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
      // Load more
      loadMore: 'Show More',
      // Personalized sections
      recentlyViewed: 'Recently Viewed',
      favSection: '❤️ Your Favorites',
      // Theme
      lang: '🌐 日本語',
      // Quiz
      quizBtn: '🔍 Find Your Tool',
      quizTitle: 'Tool Finder',
      quizQ1: 'What do you want to do?',
      quizQ1a: '🌐 Build a Website',
      quizQ1b: '🔒 Security',
      quizQ1c: '📚 Learn New Skills',
      quizQ1d: '🎨 Create Content',
      quizQ1e: '🤖 AI Tools',
      quizQ1f: '💼 Run a Business',
      quizQ1g: '☁️ File Management',
      quizQ1h: '📊 Boost SEO',
      quizQ2: 'What\'s your budget?',
      quizQ2a: '🆓 Free / Freemium',
      quizQ2b: '💰 Low Cost (< $15/mo)',
      quizQ2c: '💎 Budget is no concern',
      quizQ3: 'Your experience level?',
      quizQ3a: '🌱 Beginner',
      quizQ3b: '🌿 Intermediate',
      quizQ3c: '🌳 Advanced',
      quizResultTitle: 'Recommended Tools for You',
      quizNoResult: 'No tools matched your criteria.',
      quizRetry: 'Try Again',
      quizBack: '← Back',
      quizClose: 'Browse on my own',
      // Logo
      logoPrefix: 'Tool Compare',
      logoSuffix: 'Navi',
      // Navigation
      navAI: '🤖 AI Tools',
      navBlog: 'Blog',
      // Blog page
      blogIndexTitle: 'Blog Articles',
      blogIndexSub: 'Tool comparisons, rankings, and free tool features. Updated with the latest information.',
      blogToc: 'Table of Contents',
      blogVisitOfficial: 'Visit Official Site',
      blogReadReview: 'Read Full Review →',
      blogSectionRanking: 'Rankings',
      blogSectionCategory: 'Category Comparisons',
      blogSectionFree: 'Free Tool Features',
      blogSectionFeature: 'Feature Articles',
      blogSectionVs: 'VS Comparisons',
      blogConclusion: 'Conclusion',
      blogUpdated: 'Updated',
      blogProducts: 'products',
      blogProductsCompare: 'products compared',
      blogReadTime: 'Read time: ~',
      blogMinutes: 'min',
      blogArticles: 'articles',
      blogMerit: 'Pros',
      blogDemerit: 'Cons',
      blogFeatures: 'Key Features',
      blogTableTool: 'Tool Name',
      blogTablePrice: 'Price',
      blogTableRating: 'Rating',
      blogTableFeatures: 'Features',
      blogTableComparison: 'Comparison',
      blogTableRank: 'Rank',
      blogTableCategory: 'Category',
      blogRecommendedPoints: 'Key Highlights',
      blogHowToChoose: ' – How to Choose',
      blogComparisonTable: 'Comparison Table',
      blogOverview: 'Overview',
      blogComparisonOverview: 'Comparison Overview',
      blogSpecTable: 'Spec Comparison Table',
      blogWhichToChoose: 'Which Should You Choose?',
      blogFreeHowToChoose: 'Free ',
      blogFreeIntro: 'Why Free & What to Watch For',
      blogFreeComparison: 'Free Tools Comparison',
      blogPaidComparison: 'Paid Alternatives',
      blogRankingOverview: 'Ranking Overview',
      blogRankingTable: 'TOP 20 List',
      // Filters
      filterPriceLabel: 'Price Range',
      filterPriceAll: 'All',
      filterPriceFree: 'Free',
      filterPriceLow: '< $10',
      filterPriceMid: '< $40',
      filterPriceHigh: '$40+',
      filterTagLabel: 'Tags',
      filterTagFree: 'Free Plan Available',
      filterTagJapanese: 'Japanese Support',
      filterTagAPI: 'API Integration',
      filterTagNoCard: 'No Card Required',
      // Shutterstock banner
      ssBannerLabel: '📸 Looking for pro-quality assets?',
      ssBannerDesc: 'Over 300 million photos, videos, music & illustrations. For business and personal use.',
      ssBannerFeat1: '✅ Commercial Use OK',
      ssBannerFeat2: '✅ Japanese Support',
      ssBannerFeat3: '✅ Subscription Plans',
      ssBannerCta: 'Start Free Trial →',
      ssBannerNote: '* Free first month available',
      // Sister site banner
      sisterBannerPrefix: '🎨 Looking for free assets? →',
      sisterBannerName: 'Free Asset Portal',
      sisterBannerSuffix: '- Compare 200+ free asset sites',
      // AI page
      aiBreadcrumb: '🤖 AI Tool Comparison',
      aiHeroTitle: '🤖 AI Tool Comparison [2026 Latest]',
      aiHeroDesc: 'Compare popular AI tools including ChatGPT, Claude, Gemini, Midjourney, and GitHub Copilot by pricing, features, and free plan availability. Find the best AI tool for chat, image generation, coding assistance, voice synthesis, and more.',
      aiSearchPlaceholder: 'Search AI tools...',
      // Privacy page
      privacyTitle: 'Privacy Policy',
      privacyIntro: 'At "Tool Compare Navi" (hereinafter "this site", URL: https://tools.freesozo.com/), we respect user privacy and are committed to protecting personal information. This Privacy Policy explains how we handle information on this site.',
      privacyStorageHeading: '1. Use of Local Storage',
      privacyStorageBody: 'This site uses your browser\'s local storage (localStorage) to save the following information for a better user experience. All of this data is stored only in your browser and is never sent to our servers.',
      privacyStorageFav: 'Favorited tool information',
      privacyStorageTheme: 'Theme preference (Dark mode / Light mode)',
      privacyStorageLang: 'Language preference (Japanese / English)',
      privacyStorageRecent: 'Recently viewed tool browsing history',
      privacyStorageAffiliate: 'Affiliate link click information (anonymous)',
      privacyStorageNote: 'You can delete this data at any time through your browser settings. We do not collect any personally identifiable information.',
      privacyAnalyticsHeading: '2. Analytics',
      privacyAnalyticsBody: 'This site uses Google Analytics (GA4) to understand visitor traffic. Google Analytics uses cookies to collect traffic data. This data is collected anonymously and does not identify individuals. You can opt out by disabling cookies in your browser settings.',
      privacyAnalyticsSeeAlso: 'For details, see',
      privacyAnalyticsSuffix: '.',
      privacyGoogleLink: 'Google\'s Privacy Policy',
      privacyAdsHeading: '3. Advertising',
      privacyAdsBody: 'This site uses the following third-party advertising services. Advertising providers may use cookies to display ads based on user interests. For details on how to disable cookies, visit each advertising service\'s page or',
      privacyAdsLinkSuffix: '.',
      privacyAffiliateHeading: '4. Affiliate Programs',
      privacyAffiliateBody: 'This site participates in the following affiliate programs. If you sign up for services through this site, we may receive a referral commission. This does not result in any additional cost to you.',
      privacyAffiliateNote: 'Content containing affiliate links is clearly disclosed as such.',
      privacyExternalHeading: '5. External Links',
      privacyExternalBody: 'This site contains numerous links to external services. The privacy policies and terms of service of external sites are governed by their respective administrators and are outside the scope of this site\'s management.',
      privacyDisclaimerHeading: '6. Disclaimer',
      privacyDisclaimerBody: 'While we strive to ensure the accuracy of information on this site, we do not guarantee its content. Listed pricing, features, and service details are subject to change. Please check each service\'s official website for the latest information before use. We cannot be held responsible for any damages arising from the use of information on this site.',
      privacyChangesHeading: '7. Changes to This Policy',
      privacyChangesBody: 'This site may update this Privacy Policy as needed. The revised Privacy Policy will take effect from the time it is posted on this page.',
      privacyContactHeading: '8. Contact',
      privacyContactBody: 'For inquiries regarding this Privacy Policy, please use the',
      privacyContactLink: 'GitHub repository Issues page',
      privacyContactSuffix: '.',
      privacyUpdated: 'Last updated: March 7, 2026',
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
    // Blog cards: inline ja/en translations
    document.querySelectorAll('[data-i18n-ja]').forEach(el => {
      el.textContent = current === 'en'
        ? (el.getAttribute('data-i18n-en') || el.getAttribute('data-i18n-ja'))
        : el.getAttribute('data-i18n-ja');
    });
    window.dispatchEvent(new CustomEvent('langchange', { detail: { lang: current } }));
  }

  document.documentElement.lang = current;

  return { getLang, setLang, t, toggle, applyAll };
})();
