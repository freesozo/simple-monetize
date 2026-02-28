#!/bin/bash
# ============================================================
#  シンプルマネタイズシステム - 全自動管理スクリプト
#  Usage: ./manage.sh [command]
#  Commands: auto | validate | check | update | add | report | deploy
# ============================================================

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -W 2>/dev/null || pwd)"
DATA_DIR="$SCRIPT_DIR/data"
PRODUCTS_FILE="$DATA_DIR/products.json"
CONFIG_FILE="$DATA_DIR/config.json"
LOG_FILE="$SCRIPT_DIR/manage.log"
ERRORS=0
WARNINGS=0
FIXES=0

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()  { echo -e "${GREEN}[OK]${NC}   $1"; }
warn(){ echo -e "${YELLOW}[WARN]${NC} $1"; ((WARNINGS++)) || true; }
err() { echo -e "${RED}[ERR]${NC}  $1"; ((ERRORS++)) || true; }
fix() { echo -e "${GREEN}[FIX]${NC}  $1"; ((FIXES++)) || true; }

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

# ============================================================
#  VALIDATE - データ検証
# ============================================================
cmd_validate() {
  log "========== データ検証開始 =========="

  # Check files exist
  if [[ ! -f "$PRODUCTS_FILE" ]]; then
    err "products.json が見つかりません: $PRODUCTS_FILE"
    return 1
  fi
  ok "products.json 存在確認"

  if [[ ! -f "$CONFIG_FILE" ]]; then
    err "config.json が見つかりません: $CONFIG_FILE"
    return 1
  fi
  ok "config.json 存在確認"

  # Validate JSON syntax
  if python3 -c "import json; json.load(open('$PRODUCTS_FILE', encoding='utf-8'))" 2>/dev/null || \
     python -c "import json; json.load(open('$PRODUCTS_FILE', encoding='utf-8'))" 2>/dev/null; then
    ok "products.json JSON構文OK"
  else
    err "products.json JSON構文エラー"
    return 1
  fi

  if python3 -c "import json; json.load(open('$CONFIG_FILE', encoding='utf-8'))" 2>/dev/null || \
     python -c "import json; json.load(open('$CONFIG_FILE', encoding='utf-8'))" 2>/dev/null; then
    ok "config.json JSON構文OK"
  else
    err "config.json JSON構文エラー"
    return 1
  fi

  # Validate product structure
  local product_count
  product_count=$(python3 -c "
import json, sys
with open('$PRODUCTS_FILE', encoding='utf-8') as f:
    data = json.load(f)
products = data.get('products', [])
print(len(products))
required = ['id','name','category','summary','rating','price','status']
errors = 0
for i, p in enumerate(products):
    for key in required:
        if key not in p or not p[key]:
            print(f'ERROR: Product #{i} ({p.get(\"name\",\"unknown\")}) missing: {key}', file=sys.stderr)
            errors += 1
    if 'affiliateUrl' not in p:
        print(f'WARN: Product #{i} ({p.get(\"name\",\"unknown\")}) has no affiliateUrl', file=sys.stderr)
    if p.get('rating', 0) < 1 or p.get('rating', 0) > 5:
        print(f'WARN: Product #{i} ({p.get(\"name\",\"unknown\")}) rating out of range: {p.get(\"rating\")}', file=sys.stderr)
sys.exit(errors)
" 2>&1) || true

  local count
  count=$(echo "$product_count" | head -1)
  ok "商品数: $count 件"

  # Check for duplicate IDs
  local dupes
  dupes=$(python3 -c "
import json
with open('$PRODUCTS_FILE', encoding='utf-8') as f:
    data = json.load(f)
ids = [p['id'] for p in data['products']]
dupes = [x for x in ids if ids.count(x) > 1]
if dupes:
    print(','.join(set(dupes)))
" 2>/dev/null) || true

  if [[ -n "$dupes" ]]; then
    err "重複ID: $dupes"
  else
    ok "ID重複なし"
  fi

  # Check HTML files exist
  for f in index.html review.html privacy.html; do
    if [[ -f "$SCRIPT_DIR/$f" ]]; then
      ok "$f 存在確認"
    else
      warn "$f が見つかりません"
    fi
  done

  log "検証完了: エラー=$ERRORS, 警告=$WARNINGS"
}

# ============================================================
#  CHECK - リンクチェック
# ============================================================
cmd_check() {
  log "========== リンクチェック開始 =========="

  python3 -c "
import json, urllib.request, urllib.error, ssl, sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

with open('$PRODUCTS_FILE', encoding='utf-8') as f:
    products = json.load(f)['products']

ok = 0
fail = 0
skip = 0
results = []

for p in products:
    for label, url in [('affiliate', p.get('affiliateUrl','')), ('official', p.get('officialUrl',''))]:
        if not url or url.startswith('https://px.a8.net') or 'XXXXX' in url:
            print(f'  SKIP  {p[\"name\"]} ({label}): placeholder URL')
            skip += 1
            continue
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=10, context=ctx)
            code = resp.getcode()
            if code < 400:
                print(f'  OK    {p[\"name\"]} ({label}): {code}')
                ok += 1
            else:
                print(f'  FAIL  {p[\"name\"]} ({label}): {code}')
                fail += 1
                results.append({'id': p['id'], 'name': p['name'], 'type': label, 'status': code})
        except Exception as e:
            # Try GET if HEAD fails
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req, timeout=10, context=ctx)
                print(f'  OK    {p[\"name\"]} ({label}): {resp.getcode()} (GET)')
                ok += 1
            except Exception as e2:
                print(f'  FAIL  {p[\"name\"]} ({label}): {e2}')
                fail += 1
                results.append({'id': p['id'], 'name': p['name'], 'type': label, 'status': str(e2)})

print(f'\nResult: OK={ok}, FAIL={fail}, SKIP={skip}')
if fail > 0:
    print('BROKEN LINKS:')
    for r in results:
        print(f'  - {r[\"name\"]} ({r[\"type\"]}): {r[\"status\"]}')
    sys.exit(1)
" 2>&1 && ok "全リンク正常" || warn "壊れたリンクあり（上記参照）"

  log "リンクチェック完了"
}

