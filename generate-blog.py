#!/usr/bin/env python3
"""
Blog Article Generator for tools.freesozo.com
Reads products.json and config.json, generates static blog HTML pages.
Usage: py generate-blog.py
"""

import json
import os
import html as html_mod
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
DATA_DIR = os.path.join(BASE_DIR, "data")
SITE_URL = "https://tools.freesozo.com"
GENERATE_DATE = date.today().isoformat()
YEAR = str(date.today().year)
CSS_VERSION = "8"
JS_VERSION = "8"

CATEGORY_NAMES = {
    "server": "レンタルサーバー",
    "vpn": "VPN",
    "learning": "学習・スキルアップ",
    "ai": "AI ツール",
    "design": "デザインツール",
    "cloud": "クラウドストレージ",
    "domain": "ドメイン",
    "sitebuilder": "サイトビルダー",
    "ecommerce": "ECサイト・決済",
    "project": "プロジェクト管理",
    "communication": "コミュニケーション",
    "security": "セキュリティ",
    "seo": "SEO ツール",
    "video": "動画編集",
    "photo": "写真編集",
    "accounting": "会計・経理",
    "marketing": "マーケティング",
    "password": "パスワード管理",
    "writing": "ライティング・翻訳",
}

CATEGORY_NAMES_EN = {
    "server": "Web Hosting",
    "vpn": "VPN",
    "learning": "Learning",
    "ai": "AI Tools",
    "design": "Design Tools",
    "cloud": "Cloud Storage",
    "domain": "Domain",
    "sitebuilder": "Site Builder",
    "ecommerce": "E-commerce",
    "project": "Project Management",
    "communication": "Communication",
    "security": "Security",
    "seo": "SEO Tools",
    "video": "Video Editing",
    "photo": "Photo Editing",
    "accounting": "Accounting",
    "marketing": "Marketing",
    "password": "Password Manager",
    "writing": "Writing & Translation",
}

CATEGORY_ICONS = {
    "server": "&#x1F5A5;&#xFE0F;",
    "vpn": "&#x1F512;",
    "learning": "&#x1F4DA;",
    "ai": "&#x1F916;",
    "design": "&#x1F3A8;",
    "cloud": "&#x2601;&#xFE0F;",
    "domain": "&#x1F310;",
    "sitebuilder": "&#x1F3D7;&#xFE0F;",
    "ecommerce": "&#x1F6D2;",
    "project": "&#x1F4CB;",
    "communication": "&#x1F4AC;",
    "security": "&#x1F6E1;&#xFE0F;",
    "seo": "&#x1F4CA;",
    "video": "&#x1F3AC;",
    "photo": "&#x1F4F7;",
    "accounting": "&#x1F4B0;",
    "marketing": "&#x1F4E7;",
    "password": "&#x1F511;",
    "writing": "&#x270D;&#xFE0F;",
}

# Intro text per category for SEO
CATEGORY_INTROS = {
    "server": "ウェブサイトやブログの運営に欠かせないレンタルサーバー。速度・安定性・料金・サポートなど、選ぶポイントは多岐にわたります。本記事では、{year}年現在おすすめのレンタルサーバーを厳選し、各サービスの特徴を徹底的に比較します。初心者からプロまで、あなたの用途に最適なサーバーが見つかるはずです。",
    "vpn": "インターネットのセキュリティとプライバシー保護に不可欠なVPN。海外コンテンツへのアクセスやリモートワーク時のセキュリティ確保など、活用シーンは広がっています。本記事では{year}年おすすめのVPNサービスを比較し、速度・セキュリティ・料金の面から最適な選択肢をご紹介します。",
    "learning": "スキルアップやキャリアチェンジに役立つオンライン学習サービス。プログラミング、デザイン、ビジネスなど幅広い分野を学べるプラットフォームが増えています。{year}年版として、人気の学習サービスを料金・コンテンツ・使いやすさで徹底比較します。",
    "ai": "ChatGPTの登場以降、AIツールは急速に進化を続けています。文章生成、画像生成、コーディング支援など、{year}年はさらに多様なAIサービスが登場。本記事では注目のAIツールを機能・料金・使いやすさで比較し、目的別のおすすめをご紹介します。",
    "design": "Webデザイン、グラフィック制作、UIデザインなど、クリエイティブワークに欠かせないデザインツール。{year}年はAI機能の搭載も進み、より効率的なデザインが可能になっています。人気デザインツールを機能・料金で徹底比較します。",
    "cloud": "写真、動画、ドキュメントなど大切なファイルを安全に保存・共有できるクラウドストレージ。{year}年版として、主要なクラウドストレージサービスを容量・料金・セキュリティ・共有機能で比較します。個人利用からビジネス利用まで、最適なサービスを見つけましょう。",
    "domain": "独自ドメインはウェブサイトの「住所」。信頼性とブランディングに直結する重要な要素です。{year}年おすすめのドメイン取得サービスを料金・管理機能・サポートで比較し、最適な選択をサポートします。",
    "sitebuilder": "プログラミング知識がなくてもプロ品質のウェブサイトが作れるサイトビルダー。{year}年は AI 機能搭載のものも増え、さらに手軽にサイト制作が可能に。人気サイトビルダーをテンプレート数・機能・料金で徹底比較します。",
    "ecommerce": "オンラインショップ開設に必要なECサイト構築・決済サービス。{year}年は越境ECやサブスクリプション対応など機能が多様化。主要なECプラットフォームを手数料・機能・使いやすさで比較し、あなたのビジネスに最適なサービスをご紹介します。",
    "project": "チームの生産性を高めるプロジェクト管理ツール。タスク管理、進捗管理、チームコラボレーションなど{year}年最新のプロジェクト管理ツールを機能・料金・使いやすさで比較します。リモートワーク時代に最適なツールを見つけましょう。",
    "communication": "リモートワークやチーム連携に欠かせないコミュニケーションツール。ビデオ会議、チャット、ファイル共有など{year}年おすすめのコミュニケーションツールを機能・料金・セキュリティで比較します。",
    "security": "サイバー攻撃やデータ漏洩のリスクが高まる中、セキュリティ対策は必須。{year}年おすすめのセキュリティツールをウイルス対策・ファイアウォール・価格で比較し、個人からビジネスまで最適なセキュリティ対策をご紹介します。",
    "seo": "検索エンジンからの集客に不可欠なSEOツール。キーワード調査、サイト分析、競合分析など{year}年おすすめのSEOツールを機能・料金・使いやすさで比較します。サイトのアクセスアップに最適なツールを見つけましょう。",
    "video": "YouTubeやSNS向けの動画制作に必要な動画編集ツール。{year}年はAI自動編集やクラウド編集など革新的な機能が続々登場。人気の動画編集ソフトを機能・料金・対応フォーマットで比較します。",
    "photo": "写真のレタッチ、加工、RAW現像に必要な写真編集ツール。{year}年版として、プロ向けからカジュアルユース向けまで主要な写真編集ソフトを機能・料金・AI機能で比較します。",
    "accounting": "確定申告やインボイス対応など、経理業務を効率化する会計ソフト。{year}年おすすめの会計・経理ツールを機能・料金・サポートで比較し、フリーランスから法人まで最適なサービスをご紹介します。",
    "marketing": "メールマーケティング、SNS運用、広告管理など、集客に必要なマーケティングツール。{year}年おすすめのマーケティングツールを機能・料金・自動化機能で比較し、効果的な集客戦略をサポートします。",
    "password": "増え続けるオンラインアカウントのパスワードを安全に管理するパスワード管理ツール。{year}年おすすめのパスワードマネージャーをセキュリティ・使いやすさ・料金で比較し、安全なパスワード運用を実現します。",
    "writing": "ブログ記事やビジネス文書の作成、多言語翻訳に役立つライティング・翻訳ツール。{year}年はAI搭載の文章校正・自動翻訳がさらに進化。主要なライティングツールを機能・精度・料金で比較します。",
}


