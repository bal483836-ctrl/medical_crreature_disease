#!/usr/bin/env python3
"""侦察剩余 6 个库的取数路径，并顺手把能拿的数据拿下来。

背景：开发会话的出口网络拦截了这 6 个站，无法交互式探查，只能让 runner 带证据回来。
run #3 已定位失败原因，分两类，对应两套办法：

  A. 站活着、数据藏在 JS 里（HERB / MicrobeTCM / TCMSP）
     → 下载前端 bundle，从中挖出接口路由，逐个探测，返回实质 JSON 的当场存盘。

  B. 站已死（TCMID 域名易主 / HIT 2.0 端口拒连 / MDIPID 持续 500）
     → 只用 Wayback Machine 存档，且必须记录快照时间与原始 URL。

所有原始证据（bundle 原文、探测响应样本、CDX 清单）都落盘，因为下一步写什么
完全取决于这一轮带回什么。

用法:
    python3 gh_recon.py --out data --targets all
    python3 gh_recon.py --out data --targets herb,microbetcm --delay 1.0
"""
from __future__ import annotations

import argparse
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
    LinkParser,
    download,
    fetch_text,
    log,
    looks_like_html,
    open_url,
)

# ---------------------------------------------------------------- A 类：活站
LIVE_SITES: dict[str, dict] = {
    "herb": {
        "origin": "http://herb.ac.cn",
        "entries": ["http://herb.ac.cn/", "http://herb.ac.cn/Download/"],
        # bundle 里的 file_path 是服务端绝对路径，但服务端回 "Sorry, unavailable path."，
        # 说明清单已过时或路径要换一种写法。这里定向试各种变体，
        # 由响应内容判断哪一种被接受（裸调回 "Sorry, no path."，可作阴性对照）。
        "extra_probes": [
            "http://herb.ac.cn/download/file/?file_path=" + v
            for v in (
                "/data/Web_server/HERB_web/static/download_data/HERB_herb_info.txt",
                "data/Web_server/HERB_web/static/download_data/HERB_herb_info.txt",
                "/static/download_data/HERB_herb_info.txt",
                "static/download_data/HERB_herb_info.txt",
                "/download_data/HERB_herb_info.txt",
                "download_data/HERB_herb_info.txt",
                "HERB_herb_info.txt",
                "/data/Web_server/HERB_web/static/download_data/HERB_herb_info.txt.gz",
                "/data/Web_server/HERB_web/static/download_data/HERB_herb_info.zip",
                "/home/Web_server/HERB_web/static/download_data/HERB_herb_info.txt",
            )
        ],
        "note": "umi.js SPA；下载走 GET /download/file/?file_path=，本轮试路径变体",
    },
    "microbetcm": {
        "origin": "https://www.microbetcm.com",
        # 第一轮教训：/api/index/* 全 404，且从 bundle 看那组接口是文件上传用的，
        # 不是取数接口。本轮补 /microbetcm 前缀，并扫更多入口页找真正的数据页。
        "entries": [
            "https://www.microbetcm.com/",
            "https://www.microbetcm.com/microbetcm/",
            "https://www.microbetcm.com/microbetcm/index.html",
            "https://www.microbetcm.com/microbetcm/nazox/",
        ],
        "prefixes": ["", "/microbetcm"],
        "note": "Vue SPA，第一轮 0 命中，本轮试 /microbetcm 前缀与更多入口",
    },
    "tcmsp": {
        "origin": "https://www.tcmsp-e.com",
        # 第一轮教训：7 个 bundle 全是 jQuery/bootstrap/kendo 等通用库，挖不出接口。
        # TCMSP 用 Kendo UI Grid，数据源配置写在 PHP 页面的内联 <script> 里，
        # 所以本轮改为扫页面内联脚本。
        "entries": [
            "https://www.tcmsp-e.com/",
            "https://www.tcmsp-e.com/tcmspsearch.php",
            "https://www.tcmsp-e.com/tcmspsearch.php?qr=Ma%20Huang&qsr=herb_en_name&token=",
            "https://www.tcmsp-e.com/browse.php?qc=herbs",
            "https://www.tcmsp-e.com/tcmsp.php",
        ],
        "note": "Kendo UI Grid，接口配置在页面内联脚本里",
    },
    "hit2": {
        "origin": "http://hit2.badd-cao.net",
        # 第一轮：badd-cao.net:2345 Connection refused；Wayback 只存到一个 SEPPA3
        # 的批量提交工具和 9 行示例文件，都不是 HIT 的数据。本轮试其它主机/端口。
        # www.badd-cao.net 是 Cao-Lab 课题组主页（可达），HIT 的现址应挂在 Resources 页上。
        "entries": [
            "http://www.badd-cao.net/resources.html",
            "http://www.badd-cao.net/",
            "http://hit2.badd-cao.net/",
        ],
        "note": "根域是 Cao-Lab 主页，从 Resources 页找 HIT 现址",
    },
}

