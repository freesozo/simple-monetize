#!/usr/bin/env python3
"""
Static Page Generator for tools.freesozo.com
Generates SEO-optimized static HTML pages from data/products.json:
  - category/*.html  (19 category listing pages)
  - tool/*.html      (individual tool detail pages)
  - Updates sitemap.xml

Usage: py generate-pages.py
"""

import json
import os
import html as html_mod
from datetime import date

# ── Config ──────────────────────────────────────────────────────────
BASE_URL = "https://tools.freesozo.com"
SITE_NAME = "おすすめツール比較ナビ"
GA_ID = "G-YL05931NPE"
ADSENSE_PUB = "ca-pub-1060876188767022"
CSS_VERSION = 15
JS_VERSION = 15
TODAY = date.today().isoformat()
YEAR = date.today().year
MONTH = date.today().month

CATEGORY_NAMES = {
    "server": "レンタルサーバー", "vpn": "VPN", "learning": "学習・スキルアップ",
    "ai": "AI ツール", "design": "デザインツール", "cloud": "クラウドストレージ",
    "domain": "ドメイン", "sitebuilder": "サイトビルダー", "ecommerce": "ECサイト・決済",
    "project": "プロジェクト管理", "communication": "コミュニケーション",
    "security": "セキュリティ", "seo": "SEO ツール", "video": "動画編集",
    "photo": "写真編集", "accounting": "会計・経理", "marketing": "マーケティング",
    "password": "パスワード管理", "writing": "ライティング・翻訳",
}

CATEGORY_EMOJI = {
    "server": "🖥️", "vpn": "🔒", "learning": "📚", "ai": "🤖", "design": "🎨",
    "cloud": "☁️", "domain": "🌐", "sitebuilder": "🏗️", "ecommerce": "🛒",
    "project": "📋", "communication": "💬", "security": "🛡️", "seo": "📊",
    "video": "🎬", "photo": "📷", "accounting": "💰", "marketing": "📧",
    "password": "🔑", "writing": "✍️",
}

_SVG_ATTRS = 'width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"'
CATEGORY_SVG = {
    "server": f'<svg {_SVG_ATTRS}><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><circle cx="6" cy="6" r="1"/><circle cx="6" cy="18" r="1"/></svg>',
    "vpn": f'<svg {_SVG_ATTRS}><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "learning": f'<svg {_SVG_ATTRS}><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "ai": f'<svg {_SVG_ATTRS}><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M9 9h6v6H9z"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>',
    "design": f'<svg {_SVG_ATTRS}><circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.93 0 1.5-.67 1.5-1.5 0-.39-.15-.74-.39-1.04-.24-.3-.39-.65-.39-1.04 0-.83.67-1.5 1.5-1.5H16c3.31 0 6-2.69 6-6 0-5.17-4.49-9-10-9z"/></svg>',
    "cloud": f'<svg {_SVG_ATTRS}><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>',
    "domain": f'<svg {_SVG_ATTRS}><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "sitebuilder": f'<svg {_SVG_ATTRS}><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>',
    "ecommerce": f'<svg {_SVG_ATTRS}><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
    "project": f'<svg {_SVG_ATTRS}><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 14l2 2 4-4"/></svg>',
    "communication": f'<svg {_SVG_ATTRS}><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "security": f'<svg {_SVG_ATTRS}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "seo": f'<svg {_SVG_ATTRS}><path d="M18 20V10M12 20V4M6 20v-6"/></svg>',
    "video": f'<svg {_SVG_ATTRS}><rect x="2" y="2" width="20" height="20" rx="2.18"/><path d="M7 2v20M17 2v20M2 12h20M2 7h5M2 17h5M17 17h5M17 7h5"/></svg>',
    "photo": f'<svg {_SVG_ATTRS}><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>',
    "accounting": f'<svg {_SVG_ATTRS}><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    "marketing": f'<svg {_SVG_ATTRS}><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "password": f'<svg {_SVG_ATTRS}><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>',
    "writing": f'<svg {_SVG_ATTRS}><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
}

