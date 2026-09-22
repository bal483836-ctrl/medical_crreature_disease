# datasets 分支 — 自动抓取的原始数据

由 `.github/workflows/fetch-datasets.yml` 在 GitHub runner 上抓取并提交。

- 最近一次运行: 35750608846（83708976f7a88d67f7785bb27a5afc47c1583a61）
- 抓取时间 (UTC): 2026-09-22 15:58:06
- 每个数据源一个子目录，`fetch_report.json` 记录发现的链接、文件大小与 sha256
- 超过 90MB 的文件不在此分支，见仓库 Releases

字段含义与格式说明在主分支的 `docs/`。