def load_data():
    with open(os.path.join(DATA_DIR, "products.json"), "r", encoding="utf-8") as f:
        products_data = json.load(f)
    with open(os.path.join(DATA_DIR, "config.json"), "r", encoding="utf-8") as f:
        config_data = json.load(f)
    return products_data["products"], config_data


def h(text):
    """HTML escape"""
    return html_mod.escape(str(text))


def star_rating_html(rating):
    """Generate star rating HTML"""
    full = int(rating)
    half = 1 if rating - full >= 0.3 else 0
    empty = 5 - full - half
    stars = '<span style="color:#f59e0b;">'
    stars += "&#9733;" * full
    if half:
        stars += "&#9733;"  # half star shown as full for simplicity
    stars += "</span>"
    stars += '<span style="color:#d1d5db;">' + "&#9734;" * empty + "</span>"
    return stars + f" <strong>{rating}</strong>"


def reading_time(text_len):
    """Estimate reading time in minutes"""
    chars_per_min = 500  # Japanese
    mins = max(1, text_len // chars_per_min)
    return mins


def head_html(title, description, canonical_url, og_type="article"):
    """Generate <head> section matching existing site"""
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h(title)}</title>
  <meta name="description" content="{h(description)}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#ff6b35">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="canonical" href="{h(canonical_url)}">
  <link rel="alternate" hreflang="ja" href="{h(canonical_url)}">
  <link rel="alternate" hreflang="en" href="{h(canonical_url)}?lang=en">
  <!-- OGP -->
  <meta property="og:title" content="{h(title)}">
  <meta property="og:description" content="{h(description)}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{h(canonical_url)}">
  <meta property="og:image" content="{SITE_URL}/og-image.png">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="おすすめツール比較ナビ">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{h(title)}">
  <meta name="twitter:description" content="{h(description)}">
  <script>(function(){{var t=localStorage.getItem('theme');if(!t)t=window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';document.documentElement.dataset.theme=t;}})()</script>
  <link rel="stylesheet" href="../css/style.css?v={CSS_VERSION}">
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-YL05931NPE"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-YL05931NPE');
  </script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1060876188767022" crossorigin="anonymous"></script>
'''


def schema_article_jsonld(title, description, url, date):
    """Schema.org Article JSON-LD"""
    return f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {json.dumps(title, ensure_ascii=False)},
    "description": {json.dumps(description, ensure_ascii=False)},
    "url": {json.dumps(url)},
    "datePublished": "{date}",
    "dateModified": "{date}",
    "author": {{
      "@type": "Organization",
      "name": "おすすめツール比較ナビ",
      "url": "{SITE_URL}/"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "おすすめツール比較ナビ",
      "url": "{SITE_URL}/"
    }},
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": {json.dumps(url)}
    }}
  }}
  </script>
'''


def breadcrumb_jsonld(crumbs):
    """Schema.org BreadcrumbList JSON-LD. crumbs: list of (name, url)"""
    items = []
    for i, (name, url) in enumerate(crumbs, 1):
        items.append(f'''      {{
        "@type": "ListItem",
        "position": {i},
        "name": {json.dumps(name, ensure_ascii=False)},
        "item": {json.dumps(url)}
      }}''')
    return f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
{",\\n".join(items)}
    ]
  }}
  </script>
'''


def header_html():
    """Site header matching existing design"""
    return '''</head>
<body>
  <!-- Header -->
  <header class="site-header">
    <div class="container">
      <a href="../index.html" class="site-logo">ツール比較<span>ナビ</span></a>
      <nav class="header-nav">
        <a href="../index.html" data-i18n="navHome">ホーム</a>
        <a href="../index.html#categories" data-i18n="navCategory">カテゴリ</a>
        <a href="../index.html#all-products" data-i18n="navAll">全ツール</a>
        <a href="index.html">ブログ</a>
      </nav>
      <div class="header-actions">
        <button class="theme-btn" id="themeBtn" aria-label="Toggle theme">&#x1F319;</button>
        <button class="lang-btn" id="langBtn" data-i18n="lang">&#x1F310; English</button>
      </div>
    </div>
  </header>
'''


def breadcrumb_html(crumbs):
    """Breadcrumb nav. crumbs: list of (name, url_or_None)"""
    parts = []
    for name, url in crumbs:
        if url:
            parts.append(f'<a href="{h(url)}">{h(name)}</a>')
        else:
            parts.append(f'<span>{h(name)}</span>')
    return f'''  <div class="container">
    <div class="breadcrumb">
      {"<span>&#x203A;</span>".join(parts)}
    </div>
  </div>
'''


def footer_html():
    """Site footer matching existing design"""
    return '''  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-links">
        <a href="../index.html" data-i18n="footerHome">ホーム</a>
        <a href="index.html">ブログ</a>
        <a href="../privacy.html" data-i18n="footerPrivacy">プライバシーポリシー</a>
      </div>
      <p class="sister-site"><span data-i18n="footerSister">姉妹サイト:</span> <a href="https://freesozo.com/" target="_blank" rel="noopener" data-i18n="footerSisterName">フリー素材ポータル</a></p>
      <p data-i18n="footerAffiliate">※ 当サイトはアフィリエイトプログラムに参加しています。</p>
      <p data-i18n="footerCopyright">&copy; 2026 おすすめツール比較ナビ</p>
    </div>
  </footer>

  <button class="back-to-top" id="backToTop">&uarr;</button>
  <div class="toast" id="toast"></div>

  <script src="../js/i18n.js?v={version}"></script>
  <script src="../js/app.js?v={version}"></script>
