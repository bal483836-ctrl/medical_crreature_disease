#!/usr/bin/env bash
# 检查本机网络能否访问这 9 个数据库，先跑这个再跑 download_all.sh
set -u

HOSTS=(
  "www.symmap.org|SymMap"
  "mdipid.idrblab.net|MDIPID"
  "idrblab.org|MDIPID(主站)"
  "disbiome.ugent.be|Disbiome"
  "www.microbetcm.com|MicrobeTCM"
  "dbpth.biocuckoo.cn|dbPTH"
  "www.tcmid.org|TCMID"
  "old.tcmsp-e.com|TCMSP(旧版)"
  "www.tcmsp-e.com|TCMSP"
  "herb.ac.cn|HERB"
  "hit2.badd-cao.net|HIT 2.0"
)

printf '%-28s %-16s %s\n' "HOST" "DATABASE" "RESULT"
printf '%-28s %-16s %s\n' "----" "--------" "------"
for entry in "${HOSTS[@]}"; do
  host="${entry%%|*}"; db="${entry##*|}"
  code=$(curl -sS -o /dev/null -w '%{http_code}' -m 20 -L "https://${host}/" 2>/dev/null)
  if [ "$code" = "000" ] || [ -z "$code" ]; then
    code=$(curl -sS -o /dev/null -w '%{http_code}' -m 20 -L "http://${host}/" 2>/dev/null)
  fi
  case "$code" in
    2*|3*) mark="OK  ($code)" ;;
    000|"") mark="UNREACHABLE (被拦截 / 超时 / DNS 失败)" ;;
    *)      mark="HTTP $code" ;;
  esac
  printf '%-28s %-16s %s\n' "$host" "$db" "$mark"
done