CATEGORY_DESC = {
    "server": "国内外の人気レンタルサーバーを料金・速度・機能で徹底比較。WordPress対応やコスパ重視のおすすめサーバーが見つかります。",
    "vpn": "おすすめVPNサービスを速度・セキュリティ・料金で比較。海外から日本のサービスを使いたい方にも最適なVPNが見つかります。",
    "learning": "プログラミング・デザイン・ビジネススキルが学べるオンライン学習サービスを比較。無料プランのあるサービスも紹介。",
    "ai": "ChatGPT・Claude・Geminiなど人気AIツールを料金・機能で比較。チャットAI、画像生成、コーディング支援など用途別に最適なツールが見つかります。",
    "design": "Figma・Canvaなどデザインツールを機能・料金で比較。初心者からプロまで使えるおすすめデザインツールをご紹介。",
    "cloud": "Google Drive・Dropboxなどクラウドストレージを容量・料金・セキュリティで比較。",
    "domain": "ドメイン取得・管理サービスを料金・機能で比較。",
    "sitebuilder": "Wix・WordPress・Shopifyなどサイト作成ツールを比較。初心者でも簡単にWebサイトが作れるサービスをご紹介。",
    "ecommerce": "ネットショップ開設・決済サービスを比較。手数料・機能・使いやすさで最適なECプラットフォームが見つかります。",
    "project": "Notion・Asanaなどプロジェクト管理ツールを比較。チーム規模や用途に合ったツールが見つかります。",
    "communication": "Slack・Zoomなどコミュニケーションツールを比較。チャット・ビデオ会議・ファイル共有機能を比較できます。",
    "security": "Norton・CrowdStrikeなどセキュリティソフトを比較。ウイルス対策・VPN・パスワード管理の統合ソリューションをご紹介。",
    "seo": "Ahrefs・SEMrushなどSEOツールを比較。キーワード調査・競合分析・サイト監査機能で最適なツールが見つかります。",
    "video": "Premiere Pro・DaVinci Resolveなど動画編集ソフトを比較。初心者向け無料ソフトからプロ向けまで。",
    "photo": "Lightroom・Affinity Photoなど写真編集ソフトを比較。RAW現像・レタッチ・バッチ処理機能を比較できます。",
    "accounting": "freee・マネーフォワードなど会計ソフトを比較。確定申告・経費精算・請求書発行機能で比較できます。",
    "marketing": "メール配信・MA・広告管理ツールを比較。中小企業から大企業まで最適なマーケティングツールが見つかります。",
    "password": "1Password・Bitwardenなどパスワード管理ツールを比較。セキュリティ・使いやすさ・料金で最適なツールが見つかります。",
    "writing": "DeepL・Grammarlyなどライティング・翻訳ツールを比較。文章校正・翻訳品質・対応言語数で比較できます。",
}


# ── Helpers ──────────────────────────────────────────────────────────

def h(text):
    return html_mod.escape(str(text))


