# 下载可达性探测结果（本会话实测）

探测时间：2026-09-22
探测方式：`curl -sS -o /dev/null -w "%{http_code}" -m 15 https://<host>/`（经会话出口代理）

## 结论

**9 个数据库的全部域名均被出口网络策略在 CONNECT 阶段拒绝（HTTP 403），本会话无法下载任何一个数据集。**

这不是站点故障，也不是 TLS 问题——是运行环境的组织级出口白名单只放行 GitHub 与少数包管理源
（实测 `api.github.com`、`raw.githubusercontent.com`、`pypi.org` 可通；`example.com`、`google.com`、
`zenodo.org`、`figshare.com`、`ncbi.nlm.nih.gov` 同样 403）。
两条抓取通道（本地 `curl` 与 WebFetch）均被同一策略拦截，WebFetch 返回 `EGRESS_BLOCKED`。

## 明细

| 域名 | 所属数据库 | 结果 |
|---|---|---|
| `www.symmap.org` / `symmap.org` | SymMap | 403 CONNECT tunnel failed |
| `mdipid.idrblab.net` | MDIPID | 403 CONNECT tunnel failed |
| `disbiome.ugent.be` | Disbiome | 403 CONNECT tunnel failed |
| `www.microbetcm.com` | MicrobeTCM | 403 CONNECT tunnel failed |
| `dbpth.biocuckoo.cn` | dbPTH 1.0 | 403 CONNECT tunnel failed |
| `bionet.ncpsb.org.cn` | dbPTH（旧镜像） | 403 CONNECT tunnel failed |
| `tcmid.org` | TCMID 2.0 | 403 CONNECT tunnel failed |
| `www.tcmip.cn` | TCMID 相关 | 403 CONNECT tunnel failed |
| `old.tcmsp-e.com` / `tcmsp-e.com` | TCMSP 2.3 | 403 CONNECT tunnel failed |
| `herb.ac.cn` | HERB / HERB 2.0 | 403 CONNECT tunnel failed |
| `hit2.badd-cao.net` | HIT 2.0 | 403 CONNECT tunnel failed |
| `pending.biothings.io` | Disbiome 的 BioThings 镜像 | 403 CONNECT tunnel failed |

## 对照组（确认策略而非故障）

| 域名 | 结果 |
|---|---|
| `api.github.com` | 200 ✅ |
| `raw.githubusercontent.com` | 301 ✅ |
| `pypi.org` | 200 ✅ |
| `example.com` | 403 ❌ |
| `www.google.com` | 403 ❌ |
| `zenodo.org` | 403 ❌ |

## 要真正拿到数据，两条路

1. **换环境**：在本机 / 服务器 / 放行了这些域名的环境里运行 `scripts/download_all.sh`，
   脚本已按各库的真实下载入口写好。
2. **改策略**：请管理员把上表左列域名加入本会话环境的出口白名单，然后在新会话里重跑脚本。

（`scripts/check_hosts.sh` 可在任意环境复现这张表，用来确认你的网络放行到哪一步。）