# ---------------------------------------------------------------- B 类：死站
DEAD_SITES: dict[str, list[str]] = {
    "tcmid": ["tcmid.org", "www.tcmid.org", "megabionet.org/tcmid"],
    # HERB：下载接口本身是好的，但它指向的文件在服务端已不存在
    # （/download/file/?file_path=static/... 回 "file_path dose not exists"），
    # 即官方下载功能已损坏，转存档兜底。
    "herb": ["herb.ac.cn", "www.herb.ac.cn"],
    # MicrobeTCM：SPA 且 /api/index/* 是上传接口，无取数路径，转存档兜底。
    "microbetcm": ["microbetcm.com", "www.microbetcm.com"],
    # HIT 2.0：课题组 Resources 页确认官方地址就是 hit2.badd-cao.net，
    # 而它只是个指向 2345 端口的 frameset，该端口拒连 —— 服务已停。存档兜底。
    # HIT 2.0：存档里只有一个 9 行的演示文件（SMILES.txt）和 SEPPA3 的批量提交
    # 工具包，都不是 HIT 的数据，一并列入跳过。
    "hit2": ["hit2.badd-cao.net", "hit.badd-cao.net", "badd-cao.net"],
    # hit2 不在此列：第一轮已查过 Wayback，只存到一个 SEPPA3 的批量提交工具
    # 和 9 行示例文件，都不是 HIT 的数据。改到 LIVE_SITES 里探其它主机。
    "mdipid": ["mdipid.idrblab.net", "idrblab.org/mdipid"],
}

# 存档里常混入的「不是数据」的文件：站点杂项、工具包、可执行文件。
# 不过滤的话，每跑一次 recon 就会把它们重新下载并提交，
# 看文件数会误以为该库已取得。
NOT_DATA = re.compile(
    r"(robots\.txt|sitemap|favicon|crossdomain|flash_text|"
    r"\.exe$|geckodriver|Submit[%_ ]*local[%_ ]*files|batch\.tar)",
    re.I,
)

SKIP_PER_SITE = {
    "hit2": re.compile(r"SMILES\.txt$", re.I),
}

# 从 JS 里挖接口路由的正则
ENDPOINT_PATTERNS = [
    re.compile(r"""["'](/[\w\-./]{3,}?(?:api|list|search|query|download|data|all|info|detail)[\w\-./]*)["']""", re.I),
    re.compile(r"""["'](https?://[^"'\s]+?/(?:api|data|download)[^"'\s]*)["']""", re.I),
    re.compile(r"""baseURL\s*[:=]\s*["']([^"']+)["']""", re.I),
    re.compile(r"""(?:url|path)\s*:\s*["'](/[\w\-./]{4,})["']"""),
    # 相对路径的服务端脚本（TCMSP 的 browse.php?qc=herbs 就是这样，
    # 第一轮因为只认以 / 或 http 开头的路径而整个漏掉）
    re.compile(r"""["']((?:\.{0,2}/)?[\w\-./]{2,}\.(?:php|jsp|aspx|cgi)(?:\?[^"'\s]*)?)["']"""),
]

# 明显不是接口的静态资源，别浪费探测预算
NOISE = re.compile(r"\.(js|css|png|jpe?g|gif|svg|ico|woff2?|ttf|eot|map|mp4)(\?|$)", re.I)


def mine_endpoints(js: str) -> list[str]:
    """从 bundle 文本里抽候选接口路径。"""
    found: set[str] = set()
    for pat in ENDPOINT_PATTERNS:
        for m in pat.finditer(js):
            cand = m.group(1).strip()
            if len(cand) < 4 or NOISE.search(cand):
                continue
            found.add(cand)
    return sorted(found)


