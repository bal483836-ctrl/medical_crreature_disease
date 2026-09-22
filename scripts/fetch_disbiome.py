#!/usr/bin/env python3
"""
Disbiome 全量拉取：REST API -> JSON + 扁平化 CSV。

Disbiome 是这批库里唯一提供开放 API 的，因此是最先该接入的数据源。

用法:
    python3 fetch_disbiome.py --out data/disbiome
    python3 fetch_disbiome.py --out data/disbiome --endpoints experiments diseases

仅依赖标准库。
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://disbiome.ugent.be/api/disbiome"
ENDPOINTS = ["experiments", "organisms", "diseases", "publications", "methods"]
UA = "disbiome-fetch/1.0 (research use; +https://disbiome.ugent.be)"


def get_json(url: str, retries: int = 4, timeout: int = 120):
    """GET with exponential backoff (2s, 4s, 8s, 16s)."""
    delay = 2
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
                json.JSONDecodeError) as exc:
            last = exc
            if attempt == retries:
                break
            print(f"    retry {attempt + 1}/{retries} after {delay}s  ({exc})",
                  file=sys.stderr)
            time.sleep(delay)
            delay *= 2
    raise RuntimeError(f"failed to fetch {url}: {last}")


def flatten(record: dict) -> dict:
    """一层展开嵌套 dict/list，使其可写入 CSV。"""
    out = {}
    for key, val in record.items():
        if isinstance(val, dict):
            for sub_key, sub_val in val.items():
                out[f"{key}.{sub_key}"] = sub_val
        elif isinstance(val, list):
            out[key] = "; ".join(
                json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
                for v in val
            )
        else:
            out[key] = val
    return out


def write_csv(records: list[dict], path: Path) -> None:
    if not records:
        print(f"    (空，跳过 CSV) {path.name}")
        return
    flat = [flatten(r) for r in records]
    # 并集列名，保持首次出现顺序
    columns: list[str] = []
    seen = set()
    for row in flat:
        for col in row:
            if col not in seen:
                seen.add(col)
                columns.append(col)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(flat)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="data/disbiome", help="输出目录")
    parser.add_argument("--endpoints", nargs="*", default=ENDPOINTS,
                        help=f"要拉取的端点，默认全部: {' '.join(ENDPOINTS)}")
    parser.add_argument("--no-csv", action="store_true", help="只存 JSON，不转 CSV")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    failures = []
    for endpoint in args.endpoints:
        url = f"{BASE}/{endpoint}"
        print(f"[*] {endpoint}  <-  {url}")
        try:
            data = get_json(url)
        except RuntimeError as exc:
            print(f"[!] {exc}", file=sys.stderr)
            failures.append(endpoint)
            continue

        records = data if isinstance(data, list) else data.get("results", data)
        if isinstance(records, dict):
            records = [records]

        json_path = out_dir / f"{endpoint}.json"
        json_path.write_text(json.dumps(records, ensure_ascii=False, indent=2),
                             encoding="utf-8")
        print(f"[+] {json_path}  ({len(records)} 条)")

        if not args.no_csv:
            csv_path = out_dir / f"{endpoint}.csv"
            write_csv(records, csv_path)
            if csv_path.exists():
                print(f"[+] {csv_path}")

    if failures:
        print(f"\n[!] 以下端点失败: {', '.join(failures)}", file=sys.stderr)
        print("    若是 403/连接被拒，说明当前网络未放行 disbiome.ugent.be，"
              "换网络环境后重试。", file=sys.stderr)
        return 1

    print(f"\n完成。产物在 {out_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