</body>
</html>'''.format(version=JS_VERSION)


def adsense_mid_article():
    """Mid-article AdSense slot"""
    return '''    <div class="blog-ad-slot" style="margin:32px 0; text-align:center;">
      <ins class="adsbygoogle"
        style="display:block"
        data-ad-client="ca-pub-1060876188767022"
        data-ad-slot="auto"
        data-ad-format="auto"
        data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </div>
'''


def toc_html(sections):
    """Table of contents. sections: list of (id, title)"""
    items = "\n".join(
        f'        <li><a href="#{h(sid)}">{h(title)}</a></li>'
        for sid, title in sections
    )
    return f'''    <nav class="blog-toc">
      <p class="blog-toc-title">目次</p>
      <ol>
{items}
      </ol>
    </nav>
'''


def product_card_html(p, index=None):
    """Individual product section in article"""
    prefix = f"{index}. " if index else ""
    aff_link = f'../go.html?id={p["id"]}' if p.get("affiliateUrl") else p.get("officialUrl", "#")
    review_link = f'../review.html?id={p["id"]}'

    pros_html = "\n".join(f"          <li>{h(pro)}</li>" for pro in p.get("pros", []))
    cons_html = "\n".join(f"          <li>{h(con)}</li>" for con in p.get("cons", []))
    features_html = "\n".join(f"          <li>{h(f)}</li>" for f in p.get("features", []))

    return f'''    <div class="blog-product-card" id="product-{h(p['id'])}">
      <div class="blog-product-header">
        <h3>{prefix}{h(p["name"])}</h3>
        <span class="blog-rating">{star_rating_html(p.get("rating", 0))}</span>
        <span class="blog-price">{h(p.get("price", ""))}</span>
      </div>
      <p>{h(p.get("summary", ""))}</p>
      <p>{h(p.get("description", ""))}</p>
      <div class="blog-pros-cons">
        <div class="blog-pros">
          <h4>メリット</h4>
          <ul>
{pros_html}
          </ul>
        </div>
        <div class="blog-cons">
          <h4>デメリット</h4>
          <ul>
{cons_html}
          </ul>
        </div>
      </div>
      <div class="blog-features">
        <h4>主な機能・特徴</h4>
        <ul>
{features_html}
        </ul>
      </div>
      <div class="blog-card-actions">
        <a href="{h(aff_link)}" class="blog-cta" target="_blank" rel="noopener noreferrer nofollow">公式サイトを見る</a>
        <a href="{h(review_link)}" class="blog-review-link">詳細レビューを読む &rarr;</a>
      </div>
    </div>
'''


def comparison_table_html(products, columns=None):
    """Generate comparison table for products"""
    if columns is None:
        columns = [("ツール名", "name"), ("料金", "price"), ("評価", "rating"), ("特徴", "features")]

    rows = []
    for p in products:
        cells = []
        for label, key in columns:
            if key == "name":
                cells.append(f'<td><strong>{h(p["name"])}</strong></td>')
            elif key == "rating":
                cells.append(f'<td>{star_rating_html(p.get("rating", 0))}</td>')
            elif key == "features":
                feat_text = " / ".join(p.get("features", [])[:3])
                cells.append(f"<td>{h(feat_text)}</td>")
            else:
                cells.append(f"<td>{h(p.get(key, ''))}</td>")
        rows.append("          <tr>" + "".join(cells) + "</tr>")

    header_cells = "".join(f"<th>{h(label)}</th>" for label, _ in columns)

    return f'''    <div class="blog-comparison-table">
      <table>
        <thead>
          <tr>{header_cells}</tr>
        </thead>
        <tbody>
{"\\n".join(rows)}
        </tbody>
      </table>
    </div>
'''


def vs_table_html(p1, p2):
    """Side-by-side comparison table for A vs B articles"""
    rows_data = [
        ("料金", p1.get("price", ""), p2.get("price", "")),
        ("評価", f'{p1.get("rating", 0)}/5', f'{p2.get("rating", 0)}/5'),
        ("主な特徴", " / ".join(p1.get("features", [])[:3]), " / ".join(p2.get("features", [])[:3])),
        ("メリット数", f'{len(p1.get("pros", []))}点', f'{len(p2.get("pros", []))}点'),
        ("デメリット数", f'{len(p1.get("cons", []))}点', f'{len(p2.get("cons", []))}点'),
    ]
    rows = []
    for label, v1, v2 in rows_data:
        rows.append(f"          <tr><th>{h(label)}</th><td>{h(v1)}</td><td>{h(v2)}</td></tr>")

    return f'''    <div class="blog-vs-table">
      <table>
        <thead>
          <tr><th>比較項目</th><th>{h(p1["name"])}</th><th>{h(p2["name"])}</th></tr>
        </thead>
        <tbody>
{"\\n".join(rows)}
        </tbody>
      </table>
    </div>
