#!/usr/bin/env bash
# 下载可直链获取的数据集到 data/ 下。
# 覆盖：SymMap、Disbiome、HERB、dbPTH。
# 不覆盖：TCMSP / MDIPID / MicrobeTCM / HIT 2.0 —— 这四个没有下载接口，需要爬虫。
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA="${ROOT}/data"
mkdir -p "$DATA"

RETRY_OPTS=(--retry 4 --retry-delay 2 --retry-connrefused -L -C - --fail-with-body -sS)

log()  { printf '\033[1;34m[*]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[!]\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m[+]\033[0m %s\n' "$*"; }

fetch() {  # fetch <url> <outfile>
  local url="$1" out="$2"
  mkdir -p "$(dirname "$out")"
  if curl "${RETRY_OPTS[@]}" -o "$out" "$url"; then
    ok "$(basename "$out")  ($(du -h "$out" | cut -f1))"
  else
    warn "失败: $url"
    rm -f "$out"
    return 1
  fi
}

############################################
# 1. SymMap  —— XLSX/TSV 直链
############################################
log "SymMap → ${DATA}/symmap"
SYMMAP_BASE="http://www.symmap.org/static/download"
for f in SMHB.xlsx SMIT.xlsx SMTT.xlsx SMDE.xlsx SMTS.xlsx SMMS.xlsx SMSY.xlsx; do
  fetch "${SYMMAP_BASE}/${f}" "${DATA}/symmap/${f}" || true
done
warn "若 404：SymMap 的静态文件名随版本变动。"
warn "  打开 http://www.symmap.org/download/ ，右键复制真实链接后替换 SYMMAP_BASE 与文件名。"

############################################
# 2. Disbiome —— REST API（最可靠）
############################################
log "Disbiome → ${DATA}/disbiome"
for ep in experiments organisms diseases publications methods; do
  fetch "https://disbiome.ugent.be/api/disbiome/${ep}" "${DATA}/disbiome/${ep}.json" || true
done
warn "也可用 python3 scripts/fetch_disbiome.py --out ${DATA}/disbiome （带分页与 JSON→CSV 转换）"

############################################
# 3. HERB —— 分表下载
############################################
log "HERB → ${DATA}/herb"
HERB_BASE="http://herb.ac.cn/download"
for f in herb.txt ingredient.txt target.txt disease.txt \
         herb_ingredient.txt ingredient_target.txt target_disease.txt; do
  fetch "${HERB_BASE}/${f}" "${DATA}/herb/${f}" || true
done
warn "若 404：到 http://herb.ac.cn/Download/ 页面上逐个复制真实链接替换。"

############################################
# 4. dbPTH —— 整库打包，约 21.4 GB
############################################
log "dbPTH → ${DATA}/dbpth   （约 21.4 GB，请确认磁盘空间与时间）"
if [ "${SKIP_DBPTH:-0}" = "1" ]; then
  warn "SKIP_DBPTH=1，跳过 dbPTH"
else
  avail_gb=$(df -BG --output=avail "$DATA" 2>/dev/null | tail -1 | tr -dc '0-9')
  if [ -n "${avail_gb:-}" ] && [ "$avail_gb" -lt 30 ]; then
    warn "可用空间仅 ${avail_gb}G，低于 30G，跳过 dbPTH。腾出空间后重跑，或设 SKIP_DBPTH=1 显式跳过。"
  else
    fetch "http://dbpth.biocuckoo.cn/download/dbPTH_all.tar.gz" "${DATA}/dbpth/dbPTH_all.tar.gz" || \
      warn "若 404：到 http://dbpth.biocuckoo.cn/ 的 Download 页复制真实链接。"
  fi
fi

############################################
# 需要爬虫的四个
############################################
cat <<'NOTE'

────────────────────────────────────────────────────────────
以下 4 个库没有下载接口，本脚本不覆盖，需要按站点 DOM 写爬虫：

  TCMSP 2.3    old.tcmsp-e.com/tcmspsearch.php   按草药逐页请求，注意限速
  MDIPID       mdipid.idrblab.net                按 DEIM/MMDR/MBDA 三类分别抓
  MicrobeTCM   www.microbetcm.com                按 1032 草药 + 1468 复方逐个抓
  HIT 2.0      hit2.badd-cao.net                 按 1237 个成分逐个抓

MicrobeTCM 与 MDIPID 是人工策展的中等规模库，直接联系通讯作者索取结构化数据
通常比爬取更快也更规范，值得先试。
────────────────────────────────────────────────────────────
NOTE

log "完成。产物在 ${DATA}/"
