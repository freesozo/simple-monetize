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
CSS_VERSION = 10
JS_VERSION = 10
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


def star_html(rating):
    full = int(rating)
    half = "☆" if rating - full >= 0.5 else ""
    return "★" * full + half + "☆" * (5 - full - (1 if half else 0))


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
    region_flag = "🇯🇵" if region == "jp" else "🌐"
    region_label = "日本" if region == "jp" else "海外"
    aff = p.get("affiliateUrl") or p.get("officialUrl", "")
    reco = p.get("recommendedFor", "")
    verified = format_verified(p.get("lastChecked"))
    featured = ' featured' if p.get("featured") else ''
    featured_label = '★ おすすめ' if p.get("featured") else ''

    reco_html = f'\n          <p class="card-recommended">👤 こんな人に: {h(reco)}</p>' if reco else ''

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
      <a href="{root_prefix}/index.html" class="site-logo"><span>ツール比較</span><span>ナビ</span></a>
      <nav class="header-nav">
        <a href="{root_prefix}/index.html">ホーム</a>
        <a href="{root_prefix}/index.html#categories">カテゴリ</a>
        <a href="{root_prefix}/blog/">ブログ</a>
        <a href="{root_prefix}/about.html">サイトについて</a>
      </nav>
      <div class="header-actions">
        <button class="theme-btn" id="themeBtn" aria-label="Toggle theme">🌙</button>
        <button class="lang-btn" id="langBtn" data-i18n="lang">🌐 English</button>
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
      if(btn){{var t=document.documentElement.dataset.theme||'light';btn.textContent=t==='dark'?'☀️':'🌙';
        btn.addEventListener('click',function(){{var n=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=n;localStorage.setItem('theme',n);btn.textContent=n==='dark'?'☀️':'🌙';}});}}
      var lb=document.getElementById('langBtn');
      if(lb){{lb.textContent=I18n.t('lang');lb.addEventListener('click',function(){{I18n.toggle();lb.textContent=I18n.t('lang');}});}}
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
    emoji = CATEGORY_EMOJI.get(cat_id, "")
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
        f'        <a href="{c}.html" class="tag">{CATEGORY_EMOJI.get(c, "")} {CATEGORY_NAMES[c]}</a>'
        for c in CATEGORY_NAMES if c != cat_id
    )

    content = f'''    <section style="max-width:960px">
      <h1 style="font-size:1.5rem;font-weight:800;margin-bottom:12px">{emoji} {h(cat_ja)}おすすめ{count}選【{YEAR}年最新比較】</h1>
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

      <h2 style="font-size:1.1rem;margin:32px 0 12px">{emoji} {h(cat_ja)}に関する記事</h2>
      <ul style="line-height:1.8;margin-bottom:24px">
        <li><a href="../blog/{cat_id}-tools-comparison.html">{h(cat_ja)}おすすめ比較【{YEAR}年版】</a></li>
        <li><a href="../blog/free-{cat_id}-tools.html">無料で使える{h(cat_ja)}まとめ</a></li>
        <li><a href="../blog/best-tools-ranking.html">ビジネスツールおすすめランキングTOP20</a></li>
      </ul>

      <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:24px">
        <p>📦 <strong>フリー素材を探すなら →</strong> <a href="https://freesozo.com/" target="_blank" rel="noopener">フリー素材ポータル</a> — 写真・イラスト・音楽など221サイト以上を比較</p>
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
        breadcrumbs=[("ホーム", "../index.html"), (f"{emoji} {cat_ja}", None)],
        content=content, schema_json=schema,
    )


# ── Tool detail page ─────────────────────────────────────────────────

def generate_tool_page(product, all_products, by_cat):
    pid = product["id"]
    name = product["name"]
    cat_id = product.get("category", "")
    cat_ja = CATEGORY_NAMES.get(cat_id, cat_id)
    emoji = CATEGORY_EMOJI.get(cat_id, "")
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
      <p>👤 {h(reco)}</p>''' if reco else ''

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
          ⚠️ 掲載情報は{YEAR}年{MONTH}月時点の内容です。料金・機能は変更される場合があります。最新情報は公式サイトでご確認ください。
        </div>

        <a href="../category/{h(cat_id)}.html" class="btn btn-outline" style="margin-bottom:24px">{emoji} {h(cat_ja)}一覧に戻る</a>
{related_html}

        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-top:24px">
          <p>📦 <strong>デザインに使えるフリー素材はこちら →</strong> <a href="https://freesozo.com/" target="_blank" rel="noopener">フリー素材ポータル</a></p>
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
        breadcrumbs=[("ホーム", "../index.html"), (f"{emoji} {cat_ja}", f"../category/{cat_id}.html"),
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