'''


# ============================================================
# Article Generators
# ============================================================

def generate_category_roundup(cat_id, products):
    """Generate category roundup article"""
    cat_name = CATEGORY_NAMES.get(cat_id, cat_id)
    prods = sorted(
        [p for p in products if p["category"] == cat_id and p.get("status") == "active"],
        key=lambda x: -x.get("rating", 0),
    )
    if not prods:
        return None

    n = len(prods)
    title = f"【{YEAR}年版】おすすめの{cat_name}{n}選｜料金・機能を徹底比較"
    desc = f"{YEAR}年最新のおすすめ{cat_name}を{n}製品厳選。料金・機能・メリット・デメリットを徹底比較し、あなたに最適な{cat_name}の選び方を解説します。"
    filename = f"{cat_id}-tools-comparison.html"
    url = f"{SITE_URL}/blog/{filename}"

    intro = CATEGORY_INTROS.get(cat_id, f"{cat_name}の人気サービスを{YEAR}年版として徹底比較します。").format(year=YEAR)

    # TOC sections
    toc_sections = [
        ("intro", f"{cat_name}の選び方"),
        ("comparison", "比較一覧表"),
    ]
    for i, p in enumerate(prods, 1):
        toc_sections.append((f"product-{p['id']}", f"{i}. {p['name']}"))
    toc_sections.append(("conclusion", "まとめ"))

    # Build article body
    body_parts = []
    body_parts.append(f'    <h2 id="intro">{cat_name}の選び方</h2>')
    body_parts.append(f"    <p>{h(intro)}</p>")
    body_parts.append(f"    <p>今回は{n}つの{cat_name}サービスを、評価が高い順に紹介します。それぞれの料金体系、主な機能、メリット・デメリットを詳しく解説しますので、ぜひ参考にしてください。</p>")

    body_parts.append(f'    <h2 id="comparison">{cat_name}比較一覧表</h2>')
    body_parts.append(f"    <p>まずは{n}サービスの主要スペックを一覧で比較します。</p>")
    body_parts.append(comparison_table_html(prods))

    # Insert ad after table
    body_parts.append(adsense_mid_article())

    for i, p in enumerate(prods, 1):
        body_parts.append(product_card_html(p, index=i))

    body_parts.append(f'    <h2 id="conclusion">まとめ</h2>')
    if prods:
        top = prods[0]
        body_parts.append(f"    <p>{YEAR}年おすすめの{cat_name}{n}選を紹介しました。総合的に最も評価が高いのは<strong>{h(top['name'])}</strong>（評価: {top.get('rating', 0)}/5）です。")
        body_parts.append(f"    ただし、最適なサービスは用途や予算によって異なります。各サービスの詳細レビューページも用意していますので、気になるサービスがあればぜひチェックしてみてください。</p>")
    body_parts.append(f'    <p>各ツールの詳細は<a href="../index.html#all-products">全ツール一覧</a>からもご確認いただけます。</p>')

    content = "\n".join(body_parts)
    article_text_len = sum(len(p.get("description", "")) + len(p.get("summary", "")) for p in prods) + len(intro) + 500
    rt = reading_time(article_text_len)

    html_str = head_html(title, desc, url)
    html_str += schema_article_jsonld(title, desc, url, GENERATE_DATE)
    html_str += breadcrumb_jsonld([
        ("ホーム", f"{SITE_URL}/"),
        ("ブログ", f"{SITE_URL}/blog/"),
        (title, url),
    ])
    html_str += header_html()
    html_str += breadcrumb_html([
        ("ホーム", "../index.html"),
        ("ブログ", "index.html"),
        (title, None),
    ])
    html_str += f'''  <article class="blog-article">
    <div class="container">
    <h1>{h(title)}</h1>
    <div class="blog-meta">
      <span class="article-updated">更新日: {GENERATE_DATE}</span>
      <span class="blog-meta-cat">{h(cat_name)}</span>
      <span class="blog-meta-count">{n}製品</span>
      <span class="blog-meta-time">読了: 約{rt}分</span>
    </div>
{toc_html(toc_sections)}
{content}
    </div>
  </article>
'''
    html_str += footer_html()

    return filename, html_str, title, desc, cat_name, n


def generate_free_tools_article(cat_id, products):
    """Generate free tools article for a category"""
    cat_name = CATEGORY_NAMES.get(cat_id, cat_id)
    free_prods = sorted(
        [p for p in products if p["category"] == cat_id and "free" in p.get("tags", []) and p.get("status") == "active"],
        key=lambda x: -x.get("rating", 0),
    )
    paid_prods = sorted(
        [p for p in products if p["category"] == cat_id and "free" not in p.get("tags", []) and p.get("status") == "active"],
        key=lambda x: -x.get("rating", 0),
    )

    if len(free_prods) < 2:
        return None

    n = len(free_prods)
    title = f"無料で使える{cat_name}おすすめ{n}選【{YEAR}年版】"
    desc = f"無料プランや無料トライアルがある{cat_name}を{n}製品厳選。{YEAR}年版として機能・制限・有料版との違いを徹底比較します。"
    filename = f"free-{cat_id}-tools.html"
    url = f"{SITE_URL}/blog/{filename}"

    toc_sections = [
        ("free-intro", "無料で使える理由と注意点"),
        ("free-comparison", "無料ツール比較一覧"),
    ]
    for i, p in enumerate(free_prods, 1):
        toc_sections.append((f"product-{p['id']}", f"{i}. {p['name']}"))
    if paid_prods:
        toc_sections.append(("paid-comparison", "有料版との比較"))
    toc_sections.append(("conclusion", "まとめ"))

    body_parts = []
    body_parts.append(f'    <h2 id="free-intro">無料で使える{cat_name}の選び方</h2>')
    body_parts.append(f"    <p>{cat_name}には無料プランや無料トライアルを提供しているサービスが多数あります。コストをかけずに始められるため、初めて{cat_name}を使う方や、まずは試してみたいという方におすすめです。</p>")
    body_parts.append(f"    <p>ただし、無料プランには機能制限や容量制限がある場合があります。本記事では各サービスの無料プランでできることと制限事項を詳しく解説し、最適な選択をサポートします。</p>")

    body_parts.append(f'    <h2 id="free-comparison">無料{cat_name}比較一覧</h2>')
    body_parts.append(comparison_table_html(free_prods))

    body_parts.append(adsense_mid_article())

    for i, p in enumerate(free_prods, 1):
        body_parts.append(product_card_html(p, index=i))

    if paid_prods:
        body_parts.append(f'    <h2 id="paid-comparison">有料版との比較</h2>')
        body_parts.append(f"    <p>無料ツールで物足りなくなったら、以下の有料サービスへのアップグレードも検討しましょう。</p>")
        body_parts.append(comparison_table_html(paid_prods[:3]))
        for p in paid_prods[:3]:
            aff = f'../go.html?id={p["id"]}' if p.get("affiliateUrl") else p.get("officialUrl", "#")
            body_parts.append(f'    <p><strong>{h(p["name"])}</strong>: {h(p.get("summary", ""))} <a href="{h(aff)}" target="_blank" rel="noopener noreferrer nofollow">詳細を見る</a> / <a href="../review.html?id={p["id"]}">レビュー</a></p>')

    body_parts.append(f'    <h2 id="conclusion">まとめ</h2>')
    body_parts.append(f"    <p>無料で使える{cat_name}を{n}選ご紹介しました。無料プランでも十分な機能を持つサービスが増えていますので、まずは気になるサービスを試してみることをおすすめします。")
    body_parts.append(f"    より高度な機能が必要になった場合は、有料プランへのアップグレードも検討してみてください。</p>")

    content = "\n".join(body_parts)
    article_text_len = sum(len(p.get("description", "")) for p in free_prods) + 800
    rt = reading_time(article_text_len)

    html_str = head_html(title, desc, url)
    html_str += schema_article_jsonld(title, desc, url, GENERATE_DATE)
    html_str += breadcrumb_jsonld([
        ("ホーム", f"{SITE_URL}/"),
        ("ブログ", f"{SITE_URL}/blog/"),
        (title, url),
    ])
    html_str += header_html()
    html_str += breadcrumb_html([
        ("ホーム", "../index.html"),
        ("ブログ", "index.html"),
        (title, None),
    ])
    html_str += f'''  <article class="blog-article">
    <div class="container">
    <h1>{h(title)}</h1>
    <div class="blog-meta">
      <span class="article-updated">更新日: {GENERATE_DATE}</span>
      <span class="blog-meta-cat">{h(cat_name)}</span>
      <span class="blog-meta-count">{n}製品</span>
      <span class="blog-meta-time">読了: 約{rt}分</span>
    </div>
{toc_html(toc_sections)}
{content}
    </div>
  </article>
