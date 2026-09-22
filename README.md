# datasets 分支 — 自动抓取的原始数据

由 `.github/workflows/fetch-datasets.yml` 在 GitHub runner 上抓取并提交。

- 最近一次运行: 35752586629（675368f01e6d73157f85ed4a494b501462acc982）
- 抓取时间 (UTC): 2026-09-22 16:21:34
- 每个数据源一个子目录，`fetch_report.json` 记录发现的链接、文件大小与 sha256
- 超过 90MB 的文件不在此分支，见仓库 Releases

字段含义与格式说明在主分支的 `docs/`。
