#!/usr/bin/env python3
"""抓 TCMSP 的关系数据（成分-靶点、靶点-疾病、草药-成分）。

为什么需要它：现有 5 个库里没有「靶点→疾病」的边，导致中药侧子图和微生物侧子图
是断开的。TCMSP 的逐草药详情页里有这些关系，补上之后两个子图能经 Disease 节点接通。

为什么先探再抓：侦察阶段那次请求用的是空 token，返回的是错误页、没有数据数组，
所以**没人见过一个有效响应长什么样**。先用 --probe 存几个响应看清结构，
确认能解析再全量跑，否则等于拿 502 个请求去赌。

token 在运行时从 browse.php 现抓，不硬编码 —— HERB 那份内嵌清单就是因为过时而全部失效的。

用法:
    python3 tcmsp_relations.py --out data --probe 3      # 只探，存 HTML
    python3 tcmsp_relations.py --out data --delay 1.0    # 全量
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetchlib import fetch_text, log  # noqa: E402

BROWSE = "https://www.tcmsp-e.com/browse.php?qc=herbs"
SEARCH = "https://www.tcmsp-e.com/tcmspsearch.php"

# 详情页里会有多个 kendo 表格，靠列名判断哪个是哪个
TABLE_SIGNATURES = {
    "ingredient": {"mol_id", "molecule_name", "ob", "dl"},
    "target": {"target_name", "tar_id", "target_id"},
    "disease": {"disease_name", "dis_id", "disease_id"},
}


def find_token(html: str) -> str | None:
    """从页面里抓站点 token。"""
    for pat in (r'name=["\']token["\'][^>]*value=["\']([a-f0-9]{16,})["\']',
                r'value=["\']([a-f0-9]{32})["\']',
                r'token=([a-f0-9]{32})'):
        m = re.search(pat, html, re.I)
        if m:
            return m.group(1)
    return None


def extract_all_inline_arrays(html: str) -> list[list]:
    """抽出页面里**所有** kendo dataSource 的 data:[...] 数组。

    gh_fetch.extract_inline_json 只取第一个；详情页有多个表格，所以这里要全取。
    同样用字符串感知扫描，避免值里的 ] 或转义引号把数组提前截断。
    """
    out: list[list] = []
    for m in re.finditer(r"data\s*:\s*\[", html):
        start = m.end() - 1
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(html)):
            ch = html[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    try:
                        arr = json.loads(html[start:i + 1])
                        if isinstance(arr, list) and arr:
                            out.append(arr)
                    except json.JSONDecodeError:
                        pass
                    break
    return out


def classify(arr: list) -> str | None:
    """按列名判断这个数组是成分表、靶点表还是疾病表。"""
    if not arr or not isinstance(arr[0], dict):
        return None
    cols = {c.lower() for c in arr[0]}
    best, score = None, 0
    for kind, sig in TABLE_SIGNATURES.items():
        hit = len(cols & sig)
        if hit > score:
            best, score = kind, hit
    return best if score >= 2 else None


def herb_names(data_dir: Path) -> list[str]:
    """从已下载的 tcmsp/herbs.json 取 502 个草药英文名。"""
    p = data_dir / "tcmsp" / "herbs.json"
    if not p.exists():
        log(f"    找不到 {p}，请先跑 gh_fetch.py --datasets tcmsp")
        return []
    rows = json.loads(p.read_text(encoding="utf-8"))
    return [r["herb_en_name"] for r in rows if r.get("herb_en_name")]


def write_tsv(path: Path, rows: list[dict], extra_first: str) -> None:
    if not rows:
        return
    cols: list[str] = [extra_first]
    for r in rows:
        for c in r:
            if c not in cols:
                cols.append(c)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: str(v).replace("\t", " ").replace("\n", " ")
                        for k, v in r.items()})
    log(f"    写出 {path}  ({len(rows)} 行 × {len(cols)} 列)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data")
    ap.add_argument("--delay", type=float, default=1.0, help="请求间隔秒")
    ap.add_argument("--probe", type=int, default=0,
                    help="只抓前 N 个草药并把响应 HTML 存盘，不解析入库")
    ap.add_argument("--limit", type=int, default=0, help="最多抓多少个草药（0=全部）")
    args = ap.parse_args()

    out = Path(args.out)
    log("=" * 60)
    log("TCMSP 关系抓取")
    log("=" * 60)

    log(f"  取 token <- {BROWSE}")
    browse = fetch_text(BROWSE, retries=3)
    if not browse:
        log("  browse.php 不可达，放弃")
        return 1
    token = find_token(browse)
    if not token:
        log("  页面里没找到 token，放弃（不硬编码，避免用到过期值）")
        return 1
    log(f"  token = {token}")

    names = herb_names(out)
    if not names:
        return 1
    log(f"  草药数 {len(names)}")

    if args.probe:
        names = names[:args.probe]
        dump = out / "_recon" / "tcmsp_rel"
        dump.mkdir(parents=True, exist_ok=True)
        log(f"  探测模式：只抓 {len(names)} 个并存 HTML 到 {dump}")
    elif args.limit:
        names = names[:args.limit]

    ing_rows: list[dict] = []
    tgt_rows: list[dict] = []
    dis_rows: list[dict] = []
    stats = {"ok": 0, "empty": 0, "fail": 0}

    for i, name in enumerate(names, 1):
        url = (f"{SEARCH}?qr={urllib.parse.quote(name)}"
               f"&qsr=herb_en_name&token={token}")
        time.sleep(args.delay)
        html = fetch_text(url, retries=2)
        if not html:
            stats["fail"] += 1
            continue

        if args.probe:
            safe = re.sub(r"[^A-Za-z0-9._-]", "_", name)[:60]
            (out / "_recon" / "tcmsp_rel" / f"{safe}.html").write_text(
                html[:600_000], encoding="utf-8")
            arrays = extract_all_inline_arrays(html)
            log(f"  [{i}] {name}: {len(html):,}B, 数组 {len(arrays)} 个"
                + "".join(f"  [{classify(a)}×{len(a)}]" for a in arrays))
            continue

        arrays = extract_all_inline_arrays(html)
        if not arrays:
            stats["empty"] += 1
            continue
        got = False
        for arr in arrays:
            kind = classify(arr)
            bucket = {"ingredient": ing_rows, "target": tgt_rows,
                      "disease": dis_rows}.get(kind)
            if bucket is None:
                continue
            for r in arr:
                r = dict(r)
                r["herb_en_name"] = name
                bucket.append(r)
            got = True
        stats["ok" if got else "empty"] += 1
        if i % 50 == 0:
            log(f"  进度 {i}/{len(names)}  成分{len(ing_rows)} "
                f"靶点{len(tgt_rows)} 疾病{len(dis_rows)}")

    if args.probe:
        log("\n  探测完成。确认结构无误后去掉 --probe 再跑全量。")
        return 0

    log(f"\n  抓取结果: 成功 {stats['ok']}, 无数据 {stats['empty']}, 失败 {stats['fail']}")
    write_tsv(out / "tcmsp" / "rel_herb_ingredient.tsv", ing_rows, "herb_en_name")
    write_tsv(out / "tcmsp" / "rel_target.tsv", tgt_rows, "herb_en_name")
    write_tsv(out / "tcmsp" / "rel_disease.tsv", dis_rows, "herb_en_name")

    (out / "tcmsp" / "rel_stats.json").write_text(
        json.dumps({**stats, "herbs": len(names), "token": token,
                    "ingredient_rows": len(ing_rows),
                    "target_rows": len(tgt_rows),
                    "disease_rows": len(dis_rows)},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