'''
    html_str += footer_html()

    return filename, html_str, title, desc, cat_name, n


def generate_tag_article(tag, tag_ja, tag_desc_intro, products):
    """Generate tag-based article"""
    TAG_FILENAMES = {
        "japanese": "japanese-tools.html",
        "free": "free-plan-tools.html",
        "api": "api-tools.html",
        "nocard": "no-credit-card-tools.html",
    }
    TAG_TITLES = {
        "japanese": f"日本語対応ツールまとめ{len([p for p in products if 'japanese' in p.get('tags',[])])}選【{YEAR}年版】",
        "free": f"無料プランがあるツール一覧{len([p for p in products if 'free' in p.get('tags',[])])}選【{YEAR}年版】",
        "api": f"API連携できるツールまとめ{len([p for p in products if 'api' in p.get('tags',[])])}選【{YEAR}年版】",
        "nocard": f"カード不要で始められるツール一覧{len([p for p in products if 'nocard' in p.get('tags',[])])}選【{YEAR}年版】",
    }

    tagged_prods = sorted(
        [p for p in products if tag in p.get("tags", []) and p.get("status") == "active"],
        key=lambda x: -x.get("rating", 0),
    )
    if not tagged_prods:
        return None

    n = len(tagged_prods)
    title = TAG_TITLES.get(tag, f"{tag_ja}ツールまとめ【{YEAR}年版】")
    desc = f"{tag_ja}の{n}製品を一覧で紹介。{YEAR}年最新の情報で料金・機能を比較します。"
    filename = TAG_FILENAMES[tag]
    url = f"{SITE_URL}/blog/{filename}"

    # Group by category
    cats_in_tag = {}
    for p in tagged_prods:
        cat = p["category"]
        if cat not in cats_in_tag:
            cats_in_tag[cat] = []
        cats_in_tag[cat].append(p)

    toc_sections = [("overview", "概要")]
    for cat_id in cats_in_tag:
        cn = CATEGORY_NAMES.get(cat_id, cat_id)
        toc_sections.append((f"cat-{cat_id}", cn))
    toc_sections.append(("conclusion", "まとめ"))

    body_parts = []
    body_parts.append(f'    <h2 id="overview">概要</h2>')
    body_parts.append(f"    <p>{h(tag_desc_intro)}</p>")
    body_parts.append(f"    <p>全{n}製品を{len(cats_in_tag)}カテゴリに分けて紹介します。</p>")

    body_parts.append(comparison_table_html(tagged_prods[:20]))
    body_parts.append(adsense_mid_article())

    for cat_id, cat_prods in cats_in_tag.items():
        cn = CATEGORY_NAMES.get(cat_id, cat_id)
        body_parts.append(f'    <h2 id="cat-{cat_id}">{h(cn)}（{len(cat_prods)}製品）</h2>')
        for p in cat_prods:
            aff = f'../go.html?id={p["id"]}' if p.get("affiliateUrl") else p.get("officialUrl", "#")
            body_parts.append(f'''    <div class="blog-product-card" id="product-{h(p['id'])}">
      <div class="blog-product-header">
        <h3>{h(p["name"])}</h3>
        <span class="blog-rating">{star_rating_html(p.get("rating", 0))}</span>
        <span class="blog-price">{h(p.get("price", ""))}</span>
      </div>
      <p>{h(p.get("summary", ""))}</p>
      <div class="blog-card-actions">
        <a href="{h(aff)}" class="blog-cta" target="_blank" rel="noopener noreferrer nofollow">公式サイトを見る</a>
        <a href="../review.html?id={p['id']}" class="blog-review-link">詳細レビューを読む &rarr;</a>
      </div>
    </div>
''')

    body_parts.append(f'    <h2 id="conclusion">まとめ</h2>')
    body_parts.append(f"    <p>{tag_ja}の{n}製品をカテゴリ別にご紹介しました。目的や用途に合わせて最適なツールを選んでみてください。各ツールの詳細レビューは個別ページでご確認いただけます。</p>")

    content = "\n".join(body_parts)
    rt = reading_time(n * 100 + 500)

    html_str = head_html(title, desc, url)
    html_str += schema_article_jsonld(title, desc, url, GENERATE_DATE)
    html_str += breadcrumb_jsonld([
        ("ホーム", f"{SITE_URL}/"),
        ("ブログ", f"{SITE_URL}/blog/"),
        (title, url),
    ])
    html_str += header_html()
    html_str += breadcrumb_html([
        ("ホーム", "../index.html"),
        ("ブログ", "index.html"),
        (title, None),
    ])
    html_str += f'''  <article class="blog-article">
    <div class="container">
    <h1>{h(title)}</h1>
    <div class="blog-meta">
      <span class="article-updated">更新日: {GENERATE_DATE}</span>
      <span class="blog-meta-count">{n}製品</span>
      <span class="blog-meta-time">読了: 約{rt}分</span>
    </div>
{toc_html(toc_sections)}
{content}
    </div>
  </article>