def load_products():
    path = os.path.join(os.path.dirname(__file__), "data", "products.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [p for p in data.get("products", []) if p.get("status") == "active"]


_STAR_FILLED = '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" stroke="currentColor" stroke-width="1.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
_STAR_EMPTY = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'

def star_html(rating):
    full = int(rating)
    half = _STAR_EMPTY if rating - full >= 0.5 else ""
    return _STAR_FILLED * full + half + _STAR_EMPTY * (5 - full - (1 if half else 0))


def format_verified(last_checked):
    if not last_checked:
        return f"{YEAR}年{MONTH}月 確認済み"
    d = date.fromisoformat(last_checked)
    return f"{d.year}年{d.month}月 確認済み"


def tool_card_static(p):
    """Static HTML card for a product."""
    pid = h(p["id"])
    name = h(p["name"])
    summary = h(p.get("summary", ""))
    rating = p.get("rating", 0)
    price = h(p.get("price", ""))
    cat = p.get("category", "")
    cat_name = h(CATEGORY_NAMES.get(cat, cat))
    region = p.get("region", "global")
    region_flag = '<svg viewBox="0 0 24 16" width="18" height="12" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="16" fill="#fff" rx="2"/><circle cx="12" cy="8" r="4.5" fill="#bc002d"/></svg>' if region == "jp" else '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'
    region_label = "日本" if region == "jp" else "海外"
    aff = p.get("affiliateUrl") or p.get("officialUrl", "")
    reco = p.get("recommendedFor", "")
    verified = format_verified(p.get("lastChecked"))
    featured = ' featured' if p.get("featured") else ''
    featured_label = 'おすすめ' if p.get("featured") else ''

    reco_html = f'\n          <p class="card-recommended"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> こんな人に: {h(reco)}</p>' if reco else ''

    return f'''    <div class="product-card{featured}" data-featured-label="{featured_label}">
      <div class="card-body">
        <div class="card-top-row">
          <span class="card-category">{cat_name} <span class="card-region card-region-{region}">{region_flag} {region_label}</span></span>
        </div>
        <h3 class="card-title"><a href="../tool/{pid}.html">{name}</a></h3>
        <p class="card-summary">{summary}</p>{reco_html}
        <div class="card-meta">
          <span class="card-rating">{star_html(rating)} {rating}</span>
          <span class="card-price">{price}</span>
        </div>
        <div class="card-actions">
          <a href="../tool/{pid}.html" class="btn btn-outline">詳細を見る</a>
          <a href="{h(aff)}" class="btn btn-primary" target="_blank" rel="noopener noreferrer nofollow">公式サイトへ</a>
        </div>
        <span class="card-verified">{verified}</span>
      </div>
    </div>'''


# ── Page template ────────────────────────────────────────────────────

def page_html(*, title, description, canonical, breadcrumbs, content, schema_json,
              root_prefix=".."):
    bc_items = []
    for name, url in breadcrumbs:
        if url:
            bc_items.append(f'<a href="{url}">{h(name)}</a>')
        else:
            bc_items.append(f'<span>{h(name)}</span>')
    bc_html = ' <span>›</span> '.join(bc_items)

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h(title)}</title>
  <meta name="description" content="{h(description)}">
  <meta property="og:title" content="{h(title)}">
  <meta property="og:description" content="{h(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:image" content="{BASE_URL}/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{h(title)}">
  <meta name="twitter:description" content="{h(description)}">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="{root_prefix}/favicon.svg" type="image/svg+xml">
  <script>(function(){{var t=localStorage.getItem('theme');if(!t)t=window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}})();</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600;700;900&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root_prefix}/css/style.css?v={CSS_VERSION}">
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
    gtag('js',new Date());gtag('config','{GA_ID}');
  </script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB}" crossorigin="anonymous"></script>
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a href="{root_prefix}/index.html" class="site-logo"><span class="logo-text">freesozo</span> <span class="logo-sub">tools</span></a>
      <nav class="header-nav">
        <a href="{root_prefix}/index.html">ホーム</a>
        <div class="nav-dropdown">
          <a href="{root_prefix}/index.html#categories" class="nav-dropdown-trigger">
            <span>カテゴリ</span> <span class="dropdown-arrow">▾</span>
          </a>
          <div class="nav-dropdown-menu">
            <a href="{root_prefix}/category/server.html">{CATEGORY_SVG['server']} サーバー</a>
            <a href="{root_prefix}/category/vpn.html">{CATEGORY_SVG['vpn']} VPN</a>
            <a href="{root_prefix}/category/ai.html">{CATEGORY_SVG['ai']} AIツール</a>
            <a href="{root_prefix}/category/design.html">{CATEGORY_SVG['design']} デザイン</a>
            <a href="{root_prefix}/category/learning.html">{CATEGORY_SVG['learning']} 学習</a>
            <a href="{root_prefix}/category/security.html">{CATEGORY_SVG['security']} セキュリティ</a>
            <a href="{root_prefix}/category/cloud.html">{CATEGORY_SVG['cloud']} クラウド</a>
            <a href="{root_prefix}/category/video.html">{CATEGORY_SVG['video']} 動画編集</a>
            <a href="{root_prefix}/category/ecommerce.html">{CATEGORY_SVG['ecommerce']} EC・決済</a>
            <a href="{root_prefix}/category/seo.html">{CATEGORY_SVG['seo']} SEO</a>
            <a href="{root_prefix}/category/project.html">{CATEGORY_SVG['project']} プロジェクト管理</a>
            <a href="{root_prefix}/category/communication.html">{CATEGORY_SVG['communication']} コミュニケーション</a>
            <a href="{root_prefix}/category/sitebuilder.html">{CATEGORY_SVG['sitebuilder']} サイトビルダー</a>
            <a href="{root_prefix}/category/domain.html">{CATEGORY_SVG['domain']} ドメイン</a>
            <a href="{root_prefix}/category/photo.html">{CATEGORY_SVG['photo']} 写真編集</a>
            <a href="{root_prefix}/category/accounting.html">{CATEGORY_SVG['accounting']} 会計・経理</a>
            <a href="{root_prefix}/category/marketing.html">{CATEGORY_SVG['marketing']} マーケティング</a>
            <a href="{root_prefix}/category/password.html">{CATEGORY_SVG['password']} パスワード管理</a>
            <a href="{root_prefix}/category/writing.html">{CATEGORY_SVG['writing']} ライティング</a>
          </div>
        </div>
        <a href="{root_prefix}/diagnosis.html">AI診断</a>
        <a href="{root_prefix}/blog/">ブログ</a>
        <a href="{root_prefix}/about.html">サイトについて</a>
      </nav>
      <div class="header-actions">
        <button class="theme-btn" id="themeBtn" aria-label="Toggle theme"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></button>
        <button class="lang-btn" id="langBtn" data-i18n="lang"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg> English</button>
      </div>
    </div>
  </header>

  <main class="container" style="padding-top:24px;padding-bottom:40px">
    <nav class="breadcrumb" aria-label="Breadcrumb" style="font-size:.85rem;margin-bottom:16px;color:var(--text-muted)">
      {bc_html}
    </nav>

