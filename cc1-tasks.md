# CC1 タスク指示書（自動通信プロトコル）

## 通信プロトコル
- このファイルは **司令塔（メインCC）** と **CC1** の双方向通信チャネルである
- CC1は「未着手」のタスクを見つけたら即座に実行すること
- タスク完了後は「状態」を `完了` に、実施内容を「報告」に記入
- エラーや不明点は「報告」に記入して状態を `要確認` にする
- **全タスク完了後、最終行の `SIGNAL: CC1_DONE` を記入すること**
- 司令塔がレビュー後、追加タスクがあれば本ファイルに追記する
- 1タスクずつ順番に実行すること
- コミット・プッシュはデプロイタスクの指示に従うこと

---

## タスク7: sitemap.xml 更新（両サイト）
**状態**: 完了
**内容**:

### 7-1: ツール比較ナビ
`G:\シンプルマネタイズシステム\sitemap.xml` を再生成する。

含めるURL一覧:
- `https://tools.freesozo.com/` (priority: 1.0, changefreq: daily)
- `https://tools.freesozo.com/privacy.html` (priority: 0.3)
- `https://tools.freesozo.com/review.html?id={各商品ID}` (priority: 0.8, changefreq: weekly)
  - products.json の全 active 商品分（102件）

`manage.sh update` が使えるならそれを使う。使えなければ手動でsitemap.xmlを生成すること。
lastmod は `2026-03-01` で統一。

### 7-2: フリー素材ポータル
`G:\freesitePortal Site\sitemap.xml` を再生成する。

含めるURL一覧:
- `https://freesozo.com/` (priority: 1.0, changefreq: daily)
- `https://freesozo.com/category.html` (priority: 0.8, changefreq: weekly)
- `https://freesozo.com/privacy.html` (priority: 0.3)
- `https://freesozo.com/detail.html?id={各サイトID}` (priority: 0.7, changefreq: weekly)
  - sites.json の全サイト分

`manage.sh update` が使えるならそれを使う。
lastmod は `2026-03-01` で統一。

**報告**: 7-1: ツール比較ナビ sitemap.xml 再生成。104 URL（トップ+privacy+102商品）。lastmod=2026-03-01。7-2: フリー素材ポータル sitemap.xml 再生成。208 URL（トップ+category+privacy+205サイト）。lastmod=2026-03-01。Pythonで直接生成（manage.shはWindows環境のため不使用）。

---

## タスク8: 内部リンク強化（両サイト）
**状態**: 完了
**内容**:

### 8-1: カテゴリページの相互リンク改善（ポータル）
`G:\freesitePortal Site\js\app.js` の `cardHTML()` 関数で、各カードにカテゴリリンクを追加する。
カード内のカテゴリ名をクリックすると `category.html?cat={categoryId}` に遷移するようにする。
現在のカテゴリ表示がただのテキストならリンク化する。既にリンクなら変更不要。

### 8-2: 関連ツール表示の強化（ツール比較ナビ）
`G:\シンプルマネタイズシステム\js\app.js` の `initReviewPage()` 内の関連ツールセクションを確認。
同カテゴリのツールが表示されているか確認し、表示されていなければ同カテゴリから最大4件を表示するように修正。

### 8-3: 姉妹サイトバナー追加（両サイト）
両サイトのフッター上部に、姉妹サイトへの誘導バナーを追加する。

**ツール比較ナビ** (`G:\シンプルマネタイズシステム\index.html`) のフッター直前に:
```html
<section class="sister-banner">
  <div class="container">
    <p>🎨 無料素材を探すなら → <a href="https://freesozo.com/" target="_blank" rel="noopener"><strong>フリー素材ポータル</strong></a> - 200以上の無料素材サイトを比較</p>
  </div>
</section>
```

**フリー素材ポータル** (`G:\freesitePortal Site\index.html`) のフッター直前に:
```html
<section class="sister-banner">
  <div class="container">
    <p>🔧 ビジネスツールを探すなら → <a href="https://tools.freesozo.com/" target="_blank" rel="noopener"><strong>おすすめツール比較ナビ</strong></a> - 100以上のツールを徹底比較</p>
  </div>
</section>
```

CSSは各サイトの `css/style.css` に追加:
```css
.sister-banner {
  background: var(--card-bg, #f0f4ff);
  border-top: 2px solid var(--primary, #4f46e5);
  padding: 16px 0;
  text-align: center;
  font-size: 0.95rem;
}
.sister-banner a {
  color: var(--primary, #4f46e5);
  text-decoration: underline;
}
```
※ CSS変数名は各サイトの既存変数に合わせること。ダークモード対応を忘れずに。

### 8-4: デプロイ
- 両サイトのキャッシュバスティングを v=7 に上げる
- 両サイトをそれぞれ git commit & push

**報告**: 8-1: ポータルのcardHTML内カテゴリ表示を `<span class="tag">` → `<a class="tag" href="category.html?cat=...">` にリンク化。8-2: ツール比較ナビの関連ツール表示に `.slice(0, 4)` を追加し最大4件に制限。8-3: 両サイトのフッター直前に姉妹サイトバナーを追加。CSSは各サイトの変数に合わせて追加（ダークモード対応済み）。8-4: 全HTML v=6→v=7に更新。ツール比較ナビ commit `2104a20` → push完了。ポータル commit `035805e` → push完了。

---

## タスク9: Google Analytics 設置（両サイト）
**状態**: 完了
**内容**:

**重要: サイトごとに測定IDが異なる**
- ポータル（freesozo.com）: **G-TW9TKBPSNW**
- ツール比較ナビ（tools.freesozo.com）: **G-YL05931NPE**

各サイトの全HTMLの `<head>` 内、AdSenseスクリプトの直前にそれぞれのIDで追加:

### ポータル（G-TW9TKBPSNW）
対象: `G:\freesitePortal Site` の index.html, category.html, detail.html, privacy.html, go.html
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TW9TKBPSNW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-TW9TKBPSNW');
</script>
```

### ツール比較ナビ（G-YL05931NPE）
対象: `G:\シンプルマネタイズシステム` の index.html, review.html, privacy.html, go.html
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YL05931NPE"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YL05931NPE');
</script>
```

設置後、両サイトをそれぞれ git commit & push すること。
キャッシュバスティングは v=7 のまま（HTML構造の変更のみ）。

**報告**: ツール比較ナビ(G-YL05931NPE): index.html, review.html, privacy.html, go.html の4ファイルに設置。commit `d4eacbf` → push完了。ポータル(G-TW9TKBPSNW): index.html, category.html, detail.html, privacy.html, go.html の5ファイルに設置。commit `d6737da` → push完了。全ファイルAdSenseスクリプト直前に配置（go.htmlはAdSense無しのため`</head>`直前）。重複挿入なし確認済み。

---

## 完了シグナル
<!-- CC1: 全タスク完了後に下の行を SIGNAL: CC1_DONE に変更すること -->
SIGNAL: CC1_DONE
