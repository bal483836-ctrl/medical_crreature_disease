#!/usr/bin/env python3
"""
在 GitHub Actions runner 上下载 9 个中药/微生物数据库。

设计要点：**不硬编码下载链接**。各库的静态文件名随版本变动，硬编码必然 404。
脚本改为抓取各库的下载页面，解析出页面里的所有链接，按扩展名/正则筛出数据文件再下载。
这样即使文件名变了也能拿到，并且会把「发现了哪些链接」写进报告，便于下次校正。

用法:
    python3 gh_fetch.py --out data --datasets all
    python3 gh_fetch.py --out data --datasets symmap,disbiome --max-mb 90
    python3 gh_fetch.py --out data --datasets all --discover-only   # 只探链接不下载

仅依赖标准库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import socket
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetchlib import (  # noqa: E402
    DATA_EXT,
    UA,
    LinkParser,
    download,
    fetch_text,
    log,
    looks_like_html,
    open_url,
)

SOURCES: dict[str, dict] = {
    "symmap": {
        # run #1/#2 实测：https 拒绝连接，http 可用，稳定拿到 v1.0/v2.0 全套 26 个 xlsx
        "pages": ["http://www.symmap.org/download/"],
        "accept": re.compile(r"(SM(HB|IT|TT|DE|TS|MS|SY)|download|static)", re.I),
        "note": "SymMap 全套实体表 XLSX（已稳定下载）",
    },
    "herb": {
        # run #2 实测：herb.ac.cn 是 umi.js 单页应用，HTML 里没有任何数据链接，
        # 下载走接口。这里直接试常见的静态文件名 —— 猜错会被 HTML 校验挡下，不会假成功。
        "pages": ["http://herb.ac.cn/Download/"],
        "direct": [f"http://herb.ac.cn/download/{f}" for f in (
            "HERB_herb_info.txt", "HERB_ingredient_info.txt",
            "HERB_target_info.txt", "HERB_disease_info.txt",
            "HERB_experiment_info.txt", "HERB_reference_info.txt",
            "herb_info.txt", "ingredient_info.txt", "target_info.txt",
            "disease_info.txt",
        )],
        "accept": None,
        "note": "HERB 2.0（站点为 SPA，靠直连候选文件名探测）",
    },
    "disbiome": {
        # run #2 实测：官方 disbiome.ugent.be/api/* 全部返回 Angular 首页（假 200），
        # 唯一真正可用的是 BioThings 镜像。用 scroll 分页拉全量。
        "biothings": "https://pending.biothings.io/disbiome",
        "pages": [],
        "accept": None,
        "note": "Disbiome（经 BioThings 镜像全量拉取）",
    },
    "dbpth": {
        # run #2 教训：把 Download.php 换成 Download/ 导致发现数从 1325 掉到 0（后者 403）。
        # Download.php 才是真正列出分片的页面，恢复并置于首位。
        "pages": ["http://dbpth.biocuckoo.cn/Download.php",
                  "http://dbpth.biocuckoo.cn/"],
        "accept": None,
        "prefer": re.compile(r"(/ProtGrp/|PTH\.sql\.zip$)", re.I),
        "note": "dbPTH 1.0，取 ProtGrp 分片（整库 PTH.zip 约 21.4GB，需 --include-huge）",
    },
    "tcmid": {
        # ⚠️ run #2 实测：tcmid.org 域名已易主，现为无关的慈善机构网站，绝不可从该域取数。
        # 历史地址 megabionet.org/tcmid/ 超时。TCMID 很可能已停止服务。
        "pages": ["http://www.megabionet.org/tcmid/"],
        "accept": None,
        "note": "TCMID 2.0（原域名已易主，仅试历史地址，疑似已下线）",
    },
    "tcmsp": {
        # run #2：站点可达但页面是检索界面，无任何下载链接 —— 与文档结论一致
        "pages": ["https://www.tcmsp-e.com/", "https://www.tcmsp-e.com/tcmspsearch.php"],
        "accept": None,
        "note": "TCMSP（确认无下载链接，取数需爬虫）",
    },
    "hit2": {
        # run #2 实测：hit2.badd-cao.net 只是个 frameset，真正的站在 2345 端口
        "pages": ["http://www.badd-cao.net:2345/",
                  "http://www.badd-cao.net:2345/download.php",
                  "http://www.badd-cao.net:2345/download/"],
        "accept": None,
        "note": "HIT 2.0（真实站点在 badd-cao.net:2345，非标准端口）",
    },
    "mdipid": {
        # run #2：idrblab.org/mdipid/ 是 meta 跳转页，目标 mdipid.idrblab.net 持续 500
        "pages": ["https://mdipid.idrblab.net/", "https://idrblab.org/mdipid/"],
        "accept": None,
        "note": "MDIPID（站点持续返回 500，服务疑似故障）",
    },
    "microbetcm": {
        # run #2：确认为单页应用，HTML 内无数据链接
        "pages": ["https://www.microbetcm.com/"],
        "accept": None,
        "note": "MicrobeTCM（SPA，无静态下载链接）",
    },
}


# ------------------------------------------------------------------- 工具函数
def discover(name: str, cfg: dict, dump_dir: Path | None = None) -> list[str]:
    """抓取页面并解析出候选数据文件链接。

    dump_dir 不为 None 时会把每个发现页的 HTML 存下来 —— 当某个库发现 0 个链接，
    唯一能判断「站点没给链接」还是「解析逻辑不对」的办法就是看原始页面。
    """
    found: list[str] = []
    seen: set[str] = set()
    for page in cfg.get("pages", []):
        log(f"    扫描 {page}")
        html = fetch_text(page)
        if html is None:
            continue
        if dump_dir is not None:
            safe = re.sub(r"[^A-Za-z0-9._-]", "_", page)[-120:]
            dump_dir.mkdir(parents=True, exist_ok=True)
            (dump_dir / f"{name}__{safe}.html").write_text(html[:400_000],
                                                           encoding="utf-8")
        parser = LinkParser()
        try:
            parser.feed(html)
        except Exception as exc:  # noqa: BLE001
            log(f"      HTML 解析异常（忽略）: {exc}")
        # 补一遍裸 URL（有些站点把链接写在 JS 字符串里）
        raw_urls = re.findall(r"""['"(]\s*((?:https?:)?//?[^\s'"()<>]+?\.(?:xlsx?|tsv|csv|txt|zip|gz|tgz|tar|json|sql))\s*['")]""", html, re.I)
        for href in parser.links + raw_urls:
            href = href.strip()
            if not href or href.startswith(("#", "javascript:", "mailto:", "data:")):
                continue
            absolute = urllib.parse.urljoin(page, href)
            if absolute in seen:
                continue
            seen.add(absolute)
            if not DATA_EXT.search(urllib.parse.urlparse(absolute).path):
                continue
            accept = cfg.get("accept")
            if accept is not None and not accept.search(absolute):
                continue
            found.append(absolute)
        log(f"      命中 {len(found)} 个候选数据文件链接（累计）")

    prefer = cfg.get("prefer")
    if prefer is not None and found:
        narrowed = [u for u in found if prefer.search(u)]
        if narrowed:
            log(f"      按 prefer 规则收窄: {len(found)} -> {len(narrowed)}")
            return narrowed
        log("      prefer 规则未命中任何链接，保留全部")
    return found


def fetch_biothings(base: str, out_dir: Path) -> list[dict]:
    """用 BioThings 的 scroll 分页把整个索引拉下来。

    单次 query 最多 1000 条，必须用 fetch_all=true 拿 _scroll_id 再翻页，
    否则只会拿到第一页还误以为是全量。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    records: list = []
    url = f"{base}/query?q=__all__&fetch_all=true"
    page = 0
    while url and page < 500:
        try:
            with open_url(url, timeout=180, accept="application/json") as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            log(f"      分页在第 {page} 页中断: {type(exc).__name__}: {exc}")
            break
        hits = payload.get("hits", [])
        if not hits:
            break
        records.extend(hits)
        page += 1
        log(f"      第 {page} 页 +{len(hits)} 条（累计 {len(records)}）")
        scroll_id = payload.get("_scroll_id")
        url = f"{base}/query?scroll_id={urllib.parse.quote(scroll_id)}" if scroll_id else None

    if not records:
        return [{"url": base, "ok": False,
                 "error": "BioThings 未返回任何记录"}]
    dest = out_dir / "experiments.json"
    dest.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    size = dest.stat().st_size
    log(f"      OK  {dest.name}  ({size / 1e6:.2f} MB, {len(records)} 条)")
    return [{"url": base, "path": str(dest), "ok": True,
             "bytes": size, "records": len(records),
             "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}]


def fetch_direct(urls: list[str], out_dir: Path, max_bytes: int | None) -> list[dict]:
    """试一批候选直链。猜错的会被 HTML 校验挡下，不会产生假成功。"""
    results = []
    for url in urls:
        fname = Path(urllib.parse.urlparse(url).path).name
        log(f"    直链候选 {fname}")
        results.append(download(url, out_dir / fname, max_bytes))
    return results


def fetch_api(name: str, endpoints: dict, out_dir: Path) -> list[dict]:
    """拉 JSON API。每个端点给多个候选 base，命中一个就停。"""
    results = []
    for key, urls in endpoints.items():
        candidates = [urls] if isinstance(urls, str) else list(urls)
        dest = out_dir / f"{key}.json"
        for i, url in enumerate(candidates):
            log(f"    API {key}  <- {url}")
            rec = download(url, dest, None, expect="json")
            if rec.get("ok"):
                results.append(rec)
                break
            if i < len(candidates) - 1:
                log("      换下一个候选地址")
        else:
            results.append(rec)  # 全部候选失败，记最后一次
    return results


# ------------------------------------------------------------------------ 主流程
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data", help="输出根目录")
    ap.add_argument("--datasets", default="all",
                    help="逗号分隔，或 all。可选: " + ", ".join(SOURCES))
    ap.add_argument("--max-mb", type=float, default=90.0,
                    help="单文件大小上限 MB，超过则跳过（0 = 不限）")
    ap.add_argument("--max-total-mb", type=float, default=8000.0,
                    help="全部下载量上限 MB，达到后停止（runner 磁盘有限，0 = 不限）")
    ap.add_argument("--discover-only", action="store_true", help="只发现链接，不下载")
    ap.add_argument("--include-huge", action="store_true",
                    help="包含标记为 huge 的数据源（dbPTH ~21.4GB）")
    args = ap.parse_args()

    socket.setdefaulttimeout(300)

    names = (list(SOURCES) if args.datasets.strip().lower() == "all"
             else [n.strip().lower() for n in args.datasets.split(",") if n.strip()])
    unknown = [n for n in names if n not in SOURCES]
    if unknown:
        print(f"未知数据源: {', '.join(unknown)}\n可选: {', '.join(SOURCES)}",
              file=sys.stderr)
        return 2

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    max_bytes = int(args.max_mb * 1e6) if args.max_mb > 0 else None
    budget = int(args.max_total_mb * 1e6) if args.max_total_mb > 0 else None
    spent = 0

    report: dict = {"datasets": {}, "max_mb": args.max_mb,
                    "max_total_mb": args.max_total_mb,
                    "discover_only": args.discover_only}

    for name in names:
        cfg = SOURCES[name]
        log(f"\n{'=' * 64}\n[{name}]  {cfg['note']}\n{'=' * 64}")
        entry: dict = {"note": cfg["note"], "discovered": [], "files": []}
        out_dir = out_root / name

        if not args.discover_only:
            if cfg.get("api"):
                entry["files"] += fetch_api(name, cfg["api"], out_dir)
            if cfg.get("biothings"):
                entry["files"] += fetch_biothings(cfg["biothings"], out_dir)
            if cfg.get("direct"):
                entry["files"] += fetch_direct(cfg["direct"], out_dir, max_bytes)

        links = discover(name, cfg, dump_dir=out_root / "_pages")
        entry["discovered"] = links
        log(f"    共发现 {len(links)} 个候选链接")

        if args.discover_only:
            report["datasets"][name] = entry
            continue
        if cfg.get("huge") and not args.include_huge:  # 保留给未来的超大源
            entry["skipped"] = "标记为超大数据源，需 --include-huge 才下载"
            log("    跳过下载（超大数据源，需 --include-huge）")
            report["datasets"][name] = entry
            continue

        for url in links:
            if budget is not None and spent >= budget:
                entry.setdefault("truncated",
                                 f"已达总量上限 {args.max_total_mb:.0f} MB，其余链接未下载")
                log(f"    达到总量上限 {args.max_total_mb:.0f} MB，停止下载")
                break
            fname = Path(urllib.parse.urlparse(url).path).name or "index"
            rec = download(url, out_dir / fname, max_bytes)
            spent += rec.get("bytes", 0)
            entry["files"].append(rec)

        report["datasets"][name] = entry

    # ------------------------------------------------------------- 汇总
    report_path = out_root / "fetch_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                           encoding="utf-8")

    log(f"\n{'=' * 64}\n汇总\n{'=' * 64}")
    total_ok = total_bytes = 0
    for name, entry in report["datasets"].items():
        oks = [f for f in entry["files"] if f.get("ok")]
        size = sum(f.get("bytes", 0) for f in oks)
        total_ok += len(oks)
        total_bytes += size
        status = "—" if not entry["files"] else f"{len(oks)}/{len(entry['files'])} 成功"
        log(f"  {name:12} 发现 {len(entry['discovered']):3} 链接   "
            f"{status:16} {size / 1e6:9.2f} MB")
    log(f"\n  合计 {total_ok} 个文件，{total_bytes / 1e6:.2f} MB"
        f"（总量上限 {args.max_total_mb:.0f} MB）")
    log(f"  报告: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