{content}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-links">
        <a href="{root_prefix}/index.html">ホーム</a>
        <a href="{root_prefix}/blog/">ブログ</a>
        <a href="{root_prefix}/about.html">サイトについて</a>
        <a href="{root_prefix}/privacy.html">プライバシーポリシー</a>
      </div>
      <p class="sister-site">姉妹サイト: <a href="https://freesozo.com/" target="_blank" rel="noopener">フリー素材ポータル</a></p>
      <p>※ 当サイトはアフィリエイトプログラムに参加しています。</p>
      <p>&copy; {YEAR} {SITE_NAME}</p>
    </div>
  </footer>

  <button class="back-to-top" id="backToTop">↑</button>
  <script src="{root_prefix}/js/i18n.js?v={JS_VERSION}"></script>
  <script>
    (function(){{
      var btn=document.getElementById('themeBtn');
      if(btn){{var t=document.documentElement.dataset.theme||'light';btn.innerHTML=t==='dark'?'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>':'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
        btn.addEventListener('click',function(){{var n=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=n;localStorage.setItem('theme',n);btn.innerHTML=n==='dark'?'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>':'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';}});}}
      var lb=document.getElementById('langBtn');
      if(lb){{lb.innerHTML=I18n.t('lang');lb.addEventListener('click',function(){{I18n.toggle();lb.innerHTML=I18n.t('lang');}});}}
      I18n.applyAll();
      var btt=document.getElementById('backToTop');
      if(btt){{window.addEventListener('scroll',function(){{btt.classList.toggle('visible',window.scrollY>400);}});btt.addEventListener('click',function(){{window.scrollTo({{top:0,behavior:'smooth'}});}});}}
    }})();
  </script>
