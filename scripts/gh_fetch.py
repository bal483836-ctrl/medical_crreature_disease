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
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")

# 数据文件的扩展名白名单
DATA_EXT = re.compile(
    r"\.(xlsx?|tsv|csv|txt|zip|gz|tgz|bz2|xz|tar|json|sql|rar|7z|sdf|mol2?)$",
    re.I,
)

# ---------------------------------------------------------------- 数据源定义
#   pages     : 要抓取并解析链接的页面
#   accept    : 额外的链接筛选正则（None = 只按扩展名筛）
#   direct    : 已知可直接下载的 URL（不经发现）
#   api       : 直接拉 JSON 的 API 端点
#   note      : 说明
SOURCES: dict[str, dict] = {
    "symmap": {
        # run #1 实测：https 连接被拒，http 可用且拿到 v1.0/v2.0 全套 26 个 xlsx
        "pages": ["http://www.symmap.org/download/"],
        "accept": re.compile(r"(SM(HB|IT|TT|DE|TS|MS|SY)|download|static)", re.I),
        "note": "SymMap 草药/成分/靶点/疾病/症状/证候表，XLSX（run #1 已验证可下）",
    },
    "herb": {
        # run #1：页面抓到了但 0 个数据链接，补候选路径并 dump 页面排查
        "pages": ["http://herb.ac.cn/Download/", "http://herb.ac.cn/download/",
                  "http://herb.ac.cn/", "http://herb.ac.cn/Downloads/"],
        "accept": None,
        "note": "HERB 2.0 分表下载",
    },
    "disbiome": {
        # run #1：/api/disbiome/* 返回 Angular 首页 HTML，说明路径不对。
        # 这里给多个候选，并在 download() 里强制校验必须是合法 JSON。
        "api": {
            "experiments": [
                "https://disbiome.ugent.be/api/disbiome/experiments",
                "https://disbiome.ugent.be/api/experiments",
                "https://disbiome.ugent.be/experiments/api",
                "https://pending.biothings.io/disbiome/query?q=__all__&size=1000",
            ],
            "organisms": [
                "https://disbiome.ugent.be/api/disbiome/organisms",
                "https://disbiome.ugent.be/api/organisms",
            ],
            "diseases": [
                "https://disbiome.ugent.be/api/disbiome/diseases",
                "https://disbiome.ugent.be/api/diseases",
            ],
            "publications": [
                "https://disbiome.ugent.be/api/disbiome/publications",
                "https://disbiome.ugent.be/api/publications",
            ],
            "methods": [
                "https://disbiome.ugent.be/api/disbiome/methods",
                "https://disbiome.ugent.be/api/methods",
            ],
        },
        "pages": ["https://disbiome.ugent.be/export", "https://disbiome.ugent.be/api"],
        "accept": None,
        "note": "Disbiome REST API（run #1 路径不对，本轮试多个候选并校验 JSON）",
    },
    "dbpth": {
        # run #1 重大发现：整库按蛋白分组/成分分类切成了 1325 个 zip 分片，
        # 不必下 21.4GB 整包。默认取 ProtGrp/ 这一套（11 个分组即完整划分）+ SQL dump。
        "pages": ["http://dbpth.biocuckoo.cn/Download/", "http://dbpth.biocuckoo.cn/"],
        "accept": None,
        "prefer": re.compile(r"(/ProtGrp/|PTH\.sql\.zip$)", re.I),
        "note": "dbPTH 1.0，按 ProtGrp 分片下载（整库 PTH.zip 约 21.4GB 需 --include-huge）",
    },
    "tcmid": {
        # run #1：/download/ 404。改从根路径发现
        "pages": ["http://www.tcmid.org/", "http://tcmid.org/",
                  "http://www.megabionet.org/tcmid/"],
        "accept": None,
        "note": "TCMID 2.0 复方/草药/成分/靶点分表",
    },
    "tcmsp": {
        # run #1：old.tcmsp-e.com 连接被拒（https）；www 抓到但 0 链接
        "pages": ["https://www.tcmsp-e.com/", "http://old.tcmsp-e.com/tcmsp.php",
                  "https://www.tcmsp-e.com/tcmspsearch.php"],
        "accept": None,
        "note": "TCMSP 无下载接口，只做链接发现，实际取数需爬虫",
    },
    "hit2": {
        "pages": ["http://hit2.badd-cao.net/", "http://hit2.badd-cao.net/download/",
                  "http://hit2.badd-cao.net/download.php"],
        "accept": None,
        "note": "HIT 2.0 无批量下载，只做链接发现",
    },
    "mdipid": {
        # run #1：mdipid.idrblab.net 全站 500。主站路径另试
        "pages": ["https://idrblab.org/mdipid/", "https://mdipid.idrblab.net/",
                  "https://mdipid.idrblab.net/download"],
        "accept": None,
        "note": "MDIPID 无公开打包下载（run #1 站点 500），只做链接发现",
    },
    "microbetcm": {
        # run #1：/download 404，根路径 0 链接
        "pages": ["https://www.microbetcm.com/", "https://www.microbetcm.com/#/download",
                  "https://www.microbetcm.com/api/download"],
        "accept": None,
        "note": "MicrobeTCM 无下载接口，只做链接发现",
    },
}