'''
    html_str += footer_html()

    return filename, html_str, title, desc, tag_ja, n


def generate_vs_article(p1, p2, cat_id):
    """Generate A vs B comparison article"""
    cat_name = CATEGORY_NAMES.get(cat_id, cat_id)
    title = f"{p1['name']} vs {p2['name']}｜徹底比較【{YEAR}年版】"
    desc = f"{p1['name']}と{p2['name']}を{YEAR}年最新情報で徹底比較。料金・機能・メリット・デメリットからどちらがおすすめか解説します。"
    filename = f"{p1['id']}-vs-{p2['id']}.html"
    url = f"{SITE_URL}/blog/{filename}"

    toc_sections = [
        ("overview", "比較概要"),
        ("table", "スペック比較表"),
        (f"product-{p1['id']}", f"{p1['name']}の特徴"),
        (f"product-{p2['id']}", f"{p2['name']}の特徴"),
        ("which", "どちらを選ぶべき？"),
        ("conclusion", "まとめ"),
    ]

    body_parts = []
    body_parts.append(f'    <h2 id="overview">比較概要</h2>')
    body_parts.append(f"    <p>{cat_name}カテゴリで人気の{h(p1['name'])}と{h(p2['name'])}。どちらも高い評価を受けているサービスですが、料金体系や機能には違いがあります。本記事では両サービスを徹底的に比較し、あなたに合った選択をサポートします。</p>")

    body_parts.append(f'    <h2 id="table">スペック比較表</h2>')
    body_parts.append(vs_table_html(p1, p2))

    body_parts.append(adsense_mid_article())

    body_parts.append(f'    <h2 id="product-{p1["id"]}">{h(p1["name"])}の特徴</h2>')
    body_parts.append(f"    <p>{h(p1.get('description', p1.get('summary', '')))}</p>")
    pros1 = "\n".join(f"      <li>{h(x)}</li>" for x in p1.get("pros", []))
    cons1 = "\n".join(f"      <li>{h(x)}</li>" for x in p1.get("cons", []))
    body_parts.append(f'''    <div class="blog-pros-cons">
      <div class="blog-pros"><h4>メリット</h4><ul>
{pros1}
      </ul></div>
      <div class="blog-cons"><h4>デメリット</h4><ul>
{cons1}
      </ul></div>
    </div>''')
    aff1 = f'../go.html?id={p1["id"]}' if p1.get("affiliateUrl") else p1.get("officialUrl", "#")
    body_parts.append(f'    <p><a href="{h(aff1)}" class="blog-cta" target="_blank" rel="noopener noreferrer nofollow">{h(p1["name"])}の公式サイトを見る</a> <a href="../review.html?id={p1["id"]}" class="blog-review-link">詳細レビュー</a></p>')

    body_parts.append(f'    <h2 id="product-{p2["id"]}">{h(p2["name"])}の特徴</h2>')
    body_parts.append(f"    <p>{h(p2.get('description', p2.get('summary', '')))}</p>")
    pros2 = "\n".join(f"      <li>{h(x)}</li>" for x in p2.get("pros", []))
    cons2 = "\n".join(f"      <li>{h(x)}</li>" for x in p2.get("cons", []))
    body_parts.append(f'''    <div class="blog-pros-cons">
      <div class="blog-pros"><h4>メリット</h4><ul>
{pros2}
      </ul></div>
      <div class="blog-cons"><h4>デメリット</h4><ul>
{cons2}
      </ul></div>
    </div>''')
    aff2 = f'../go.html?id={p2["id"]}' if p2.get("affiliateUrl") else p2.get("officialUrl", "#")
    body_parts.append(f'    <p><a href="{h(aff2)}" class="blog-cta" target="_blank" rel="noopener noreferrer nofollow">{h(p2["name"])}の公式サイトを見る</a> <a href="../review.html?id={p2["id"]}" class="blog-review-link">詳細レビュー</a></p>')

    body_parts.append(f'    <h2 id="which">どちらを選ぶべき？</h2>')
    # Determine recommendation based on characteristics
    if p1.get("rating", 0) > p2.get("rating", 0):
        body_parts.append(f"    <p>総合評価では<strong>{h(p1['name'])}</strong>がやや上回っています（{p1.get('rating',0)} vs {p2.get('rating',0)}）。")
    elif p2.get("rating", 0) > p1.get("rating", 0):
        body_parts.append(f"    <p>総合評価では<strong>{h(p2['name'])}</strong>がやや上回っています（{p2.get('rating',0)} vs {p1.get('rating',0)}）。")
    else:
        body_parts.append(f"    <p>総合評価は両サービスとも{p1.get('rating',0)}と同等です。")

    body_parts.append(f"    ただし、最適な選択は用途や予算によって異なります。以下を参考に判断してみてください。</p>")
    body_parts.append(f"    <ul>")
    body_parts.append(f"      <li><strong>{h(p1['name'])}</strong>がおすすめ: {h(p1.get('pros', [''])[0] if p1.get('pros') else '')}を重視する方</li>")
    body_parts.append(f"      <li><strong>{h(p2['name'])}</strong>がおすすめ: {h(p2.get('pros', [''])[0] if p2.get('pros') else '')}を重視する方</li>")
    body_parts.append(f"    </ul>")

    body_parts.append(f'    <h2 id="conclusion">まとめ</h2>')
    body_parts.append(f"    <p>{h(p1['name'])}と{h(p2['name'])}の徹底比較をお届けしました。両サービスともに{cat_name}として優れた選択肢です。まずは無料トライアルや無料プランがあれば試してみて、自分の用途に合うかどうかを確認することをおすすめします。</p>")

    content = "\n".join(body_parts)
    text_len = len(p1.get("description", "")) + len(p2.get("description", "")) + 1000
    rt = reading_time(text_len)

    html_str = head_html(title, desc, url)
    html_str += schema_article_jsonld(title, desc, url, GENERATE_DATE)
    html_str += breadcrumb_jsonld([
        ("ホーム", f"{SITE_URL}/"),
        ("ブログ", f"{SITE_URL}/blog/"),
        (title, url),
    ])
    html_str += header_html()
    html_str += breadcrumb_html([
        ("ホーム", "../index.html"),
        ("ブログ", "index.html"),
        (title, None),
    ])
    html_str += f'''  <article class="blog-article">
    <div class="container">
    <h1>{h(title)}</h1>
    <div class="blog-meta">
      <span class="article-updated">更新日: {GENERATE_DATE}</span>
      <span class="blog-meta-cat">{h(cat_name)}</span>
      <span class="blog-meta-time">読了: 約{rt}分</span>
    </div>
{toc_html(toc_sections)}
{content}
    </div>
  </article>