</body>
</html>'''


# ── Category page ────────────────────────────────────────────────────

def generate_category_page(cat_id, products):
    cat_ja = CATEGORY_NAMES[cat_id]
    svg_icon = CATEGORY_SVG.get(cat_id, "")
    desc = CATEGORY_DESC.get(cat_id, f"{cat_ja}を料金・機能で比較。")
    count = len(products)

    title = f"{cat_ja}おすすめ{count}選 比較【{YEAR}年最新】| {SITE_NAME}"
    canonical = f"{BASE_URL}/category/{cat_id}.html"

    prods_sorted = sorted(products, key=lambda p: (-p.get("rating", 0), p["name"]))
    cards = "\n".join(tool_card_static(p) for p in prods_sorted)

    # Comparison table
    rows = []
    for p in prods_sorted:
        pid = h(p["id"])
        name = h(p["name"])
        rating = f'{p.get("rating", 0)}'
        price = h(p.get("price", ""))
        free = "○" if any("無料" in str(p.get("freeLimit", "")) or f in str(p.get("freeFeatures", []))
                         for f in ["無料"]) or p.get("freeFeatures") else "—"
        rows.append(f'          <tr><td><a href="../tool/{pid}.html">{name}</a></td><td>{rating}/5</td><td>{price}</td><td>{free}</td></tr>')
    rows_str = "\n".join(rows)

    other_cats = "\n".join(
        f'        <a href="{c}.html" class="tag">{CATEGORY_SVG.get(c, "")} {CATEGORY_NAMES[c]}</a>'
        for c in CATEGORY_NAMES if c != cat_id
    )

    content = f'''    <section style="max-width:960px">
      <h1 style="font-size:1.5rem;font-weight:800;margin-bottom:12px">{svg_icon} {h(cat_ja)}おすすめ{count}選【{YEAR}年最新比較】</h1>
      <p style="color:var(--text-sub);line-height:1.7;margin-bottom:16px">{h(desc)}</p>
      <p style="font-size:.85rem;color:var(--text-muted);margin-bottom:24px">掲載ツール数: <strong>{count}件</strong>（{YEAR}年{MONTH}月更新）</p>

      <h2 style="font-size:1.2rem;margin-bottom:12px">比較表</h2>
      <div class="blog-comparison-table" style="margin-bottom:32px">
        <table>
          <thead><tr><th>ツール名</th><th>評価</th><th>料金</th><th>無料プラン</th></tr></thead>
          <tbody>
{rows_str}
          </tbody>
        </table>
      </div>

      <h2 style="font-size:1.2rem;margin-bottom:16px">各ツールの詳細</h2>
      <div class="product-grid">
{cards}
      </div>

      <h2 style="font-size:1.1rem;margin:32px 0 12px">{svg_icon} {h(cat_ja)}に関する記事</h2>
      <ul style="line-height:1.8;margin-bottom:24px">
        <li><a href="../blog/{cat_id}-tools-comparison.html">{h(cat_ja)}おすすめ比較【{YEAR}年版】</a></li>
        <li><a href="../blog/free-{cat_id}-tools.html">無料で使える{h(cat_ja)}まとめ</a></li>
        <li><a href="../blog/best-tools-ranking.html">ビジネスツールおすすめランキングTOP20</a></li>
      </ul>

      <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:24px">
        <p><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg> <strong>フリー素材を探すなら →</strong> <a href="https://freesozo.com/" target="_blank" rel="noopener">フリー素材ポータル</a> — 写真・イラスト・音楽など221サイト以上を比較</p>
      </div>

      <h2 style="font-size:1.1rem;margin:32px 0 12px">他のカテゴリ</h2>
      <div style="display:flex;flex-wrap:wrap;gap:8px">
{other_cats}
      </div>
    </section>'''

    item_list = [{
        "@type": "ListItem", "position": i+1,
        "name": p["name"], "url": f"{BASE_URL}/tool/{p['id']}.html"
    } for i, p in enumerate(prods_sorted)]

    schema = json.dumps([
        {"@context": "https://schema.org", "@type": "ItemList",
         "name": f"{cat_ja}おすすめ比較", "numberOfItems": count,
         "itemListElement": item_list},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{BASE_URL}/"},
             {"@type": "ListItem", "position": 2, "name": cat_ja, "item": canonical}
         ]}
    ], ensure_ascii=False, indent=2)

    return page_html(
        title=title, description=desc, canonical=canonical,
        breadcrumbs=[("ホーム", "../index.html"), (f"{svg_icon} {cat_ja}", None)],
        content=content, schema_json=schema,
    )


# ── Tool detail page ─────────────────────────────────────────────────

def generate_tool_page(product, all_products, by_cat):
    pid = product["id"]
    name = product["name"]
    cat_id = product.get("category", "")
    cat_ja = CATEGORY_NAMES.get(cat_id, cat_id)
    svg_icon = CATEGORY_SVG.get(cat_id, "")
    desc_text = product.get("description", product.get("summary", ""))
    summary = product.get("summary", "")
    rating = product.get("rating", 0)
    price = product.get("price", "")
    aff = product.get("affiliateUrl") or product.get("officialUrl", "")
    official = product.get("officialUrl", "")
    reco = product.get("recommendedFor", "")
    free_limit = product.get("freeLimit", "")
    verified = format_verified(product.get("lastChecked"))

    title = f"{name}の評判・料金・機能【{YEAR}年】| {SITE_NAME}"
    description = f"{name}のレビュー。{summary}"[:160]
    canonical = f"{BASE_URL}/tool/{pid}.html"

    # Pros / Cons / Features
    pros = product.get("pros", [])
    cons = product.get("cons", [])
    features = product.get("features", [])
    free_features = product.get("freeFeatures", [])

    pros_html = "\n".join(f"          <li>{h(p)}</li>" for p in pros) if pros else "<li>—</li>"
    cons_html = "\n".join(f"          <li>{h(c)}</li>" for c in cons) if cons else "<li>—</li>"
    feat_html = "\n".join(f"          <li>{h(f)}</li>" for f in features) if features else ""
    free_feat_html = ""
    if free_limit or free_features:
        items = "\n".join(f"          <li>{h(f)}</li>" for f in free_features)
        free_feat_html = f'''
      <h2>無料プランでできること</h2>
      {f'<p>{h(free_limit)}</p>' if free_limit else ''}
      {'<ul>' + items + '</ul>' if free_features else ''}'''

    reco_html = f'''
      <h2>こんな人におすすめ</h2>
      <p><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> {h(reco)}</p>''' if reco else ''

    # Related tools
    related = [p for p in by_cat.get(cat_id, []) if p["id"] != pid][:5]
    related_html = ""
    if related:
        items = "\n".join(
            f'        <li><a href="{p["id"]}.html">{h(p["name"])}</a> — {h(p.get("summary", "")[:60])}</li>'
            for p in related
        )
        related_html = f'''
      <h2>関連する{h(cat_ja)}ツール</h2>
      <ul style="line-height:1.8">
{items}
      </ul>'''

    content = f'''    <section class="review-page">
      <div class="review-description" style="max-width:800px">
        <h1>{h(name)}</h1>
        <div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:12px">
          <span class="card-rating" style="font-size:1.1rem">{star_html(rating)} {rating}</span>
          <span style="font-weight:700;font-size:1.1rem">{h(price)}</span>
          <span class="card-verified">{verified}</span>
        </div>

        <p style="line-height:1.8;margin-bottom:20px">{h(desc_text)}</p>

        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px">
          <a href="{h(aff)}" class="btn btn-primary" target="_blank" rel="noopener noreferrer nofollow" style="padding:12px 28px">公式サイトを見る →</a>
          {f'<a href="{h(official)}" class="btn btn-outline" target="_blank" rel="noopener noreferrer" style="padding:12px 28px">公式サイト（直接）</a>' if official and official != aff else ''}
        </div>

        <div class="pros-cons" style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px">
          <div class="pros">
            <h3>メリット</h3>
            <ul>
{pros_html}
            </ul>
          </div>
          <div class="cons">
            <h3>デメリット</h3>
            <ul>
{cons_html}
            </ul>
          </div>
        </div>

        {f'<h2>主な機能・特徴</h2><ul>{feat_html}</ul>' if feat_html else ''}
{free_feat_html}
{reco_html}

        <div style="margin:24px 0;padding:16px;background:var(--bg-card);border:1px solid var(--border);border-radius:8px;font-size:.85rem;color:var(--text-muted)">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> 掲載情報は{YEAR}年{MONTH}月時点の内容です。料金・機能は変更される場合があります。最新情報は公式サイトでご確認ください。
        </div>

        <a href="../category/{h(cat_id)}.html" class="btn btn-outline" style="margin-bottom:24px">{svg_icon} {h(cat_ja)}一覧に戻る</a>
{related_html}

        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-top:24px">
          <p><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg> <strong>デザインに使えるフリー素材はこちら →</strong> <a href="https://freesozo.com/" target="_blank" rel="noopener">フリー素材ポータル</a></p>
        </div>
      </div>
    </section>'''

    schema = json.dumps([
        {"@context": "https://schema.org", "@type": "SoftwareApplication",
         "name": name, "description": desc_text[:200],
         "applicationCategory": "WebApplication",
         "operatingSystem": "Web",
         "offers": {"@type": "Offer", "price": "0" if "無料" in price else price.replace("¥","").split("/")[0],
                    "priceCurrency": "JPY"},
         "aggregateRating": {"@type": "AggregateRating",
                             "ratingValue": str(rating), "bestRating": "5"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{BASE_URL}/"},
             {"@type": "ListItem", "position": 2, "name": cat_ja,
              "item": f"{BASE_URL}/category/{cat_id}.html"},
             {"@type": "ListItem", "position": 3, "name": name, "item": canonical}
         ]}
    ], ensure_ascii=False, indent=2)

    return page_html(
        title=title, description=description, canonical=canonical,
        breadcrumbs=[("ホーム", "../index.html"), (f"{svg_icon} {cat_ja}", f"../category/{cat_id}.html"),
                     (name, None)],
        content=content, schema_json=schema,
    )


# ── Sitemap ──────────────────────────────────────────────────────────

def update_sitemap(categories, tool_ids):
    sitemap_path = os.path.join(os.path.dirname(__file__), "sitemap.xml")
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    import re
    content = re.sub(r'  <!-- SSG -->\n(?:.*\n)*?  <!-- /SSG -->\n', '', content)

    lines = ['  <!-- SSG -->']
    for c in categories:
        lines.append(f'  <url><loc>{BASE_URL}/category/{c}.html</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>')
    for t in tool_ids:
        lines.append(f'  <url><loc>{BASE_URL}/tool/{t}.html</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')
    lines.append('  <!-- /SSG -->')

    content = content.replace("</urlset>", "\n".join(lines) + "\n</urlset>")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  sitemap.xml updated ({len(categories)} categories + {len(tool_ids)} tools)")


# ── CSS ──────────────────────────────────────────────────────────────

def ensure_css():
    css_path = os.path.join(os.path.dirname(__file__), "css", "style.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    if "/* SSG tools */" in css:
        return
    with open(css_path, "a", encoding="utf-8") as f:
        f.write("""
/* SSG tools */
.breadcrumb a { color: var(--primary); }
.breadcrumb span { color: var(--text-muted); }
.product-card .card-title a { color: inherit; text-decoration: none; }
.product-card .card-title a:hover { color: var(--primary); }
""")
    print("  Added SSG CSS")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    print("=== Static Page Generator for tools.freesozo.com ===\n")

    products = load_products()
    print(f"Loaded {len(products)} active products")

    by_cat = {}
    for p in products:
        by_cat.setdefault(p.get("category", "other"), []).append(p)

    ensure_css()

    # Category pages
    cat_dir = os.path.join(os.path.dirname(__file__), "category")
    os.makedirs(cat_dir, exist_ok=True)
    print("\n--- Category Pages ---")
    gen_cats = []
    for cat_id in sorted(CATEGORY_NAMES.keys()):
        prods = by_cat.get(cat_id, [])
        if not prods:
            continue
        html = generate_category_page(cat_id, prods)
        with open(os.path.join(cat_dir, f"{cat_id}.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [OK] category/{cat_id}.html ({len(prods)} tools)")
        gen_cats.append(cat_id)

    # Tool detail pages
    tool_dir = os.path.join(os.path.dirname(__file__), "tool")
    os.makedirs(tool_dir, exist_ok=True)
    print("\n--- Tool Detail Pages ---")
    gen_tools = []
    for p in products:
        html = generate_tool_page(p, products, by_cat)
        with open(os.path.join(tool_dir, f"{p['id']}.html"), "w", encoding="utf-8") as f:
            f.write(html)
        gen_tools.append(p["id"])
    print(f"  [OK] Generated {len(gen_tools)} tool detail pages")

    # Sitemap
    print("\n--- Sitemap ---")
    update_sitemap(gen_cats, gen_tools)

    print(f"\n=== Done! {len(gen_cats)} categories + {len(gen_tools)} tools ===")


if __name__ == "__main__":
    main()