# ------------------------------------------------------------------- 工具函数
class LinkParser(HTMLParser):
    """收集 <a href>、<link href>、<iframe/script/form src|action>。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = dict(attrs)
        for key in ("href", "src", "action", "data-href", "data-url"):
            val = d.get(key)
            if val:
                self.links.append(val)


HTML_SNIFF = re.compile(rb"^\s*(<!DOCTYPE|<html|<\?xml[^>]*>\s*<html)", re.I)


def log(msg: str) -> None:
    print(msg, flush=True)


def looks_like_html(head: bytes) -> bool:
    """下载到的内容是不是 HTML 页面（而不是数据文件）。

    站点把未知路由交给前端框架时会对任何 URL 都回 200 + SPA 首页，
    只看状态码会把这种情况误判为下载成功 —— 必须嗅探内容。
    """
    return bool(HTML_SNIFF.match(head))


def open_url(url: str, timeout: int = 90, accept: str = "*/*"):
    ctx = ssl.create_default_context()
    # 部分国内学术站点证书链不完整 / 过期，发现阶段不因此中断
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": accept,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    })
    return urllib.request.urlopen(req, timeout=timeout, context=ctx)


def fetch_text(url: str, retries: int = 2) -> str | None:
    delay = 2
    for attempt in range(retries + 1):
        try:
            with open_url(url) as resp:
                raw = resp.read()
            for enc in ("utf-8", "gb18030", "latin-1"):
                try:
                    return raw.decode(enc)
                except UnicodeDecodeError:
                    continue
            return raw.decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001 - 发现阶段要尽量往下走
            if attempt == retries:
                log(f"      页面不可达: {url}  ({type(exc).__name__}: {exc})")
                return None
            time.sleep(delay)
            delay *= 2
    return None


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


def download(url: str, dest: Path, max_bytes: int | None,
             expect: str | None = None) -> dict:
    """下载单个文件，返回结果记录。

    expect="json" 时会校验返回体确实是 JSON；任何情况下都会拒绝把
    HTML 页面当作数据文件存下来（SPA 站点对任意路径都回 200 + 首页）。
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    record: dict = {"url": url, "path": str(dest), "ok": False}
    accept = "application/json" if expect == "json" else "*/*"
    delay = 2
    for attempt in range(4):
        try:
            with open_url(url, timeout=300, accept=accept) as resp:
                declared = resp.headers.get("Content-Length")
                if declared and max_bytes and int(declared) > max_bytes:
                    record["skipped"] = (
                        f"超过大小上限 ({int(declared) / 1e6:.0f} MB > "
                        f"{max_bytes / 1e6:.0f} MB)")
                    log(f"      跳过（过大 {int(declared) / 1e6:.0f} MB）: {url}")
                    return record
                sha = hashlib.sha256()
                total = 0
                head = b""
                with dest.open("wb") as fh:
                    while True:
                        chunk = resp.read(1 << 20)
                        if not chunk:
                            break
                        if len(head) < 512:
                            head += chunk[:512]
                        total += len(chunk)
                        if max_bytes and total > max_bytes:
                            fh.close()
                            dest.unlink(missing_ok=True)
                            record["skipped"] = (
                                f"下载中超过大小上限 {max_bytes / 1e6:.0f} MB")
                            log(f"      跳过（传输中超限）: {url}")
                            return record
                        sha.update(chunk)
                        fh.write(chunk)
            # ---- 内容校验：状态码 200 不等于拿到了数据 ----
            if looks_like_html(head) and not dest.suffix.lower() in (".html", ".htm"):
                dest.unlink(missing_ok=True)
                record["error"] = (
                    "ContentMismatch: 返回的是 HTML 页面而非数据文件"
                    "（该路径可能不存在，被前端路由兜底为首页）")
                log(f"      失败（返回 HTML 而非数据）: {url}")
                return record
            if expect == "json":
                try:
                    parsed = json.loads(dest.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                    dest.unlink(missing_ok=True)
                    record["error"] = f"ContentMismatch: 不是合法 JSON ({exc})"
                    log(f"      失败（不是合法 JSON）: {url}")
                    return record
                record["records"] = len(parsed) if isinstance(parsed, list) else 1
            record.update(ok=True, bytes=total, sha256=sha.hexdigest())
            extra = f", {record['records']} 条" if "records" in record else ""
            log(f"      OK  {dest.name}  ({total / 1e6:.2f} MB{extra})")
            return record
        except Exception as exc:  # noqa: BLE001
            record["error"] = f"{type(exc).__name__}: {exc}"
            if attempt < 3:
                time.sleep(delay)
                delay *= 2
    dest.unlink(missing_ok=True)
    log(f"      失败: {url}  ({record.get('error')})")
    return record


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

        if cfg.get("api") and not args.discover_only:
            entry["files"] += fetch_api(name, cfg["api"], out_dir)

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