def probe(url: str, out_dir: Path, delay: float) -> dict:
    """GET 一个候选接口，记录它到底返回了什么。"""
    rec: dict = {"url": url, "ok": False}
    time.sleep(delay)
    try:
        with open_url(url, timeout=45, accept="application/json, text/plain, */*") as resp:
            body = resp.read(512_000)
            rec["status"] = resp.status
            rec["content_type"] = resp.headers.get("Content-Type", "")
            rec["bytes"] = len(body)
    except Exception as exc:  # noqa: BLE001
        rec["error"] = f"{type(exc).__name__}: {exc}"
        return rec

    rec["is_html"] = looks_like_html(body[:512])
    rec["head"] = body[:300].decode("utf-8", "replace")
    if rec["is_html"]:
        rec["verdict"] = "HTML 兜底页，不是接口"
        return rec
    try:
        parsed = json.loads(body.decode("utf-8"))
        rec["is_json"] = True
        if isinstance(parsed, list):
            rec["json_len"] = len(parsed)
        elif isinstance(parsed, dict):
            rec["json_keys"] = sorted(parsed.keys())[:25]
            for k in ("data", "results", "hits", "rows", "list", "records"):
                v = parsed.get(k)
                if isinstance(v, list):
                    rec["payload_key"] = k
                    rec["payload_len"] = len(v)
                    break
        rec["ok"] = True
        rec["verdict"] = "返回合法 JSON ✅"
        # 存样本，供我分析结构
        out_dir.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", url)[-120:]
        (out_dir / f"{safe}.json").write_bytes(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        rec["is_json"] = False
        rec["verdict"] = "非 JSON 非 HTML（可能是 TSV/二进制）"
        rec["ok"] = rec["bytes"] > 200
        if rec["ok"]:
            out_dir.mkdir(parents=True, exist_ok=True)
            safe = re.sub(r"[^A-Za-z0-9._-]", "_", url)[-120:]
            (out_dir / f"{safe}.bin").write_bytes(body)
    return rec


def recon_live(name: str, cfg: dict, out_root: Path, delay: float,
               max_probes: int) -> dict:
    """A 类：挖 JS bundle 里的接口并探测。"""
    entry = {"kind": "live", "note": cfg["note"], "bundles": [],
             "candidates": [], "probes": []}
    js_dir = out_root / "_recon" / "js" / name
    probe_dir = out_root / "_recon" / "probes" / name

    # 1) 入口 HTML -> bundle 列表，同时挖内联脚本
    #    第一轮 TCMSP 栽在这里：它的 bundle 全是通用库，接口配置在页面内联 <script> 中。
    bundles: list[str] = []
    all_cands: set[str] = set()
    html_dir = out_root / "_recon" / "html" / name
    for page in cfg["entries"]:
        log(f"    入口 {page}")
        html = fetch_text(page)
        if html is None:
            continue
        html_dir.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", page)[-110:]
        (html_dir / f"{safe}.html").write_text(html[:400_000], encoding="utf-8")
        inline = mine_endpoints(html)
        if inline:
            log(f"      页面内联脚本挖出 {len(inline)} 个候选")
            all_cands.update(inline)
        parser = LinkParser()
        try:
            parser.feed(html)
        except Exception:  # noqa: BLE001, S110
            pass
        for href in parser.links:
            if re.search(r"\.js(\?|$)", href, re.I):
                bundles.append(urllib.parse.urljoin(page, href))
    bundles = sorted(set(bundles))
    log(f"    发现 {len(bundles)} 个 JS bundle")

    # 2) 下载 bundle 并挖接口
    for b in bundles[:20]:
        js_dir.mkdir(parents=True, exist_ok=True)
        fname = re.sub(r"[^A-Za-z0-9._-]", "_", b)[-100:] + ".js"
        rec = download(b, js_dir / fname, 40_000_000)
        entry["bundles"].append({"url": b, "ok": rec.get("ok"),
                                 "bytes": rec.get("bytes")})
        if not rec.get("ok"):
            continue
        text = (js_dir / fname).read_text(encoding="utf-8", errors="replace")
        cands = mine_endpoints(text)
        log(f"      {fname[:50]}: {rec.get('bytes', 0)/1e6:.2f}MB -> {len(cands)} 个候选")
        all_cands.update(cands)

    entry["candidates"] = sorted(all_cands)
    log(f"    合计 {len(all_cands)} 个候选接口，探测前 {max_probes} 个")

    # 3) 逐个探测
    origin = cfg["origin"]
    ordered = sorted(all_cands,
                     key=lambda c: (0 if re.search(r"(all|list|download|export|api)", c, re.I) else 1, len(c)))
    for extra in cfg.get("extra_probes", []):
        r = probe(extra, probe_dir, delay)
        # 这类定向探测要看响应正文而非状态码：服务端用 200 + 文案表达失败
        body = (r.get("head") or "").strip()
        r["targeted"] = True
        if body.lower().startswith("sorry"):
            r["ok"] = False
            r["verdict"] = f"服务端拒绝: {body[:60]}"
        entry["probes"].append(r)
        log(f"      {'✅' if r.get('ok') else '·'} {extra[-70:]}  {r.get('verdict') or r.get('error','')}"[:150])

    prefixes = cfg.get("prefixes", [""])
    for cand in ordered[:max_probes]:
        for pref in prefixes:
            if cand.startswith("http"):
                url = cand
            else:
                url = urllib.parse.urljoin(origin, pref + cand)
            r = probe(url, probe_dir, delay)
            entry["probes"].append(r)
            if r.get("ok"):
                log(f"      ✅ {url[:95]}  {r.get('verdict')}")
                break
            if cand.startswith("http"):
                break
    hits = [p for p in entry["probes"] if p.get("ok")]
    log(f"    探测完成：{len(hits)}/{len(entry['probes'])} 个返回可用内容")
    return entry


def wayback_list(domain: str, limit: int = 5000) -> list[dict]:
    """查 Wayback CDX，列出该域存档过的数据文件。"""
    url = ("http://web.archive.org/cdx/search/cdx"
           f"?url={urllib.parse.quote(domain)}/*&output=json"
           f"&collapse=urlkey&filter=statuscode:200&limit={limit}")
    txt = fetch_text(url, retries=3)
    if not txt:
        return []
    try:
        rows = json.loads(txt)
    except json.JSONDecodeError:
        return []
    if not rows or len(rows) < 2:
        return []
    header, *data = rows
    idx = {k: i for i, k in enumerate(header)}
    out = []
    for r in data:
        original = r[idx["original"]]
        if not DATA_EXT.search(urllib.parse.urlparse(original).path):
            continue
        out.append({
            "timestamp": r[idx["timestamp"]],
            "original": original,
            "mimetype": r[idx.get("mimetype", 3)],
            "length": r[idx.get("length", 6)] if "length" in idx else None,
            # id_ 后缀取原始未改写文件；不加会拿到注入了 Wayback 工具栏的 HTML
            "fetch_url": f"https://web.archive.org/web/{r[idx['timestamp']]}id_/{original}",
        })
    return out


def recon_dead(name: str, domains: list[str], out_root: Path,
               delay: float, max_bytes: int | None, max_files: int) -> dict:
    """B 类：从 Wayback 存档恢复。"""
    entry: dict = {"kind": "dead", "domains": domains,
                   "archived": [], "files": [], "provenance": []}
    all_rows: list[dict] = []
    for d in domains:
        log(f"    CDX 查询 {d}")
        rows = wayback_list(d)
        log(f"      存档中的数据文件: {len(rows)} 个")
        all_rows.extend(rows)
        time.sleep(delay)

    # 同一 original URL 只取最新快照
    latest: dict[str, dict] = {}
    for r in all_rows:
        prev = latest.get(r["original"])
        if prev is None or r["timestamp"] > prev["timestamp"]:
            latest[r["original"]] = r
    rows = sorted(latest.values(), key=lambda r: -int(r["timestamp"]))
    site_skip = SKIP_PER_SITE.get(name)
    kept, skipped = [], []
    for r in rows:
        fname = Path(urllib.parse.urlparse(r["original"]).path).name
        if NOT_DATA.search(fname) or NOT_DATA.search(r["original"]) or (
                site_skip and site_skip.search(fname)):
            skipped.append(r["original"])
            continue
        kept.append(r)
    if skipped:
        log(f"    跳过 {len(skipped)} 个非数据文件（站点杂项/工具包）")
        entry["skipped_not_data"] = skipped[:50]
    rows = kept
    entry["archived"] = rows[:400]
    log(f"    去重后 {len(rows)} 个唯一文件，下载前 {max_files} 个")

    out_dir = out_root / name
    for r in rows[:max_files]:
        fname = Path(urllib.parse.urlparse(r["original"]).path).name or "index"
        time.sleep(delay)
        rec = download(r["fetch_url"], out_dir / fname, max_bytes)
        rec["wayback_timestamp"] = r["timestamp"]
        rec["original_url"] = r["original"]
        entry["files"].append(rec)
        if rec.get("ok"):
            entry["provenance"].append({
                "file": fname,
                "source": "Internet Archive Wayback Machine",
                "snapshot": r["timestamp"],
                "original_url": r["original"],
                "fetch_url": r["fetch_url"],
            })
    ok = [f for f in entry["files"] if f.get("ok")]
    log(f"    取回 {len(ok)}/{len(entry['files'])} 个文件")
    if entry["provenance"]:
        pdir = out_root / name
        pdir.mkdir(parents=True, exist_ok=True)
        (pdir / "provenance.json").write_text(
            json.dumps(entry["provenance"], ensure_ascii=False, indent=2),
            encoding="utf-8")
    return entry


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data")
    ap.add_argument("--targets", default="all",
                    help="逗号分隔，或 all。可选: " + ", ".join(list(LIVE_SITES) + list(DEAD_SITES)))
    ap.add_argument("--delay", type=float, default=1.0, help="请求间隔秒（对学术站点限速）")
    ap.add_argument("--max-probes", type=int, default=120, help="每个活站最多探测多少个候选接口")
    ap.add_argument("--max-files", type=int, default=60, help="每个死站最多从存档取多少文件")
    ap.add_argument("--max-mb", type=float, default=90.0)
    args = ap.parse_args()

    socket.setdefaulttimeout(300)
    known = list(dict.fromkeys(list(LIVE_SITES) + list(DEAD_SITES)))
    names = known if args.targets.strip().lower() == "all" else [
        n.strip().lower() for n in args.targets.split(",") if n.strip()]
    unknown = [n for n in names if n not in known]
    if unknown:
        print(f"未知目标: {', '.join(unknown)}\n可选: {', '.join(known)}", file=sys.stderr)
        return 2

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    max_bytes = int(args.max_mb * 1e6) if args.max_mb > 0 else None
    report: dict = {"targets": {}, "delay": args.delay}

    for name in names:
        log(f"\n{'=' * 64}\n[{name}]\n{'=' * 64}")
        entry: dict = {}
        if name in LIVE_SITES:
            entry = recon_live(name, LIVE_SITES[name], out_root,
                               args.delay, args.max_probes)
        if name in DEAD_SITES:
            # 活站探测无果的库仍可从存档兜底，两者结果合并
            dead = recon_dead(name, DEAD_SITES[name], out_root,
                              args.delay, max_bytes, args.max_files)
            if entry:
                entry["wayback"] = dead
                entry.setdefault("files", []).extend(dead.get("files", []))
            else:
                entry = dead
        report["targets"][name] = entry

    rdir = out_root / "_recon"
    rdir.mkdir(parents=True, exist_ok=True)
    (rdir / "recon_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    log(f"\n{'=' * 64}\n侦察汇总\n{'=' * 64}")
    for name, e in report["targets"].items():
        if e.get("kind") == "live":
            hits = [p for p in e["probes"] if p.get("ok")]
            wb = e.get("wayback") or {}
            wbok = [f for f in wb.get("files", []) if f.get("ok")]
            extra = f"  存档取回 {len(wbok)}" if wb else ""
            log(f"  {name:12} [活站] bundle {len(e['bundles'])}  "
                f"候选 {len(e['candidates']):4}  可用接口 {len(hits)}{extra}")
            for h in hits[:5]:
                log(f"               ✅ {h['url'][:88]}")
        else:
            ok = [f for f in e["files"] if f.get("ok")]
            log(f"  {name:12} [死站] 存档数据文件 {len(e['archived']):4}  "
                f"取回 {len(ok)}/{len(e['files'])}")
    log(f"\n  报告: {rdir / 'recon_report.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
