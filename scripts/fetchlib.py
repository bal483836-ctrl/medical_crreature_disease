#!/usr/bin/env python3
"""共享的抓取原语 —— gh_fetch.py 与 gh_recon.py 都用这一份。

抽出来是为了避免两份实现漂移：特别是 looks_like_html() 这道内容校验闸门，
它挡下过 Disbiome 的 4 份「HTTP 200 但其实是 SPA 首页」的假成功。
侦察脚本必须用同一套判断，否则会得出互相矛盾的结论。
"""
from __future__ import annotations

import hashlib
import json
import re
import ssl
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