'''
    html_str += footer_html()

    return filename, html_str, title, desc, cat_name


def generate_ranking_article(products):
    """Generate top 20 ranking article"""
    top_prods = sorted(
        [p for p in products if p.get("status") == "active"],
        key=lambda x: (-x.get("rating", 0), x.get("name", "")),
    )[:20]

    title = f"ビジネスツールおすすめランキングTOP20【{YEAR}年版】"
    desc = f"{YEAR}年最新のビジネスツールランキングTOP20。全カテゴリから評価の高い厳選ツールを紹介。料金・機能・口コミで徹底比較します。"
    filename = "best-tools-ranking.html"
    url = f"{SITE_URL}/blog/{filename}"

    toc_sections = [("overview", "ランキング概要"), ("ranking-table", "TOP20一覧")]
    for i, p in enumerate(top_prods, 1):
        toc_sections.append((f"product-{p['id']}", f"第{i}位: {p['name']}"))
    toc_sections.append(("conclusion", "まとめ"))

    body_parts = []
    body_parts.append(f'    <h2 id="overview">ランキング概要</h2>')
    body_parts.append(f"    <p>当サイトに掲載している{len(products)}以上のビジネスツール・Webサービスの中から、ユーザー評価の高いTOP20をランキング形式でご紹介します。レンタルサーバー、AI、VPN、デザインなど全カテゴリから厳選しました。</p>")

    body_parts.append(f'    <h2 id="ranking-table">TOP20一覧</h2>')
    # Ranking table with rank
    rows = []
    for i, p in enumerate(top_prods, 1):
        cat_name = CATEGORY_NAMES.get(p["category"], p["category"])
        rows.append(f'          <tr><td><strong>{i}</strong></td><td><strong>{h(p["name"])}</strong></td><td>{h(cat_name)}</td><td>{star_rating_html(p.get("rating", 0))}</td><td>{h(p.get("price", ""))}</td></tr>')
    body_parts.append(f'''    <div class="blog-comparison-table">
      <table>
        <thead><tr><th>順位</th><th>ツール名</th><th>カテゴリ</th><th>評価</th><th>料金</th></tr></thead>
        <tbody>
{"\\n".join(rows)}
        </tbody>
      </table>
    </div>
''')

    body_parts.append(adsense_mid_article())

    for i, p in enumerate(top_prods, 1):
        cat_name = CATEGORY_NAMES.get(p["category"], p["category"])
        aff = f'../go.html?id={p["id"]}' if p.get("affiliateUrl") else p.get("officialUrl", "#")
        pros = "\n".join(f"          <li>{h(x)}</li>" for x in p.get("pros", [])[:3])
        body_parts.append(f'''    <div class="blog-product-card" id="product-{h(p['id'])}">
      <div class="blog-product-header">
        <h3>第{i}位: {h(p["name"])}</h3>
        <span class="blog-rating">{star_rating_html(p.get("rating", 0))}</span>
        <span class="blog-price">{h(p.get("price", ""))}</span>
      </div>
      <p class="blog-meta-cat" style="margin-bottom:8px;">{h(cat_name)}</p>
      <p>{h(p.get("description", p.get("summary", "")))}</p>
      <div class="blog-pros">
        <h4>おすすめポイント</h4>
        <ul>
{pros}
        </ul>
      </div>
      <div class="blog-card-actions">
        <a href="{h(aff)}" class="blog-cta" target="_blank" rel="noopener noreferrer nofollow">公式サイトを見る</a>
        <a href="../review.html?id={p['id']}" class="blog-review-link">詳細レビューを読む &rarr;</a>
      </div>
    </div>
''')
        if i == 10:
            body_parts.append(adsense_mid_article())

    body_parts.append(f'    <h2 id="conclusion">まとめ</h2>')
    body_parts.append(f"    <p>{YEAR}年版ビジネスツールおすすめランキングTOP20をお届けしました。第1位の<strong>{h(top_prods[0]['name'])}</strong>を筆頭に、いずれも高品質なサービスばかりです。</p>")
    body_parts.append(f"    <p>ツール選びで迷ったら、まずは無料プランやトライアルで試してみることをおすすめします。全ツールの詳細は<a href='../index.html'>トップページ</a>からご確認いただけます。</p>")

    content = "\n".join(body_parts)
    rt = reading_time(sum(len(p.get("description", "")) for p in top_prods) + 1000)

    html_str = head_html(title, desc, url)
    html_str += schema_article_jsonld(title, desc, url, GENERATE_DATE)
    html_str += breadcrumb_jsonld([
        ("ホーム", f"{SITE_URL}/"),
        ("ブログ", f"{SITE_URL}/blog/"),
        (title, url),
    ])
    html_str += header_html()
    html_str += breadcrumb_html([
        ("ホーム", "../index.html"),
        ("ブログ", "index.html"),
        (title, None),
    ])
    html_str += f'''  <article class="blog-article">
    <div class="container">
    <h1>{h(title)}</h1>
    <div class="blog-meta">
      <span class="article-updated">更新日: {GENERATE_DATE}</span>
      <span class="blog-meta-count">TOP20</span>
      <span class="blog-meta-time">読了: 約{rt}分</span>
    </div>
{toc_html(toc_sections)}
{content}
    </div>
  </article>
'''
    html_str += footer_html()

    return filename, html_str, title, desc, "総合", 20


def generate_blog_index(articles):
    """Generate blog index page with article cards"""
    title = "ブログ記事一覧｜おすすめツール比較ナビ"
    desc = f"おすすめツール比較ナビのブログ記事一覧。{YEAR}年版のツール比較、ランキング、無料ツール特集などの記事をお届けします。"
    url = f"{SITE_URL}/blog/"
    filename = "index.html"

    # Categorize articles
    roundups = [a for a in articles if a["type"] == "roundup"]
    free_arts = [a for a in articles if a["type"] == "free"]
    tag_arts = [a for a in articles if a["type"] == "tag"]
    vs_arts = [a for a in articles if a["type"] == "vs"]
    ranking_arts = [a for a in articles if a["type"] == "ranking"]

    total = len(articles)

    def article_card(a):
        return f'''      <a href="{h(a['filename'])}" class="blog-card">
        <div class="blog-card-tag">{h(a.get("tag_label", ""))}</div>
        <h3 class="blog-card-title">{h(a["title"])}</h3>
        <p class="blog-card-excerpt">{h(a["desc"][:100])}...</p>
        <span class="blog-card-meta">{h(a.get("product_count", ""))}</span>
      </a>