# ============================================================
#  UPDATE - 自動更新
# ============================================================
cmd_update() {
  log "========== 自動更新開始 =========="

  # Update lastChecked timestamps
  local today
  today=$(date '+%Y-%m-%d')

  python3 -c "
import json
with open('$PRODUCTS_FILE', encoding='utf-8') as f:
    data = json.load(f)
changed = 0
for p in data['products']:
    if p.get('lastChecked') != '$today':
        p['lastChecked'] = '$today'
        changed += 1
with open('$PRODUCTS_FILE', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'Updated lastChecked for {changed} products')
"
  fix "lastChecked を $today に更新"

  # Update config lastUpdated
  python3 -c "
import json
with open('$CONFIG_FILE', encoding='utf-8') as f:
    data = json.load(f)
data['lastUpdated'] = '$today'
with open('$CONFIG_FILE', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
"
  fix "config.json lastUpdated 更新"

  # Generate/update sitemap.xml
  python3 -c "
import json
with open('$CONFIG_FILE', encoding='utf-8') as f:
    config = json.load(f)
with open('$PRODUCTS_FILE', encoding='utf-8') as f:
    products = json.load(f)['products']

base = config.get('siteUrl', '').rstrip('/')
if not base:
    base = '.'

xml = '''<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">
  <url><loc>{base}/index.html</loc><priority>1.0</priority></url>
  <url><loc>{base}/privacy.html</loc><priority>0.3</priority></url>'''.format(base=base)
for p in products:
    if p.get('status') == 'active':
        xml += f'''
  <url><loc>{base}/review.html?id={p[\"id\"]}</loc><priority>0.8</priority></url>'''
xml += '''
</urlset>'''

with open('$SCRIPT_DIR/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(xml)
print(f'sitemap.xml generated with {len(products)+2} URLs')
"
  fix "sitemap.xml 生成完了"

  # Generate robots.txt
  cat > "$SCRIPT_DIR/robots.txt" << 'ROBOTS'
User-agent: *
Allow: /
Sitemap: sitemap.xml
ROBOTS
  fix "robots.txt 生成完了"

  log "自動更新完了: $FIXES 件の更新"
}

# ============================================================
#  ADD - 商品追加
# ============================================================
cmd_add() {
  log "========== 商品追加 =========="
  echo ""
  read -rp "商品ID (英数字, 例: my-product): " pid
  read -rp "商品名: " pname
  echo "カテゴリ: server / vpn / learning / ai / design"
  read -rp "カテゴリID: " pcat
  read -rp "一行説明: " psummary
  read -rp "詳細説明: " pdesc
  read -rp "評価 (1.0-5.0): " prating
  read -rp "価格 (例: ¥990/月〜): " pprice
  read -rp "アフィリエイトURL: " paffurl
  read -rp "公式サイトURL: " pofficialurl
  read -rp "おすすめ (true/false): " pfeatured

  python3 -c "
import json
with open('$PRODUCTS_FILE', encoding='utf-8') as f:
    data = json.load(f)

new_product = {
    'id': '$pid',
    'name': '''$pname''',
    'category': '$pcat',
    'summary': '''$psummary''',
    'description': '''$pdesc''',
    'rating': float('$prating'),
    'price': '''$pprice''',
    'affiliateUrl': '$paffurl',
    'affiliateProvider': 'a8',
    'imageUrl': '',
    'pros': [],
    'cons': [],
    'features': [],
    'officialUrl': '$pofficialurl',
    'lastChecked': '$(date +%Y-%m-%d)',
    'status': 'active',
    'featured': $pfeatured == 'true'
}

# Check duplicate
if any(p['id'] == '$pid' for p in data['products']):
    print('ERROR: ID already exists')
    exit(1)

data['products'].append(new_product)
with open('$PRODUCTS_FILE', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'Added: {new_product[\"name\"]} (ID: {new_product[\"id\"]})')
"
  ok "商品追加完了"
  echo "  ※ pros/cons/features は products.json を直接編集してください"
}

# ============================================================
#  REPORT - レポート生成
# ============================================================
cmd_report() {
  log "========== レポート =========="

  python3 -c "
import json
from collections import Counter

with open('$PRODUCTS_FILE', encoding='utf-8') as f:
    products = json.load(f)['products']
with open('$CONFIG_FILE', encoding='utf-8') as f:
    config = json.load(f)

active = [p for p in products if p.get('status') == 'active']
inactive = [p for p in products if p.get('status') != 'active']
featured = [p for p in active if p.get('featured')]
no_affiliate = [p for p in active if not p.get('affiliateUrl') or 'XXXXX' in p.get('affiliateUrl','')]
categories = Counter(p['category'] for p in active)

print(f'''
{'='*50}
  サイト名: {config.get('siteName', 'N/A')}
  最終更新: {config.get('lastUpdated', 'N/A')}
{'='*50}

【商品統計】
  総商品数:     {len(products)}
  アクティブ:   {len(active)}
  非アクティブ: {len(inactive)}
  おすすめ:     {len(featured)}

【カテゴリ別】''')
for cat, count in sorted(categories.items()):
    print(f'  {cat}: {count}件')

print(f'''
【注意が必要】
  アフィリエイトURL未設定: {len(no_affiliate)}件''')
for p in no_affiliate:
    print(f'    - {p[\"name\"]} ({p[\"id\"]})')

# Average rating
avg = sum(p['rating'] for p in active) / len(active) if active else 0
print(f'''
【平均評価】 {avg:.1f} / 5.0

{'='*50}''')
"
}

# ============================================================
#  DEPLOY - GitHub Pages デプロイ
# ============================================================
cmd_deploy() {
  log "========== デプロイ =========="

  cd "$SCRIPT_DIR"

  if [[ ! -d .git ]]; then
    log "Gitリポジトリ初期化..."
    git init
    git branch -M main
  fi

  git add -A
  if git diff --cached --quiet 2>/dev/null; then
    ok "変更なし - デプロイ不要"
    return
  fi

  git commit -m "auto-update: $(date '+%Y-%m-%d %H:%M')"
  ok "コミット作成"

  if git remote get-url origin &>/dev/null; then
    git push origin main
    ok "プッシュ完了"
  else
    warn "リモートが設定されていません。以下を実行してください:"
    echo "  git remote add origin https://github.com/USERNAME/REPO.git"
    echo "  git push -u origin main"
  fi
}

# ============================================================
#  AUTO - 全自動実行 (更新 → 修正 → 確認)
# ============================================================
cmd_auto() {
  echo ""
  echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║   全自動マネタイズ管理システム       ║${NC}"
  echo -e "${BLUE}║   $(timestamp)            ║${NC}"
  echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
  echo ""

  # Step 1: Update
  cmd_update
  echo ""

  # Step 2: Validate
  cmd_validate
  echo ""

  # Step 3: Check links
  cmd_check
  echo ""

  # Step 4: Report
  cmd_report
  echo ""

  # Summary
  echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║   実行結果サマリー                   ║${NC}"
  echo -e "${BLUE}╠══════════════════════════════════════╣${NC}"
  echo -e "${BLUE}║${NC}  更新: ${GREEN}$FIXES 件${NC}                       ${BLUE}║${NC}"
  echo -e "${BLUE}║${NC}  エラー: ${RED}$ERRORS 件${NC}                     ${BLUE}║${NC}"
  echo -e "${BLUE}║${NC}  警告: ${YELLOW}$WARNINGS 件${NC}                     ${BLUE}║${NC}"
  echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"

  # Log
  echo "[$(timestamp)] auto: fixes=$FIXES errors=$ERRORS warnings=$WARNINGS" >> "$LOG_FILE"
}

# ============================================================
#  HELP
# ============================================================
cmd_help() {
  echo ""
  echo "シンプルマネタイズ管理スクリプト"
  echo ""
  echo "Usage: ./manage.sh [command]"
  echo ""
  echo "Commands:"
  echo "  auto      全自動実行（更新→検証→チェック→レポート）"
  echo "  validate  データの構造・整合性を検証"
  echo "  check     アフィリエイト・公式サイトのリンクチェック"
  echo "  update    タイムスタンプ・sitemap・robots.txt 更新"
  echo "  add       新しい商品を対話的に追加"
  echo "  report    サイト統計レポート表示"
  echo "  deploy    GitHub にコミット＆プッシュ"
  echo "  help      このヘルプを表示"
  echo ""
}

# ============================================================
#  Main
# ============================================================
case "${1:-help}" in
  auto)     cmd_auto ;;
  validate) cmd_validate ;;
  check)    cmd_check ;;
  update)   cmd_update ;;
  add)      cmd_add ;;
  report)   cmd_report ;;
  deploy)   cmd_deploy ;;
  help|*)   cmd_help ;;
esac
