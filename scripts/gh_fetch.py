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
        "pages": ["http://www.symmap.org/download/",
                  "https://www.symmap.org/download/"],
        "accept": re.compile(r"(SM(HB|IT|TT|DE|TS|MS|SY)|download|static)", re.I),
        "note": "SymMap 草药/成分/靶点/疾病/症状表，XLSX 或 TSV",
    },
    "herb": {
        "pages": ["http://herb.ac.cn/Download/", "http://herb.ac.cn/download/"],
        "accept": None,
        "note": "HERB 2.0 分表下载",
    },
    "disbiome": {
        "api": {
            "experiments": "https://disbiome.ugent.be/api/disbiome/experiments",
            "organisms": "https://disbiome.ugent.be/api/disbiome/organisms",
            "diseases": "https://disbiome.ugent.be/api/disbiome/diseases",
            "publications": "https://disbiome.ugent.be/api/disbiome/publications",
            "methods": "https://disbiome.ugent.be/api/disbiome/methods",
        },
        "pages": ["https://disbiome.ugent.be/export"],
        "accept": None,
        "note": "Disbiome REST API（唯一能一次拉全量的）",
    },
    "dbpth": {
        "pages": ["http://dbpth.biocuckoo.cn/download.php",
                  "http://dbpth.biocuckoo.cn/Download.php",
                  "http://dbpth.biocuckoo.cn/"],
        "accept": None,
        "note": "dbPTH 1.0，整库约 21.4 GB —— 超出 runner 磁盘，默认只发现不下载",
        "huge": True,
    },
    "tcmid": {
        "pages": ["http://www.tcmid.org/download/",
                  "http://www.megabionet.org/tcmid/download/"],
        "accept": None,
        "note": "TCMID 2.0 复方/草药/成分/靶点分表",
    },
    "tcmsp": {
        "pages": ["https://old.tcmsp-e.com/tcmsp.php",
                  "https://www.tcmsp-e.com/"],
        "accept": None,
        "note": "TCMSP 无下载接口，这里只做链接发现，实际取数需爬虫",
    },
    "hit2": {
        "pages": ["http://hit2.badd-cao.net/", "http://hit2.badd-cao.net/download/"],
        "accept": None,
        "note": "HIT 2.0 无批量下载，只做链接发现",
    },
    "mdipid": {
        "pages": ["https://mdipid.idrblab.net/download",
                  "https://mdipid.idrblab.net/",
                  "https://idrblab.org/mdipid/"],
        "accept": None,
        "note": "MDIPID 无公开打包下载，只做链接发现",
    },
    "microbetcm": {
        "pages": ["https://www.microbetcm.com/download",
                  "https://www.microbetcm.com/"],
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


def log(msg: str) -> None:
    print(msg, flush=True)


def open_url(url: str, timeout: int = 90):
    ctx = ssl.create_default_context()
    # 部分国内学术站点证书链不完整 / 过期，发现阶段不因此中断
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "*/*",
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


def discover(name: str, cfg: dict) -> list[str]:
    """抓取页面并解析出候选数据文件链接。"""
    found: list[str] = []
    seen: set[str] = set()
    for page in cfg.get("pages", []):
        log(f"    扫描 {page}")
        html = fetch_text(page)
        if html is None:
            continue
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
    return found


def download(url: str, dest: Path, max_bytes: int | None) -> dict:
    """下载单个文件，返回结果记录。"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    record: dict = {"url": url, "path": str(dest), "ok": False}
    delay = 2
    for attempt in range(4):
        try:
            with open_url(url, timeout=300) as resp:
                declared = resp.headers.get("Content-Length")
                if declared and max_bytes and int(declared) > max_bytes:
                    record["skipped"] = (
                        f"超过大小上限 ({int(declared) / 1e6:.0f} MB > "
                        f"{max_bytes / 1e6:.0f} MB)")
                    log(f"      跳过（过大 {int(declared) / 1e6:.0f} MB）: {url}")
                    return record
                sha = hashlib.sha256()
                total = 0
                with dest.open("wb") as fh:
                    while True:
                        chunk = resp.read(1 << 20)
                        if not chunk:
                            break
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
            record.update(ok=True, bytes=total, sha256=sha.hexdigest())
            log(f"      OK  {dest.name}  ({total / 1e6:.2f} MB)")
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
    results = []
    for key, url in endpoints.items():
        log(f"    API {key}  <- {url}")
        dest = out_dir / f"{key}.json"
        rec = download(url, dest, None)
        if rec.get("ok"):
            try:
                data = json.loads(dest.read_text(encoding="utf-8"))
                rec["records"] = len(data) if isinstance(data, list) else 1
                log(f"        {rec['records']} 条记录")
            except json.JSONDecodeError as exc:
                rec["warning"] = f"返回的不是合法 JSON: {exc}"
                log(f"        警告：返回的不是合法 JSON")
        results.append(rec)
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

    report: dict = {"datasets": {}, "max_mb": args.max_mb,
                    "discover_only": args.discover_only}

    for name in names:
        cfg = SOURCES[name]
        log(f"\n{'=' * 64}\n[{name}]  {cfg['note']}\n{'=' * 64}")
        entry: dict = {"note": cfg["note"], "discovered": [], "files": []}
        out_dir = out_root / name

        if cfg.get("api") and not args.discover_only:
            entry["files"] += fetch_api(name, cfg["api"], out_dir)

        links = discover(name, cfg)
        entry["discovered"] = links
        log(f"    共发现 {len(links)} 个候选链接")

        if args.discover_only:
            report["datasets"][name] = entry
            continue
        if cfg.get("huge") and not args.include_huge:
            entry["skipped"] = "标记为超大数据源，需 --include-huge 才下载"
            log("    跳过下载（超大数据源，需 --include-huge）")
            report["datasets"][name] = entry
            continue

        for url in links:
            fname = Path(urllib.parse.urlparse(url).path).name or "index"
            entry["files"].append(download(url, out_dir / fname, max_bytes))

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
    log(f"\n  合计 {total_ok} 个文件，{total_bytes / 1e6:.2f} MB")
    log(f"  报告: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