'''

    cards_html_parts = []

    # Ranking first
    if ranking_arts:
        cards_html_parts.append('    <h2>ランキング</h2>')
        cards_html_parts.append('    <div class="blog-card-grid">')
        for a in ranking_arts:
            cards_html_parts.append(article_card(a))
        cards_html_parts.append("    </div>")

    # Category roundups
    if roundups:
        cards_html_parts.append(f'    <h2>カテゴリ別比較（{len(roundups)}記事）</h2>')
        cards_html_parts.append('    <div class="blog-card-grid">')
        for a in sorted(roundups, key=lambda x: x["title"]):
            cards_html_parts.append(article_card(a))
        cards_html_parts.append("    </div>")

    # Free tools
    if free_arts:
        cards_html_parts.append(f'    <h2>無料ツール特集（{len(free_arts)}記事）</h2>')
        cards_html_parts.append('    <div class="blog-card-grid">')
        for a in sorted(free_arts, key=lambda x: x["title"]):
            cards_html_parts.append(article_card(a))
        cards_html_parts.append("    </div>")

    # Tag articles
    if tag_arts:
        cards_html_parts.append(f'    <h2>特集記事（{len(tag_arts)}記事）</h2>')
        cards_html_parts.append('    <div class="blog-card-grid">')
        for a in tag_arts:
            cards_html_parts.append(article_card(a))
        cards_html_parts.append("    </div>")

    # VS articles
    if vs_arts:
        cards_html_parts.append(f'    <h2>VS 比較（{len(vs_arts)}記事）</h2>')
        cards_html_parts.append('    <div class="blog-card-grid">')
        for a in sorted(vs_arts, key=lambda x: x["title"]):
            cards_html_parts.append(article_card(a))
        cards_html_parts.append("    </div>")

    cards_html = "\n".join(cards_html_parts)

    html_str = head_html(title, desc, url, og_type="website")
    html_str += breadcrumb_jsonld([
        ("ホーム", f"{SITE_URL}/"),
        ("ブログ", url),
    ])
    html_str += header_html()
    html_str += breadcrumb_html([
        ("ホーム", "../index.html"),
        ("ブログ", None),
    ])
    html_str += f'''  <section class="blog-article">
    <div class="container">
    <h1>ブログ記事一覧</h1>
    <p class="blog-index-sub">ツールの比較・ランキング・特集記事を{total}本公開中。{YEAR}年の最新情報でお届けします。</p>

{cards_html}

    </div>
  </section>
'''
    html_str += footer_html()

    return filename, html_str


# ============================================================
# Main
# ============================================================

def main():
    products, config = load_data()
    os.makedirs(BLOG_DIR, exist_ok=True)

    articles = []  # metadata for index
    generated_files = []

    # 1. Category Roundups (19)
    print("Generating category roundup articles...")
    for cat in config["categories"]:
        cat_id = cat["id"]
        result = generate_category_roundup(cat_id, products)
        if result:
            filename, html_content, title, desc, cat_name, n = result
            filepath = os.path.join(BLOG_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            articles.append({
                "type": "roundup",
                "filename": filename,
                "title": title,
                "desc": desc,
                "tag_label": cat_name,
                "product_count": f"{n}製品比較",
            })
            generated_files.append(filename)
            print(f"  {filename} ({n} products)")

    # 2. Free Tools Articles
    print("Generating free tools articles...")
    for cat in config["categories"]:
        cat_id = cat["id"]
        result = generate_free_tools_article(cat_id, products)
        if result:
            filename, html_content, title, desc, cat_name, n = result
            filepath = os.path.join(BLOG_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            articles.append({
                "type": "free",
                "filename": filename,
                "title": title,
                "desc": desc,
                "tag_label": f"無料 {cat_name}",
                "product_count": f"{n}製品",
            })
            generated_files.append(filename)
            print(f"  {filename} ({n} free products)")

    # 3. Tag-based Articles
    print("Generating tag-based articles...")
    tag_configs = [
        ("japanese", "日本語対応ツール", f"海外サービスが多いなか、日本語に対応しているツールは日本のユーザーにとって大きなメリットです。本記事では{YEAR}年現在、日本語で利用できるビジネスツール・Webサービスをカテゴリ別にまとめました。"),
        ("free", "無料プランがあるツール", f"コストをかけずにスタートできる無料プランは、初めてツールを導入する方に最適です。{YEAR}年版として、無料プラン・無料トライアルがあるツールを全カテゴリからまとめました。"),
        ("api", "API連携できるツール", f"他のサービスやシステムと連携させるためにAPIは不可欠。{YEAR}年版として、API連携に対応したビジネスツールをカテゴリ別にまとめました。自動化やワークフロー構築に役立ちます。"),
        ("nocard", "カード不要で始められるツール", f"クレジットカードなしでも利用開始できるツールをまとめました。{YEAR}年版として、アカウント作成だけで始められるサービスをカテゴリ別にご紹介します。"),
    ]
    for tag, tag_ja, intro in tag_configs:
        result = generate_tag_article(tag, tag_ja, intro, products)
        if result:
            filename, html_content, title, desc, tag_label, n = result
            filepath = os.path.join(BLOG_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            articles.append({
                "type": "tag",
                "filename": filename,
                "title": title,
                "desc": desc,
                "tag_label": tag_label,
                "product_count": f"{n}製品",
            })
            generated_files.append(filename)
            print(f"  {filename} ({n} products)")

    # 4. Comparison (VS) Articles
    print("Generating VS comparison articles...")
    for cat in config["categories"]:
        cat_id = cat["id"]
        cat_prods = sorted(
            [p for p in products if p["category"] == cat_id and p.get("status") == "active"],
            key=lambda x: -x.get("rating", 0),
        )
        if len(cat_prods) >= 4:
            p1, p2 = cat_prods[0], cat_prods[1]
            result = generate_vs_article(p1, p2, cat_id)
            if result:
                filename, html_content, title, desc, cat_name = result
                filepath = os.path.join(BLOG_DIR, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(html_content)
                articles.append({
                    "type": "vs",
                    "filename": filename,
                    "title": title,
                    "desc": desc,
                    "tag_label": f"VS比較 ({cat_name})",
                    "product_count": "2製品比較",
                })
                generated_files.append(filename)
                print(f"  {filename}")

    # 5. Top Ranking Article
    print("Generating ranking article...")
    result = generate_ranking_article(products)
    if result:
        filename, html_content, title, desc, _, n = result
        filepath = os.path.join(BLOG_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        articles.append({
            "type": "ranking",
            "filename": filename,
            "title": title,
            "desc": desc,
            "tag_label": "ランキング",
            "product_count": f"TOP{n}",
        })
        generated_files.append(filename)
        print(f"  {filename} (TOP{n})")

    # 6. Blog Index
    print("Generating blog index...")
    filename, html_content = generate_blog_index(articles)
    filepath = os.path.join(BLOG_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    generated_files.append(filename)
    print(f"  {filename} ({len(articles)} articles)")

    # Summary
    print(f"\nDone! Generated {len(generated_files)} files in blog/")
    print(f"  Category roundups: {len([a for a in articles if a['type']=='roundup'])}")
    print(f"  Free tools: {len([a for a in articles if a['type']=='free'])}")
    print(f"  Tag articles: {len([a for a in articles if a['type']=='tag'])}")
    print(f"  VS comparisons: {len([a for a in articles if a['type']=='vs'])}")
    print(f"  Ranking: {len([a for a in articles if a['type']=='ranking'])}")
    print(f"  Index: 1")

    return generated_files


if __name__ == "__main__":
    main()
