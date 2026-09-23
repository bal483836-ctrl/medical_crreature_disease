# datasets 分支 — 已取得的数据

本分支**只放经过内容校验的真实数据**。未能取得的库不放占位文件。
字段说明与格式文档在主分支 `docs/`。

最后更新：2026-09-23

## ✅ 已取得（5 个库）

| 库 | 位置 | 规模 | 来源 | 备注 |
|---|---|---|---|---|
| **SymMap** | `symmap/` | 26 个 XLSX，20.97 MB | 官网 `symmap.org/download`（http only） | v1.0 与 v2.0 全套实体表；**不含配对关系表**（官网未提供） |
| **Disbiome** | `disbiome/experiments.json` | **10,866 条**，11.75 MB | **BioThings 镜像**（官网 API 不可用） | BioLink 嵌套结构；自带 NCBI 谱系与 MedDRA |
| **dbPTH** | `dbpth/` + Releases | **932 MB**（7 分片在分支，3 个大文件在 Release） | 官网 `Download.php` | 按 ProtGrp 分片，无需下 21.4 GB 整包 |
| **TCMSP** | `tcmsp/` | 4 表，7.29 MB | `browse.php` 内联全表 | 502 草药 / 13,729 成分（含 ADME）/ 3,339 靶点 / 867 疾病 |
| **TCMID** | `tcmid/` | 4 个 zip，9.25 MB | **Wayback 存档**（见 `tcmid/provenance.json`） | ⚠️ 是 **v1.0**（2015 快照），非 2.0 |

### TCMSP 数值字段是字符串
JSON 里 `"ob":"46.43"` 是字符串，直接比较会静默出错（`"9" > "30"`）。先 `pd.to_numeric` 再筛选。

### TCMID 的版本务必注意
Wayback 快照为 2015 年，文件日期 2012，对应 **TCMID 1.0**。
论文里 2.0 的统计数字（18,203 成分等）**不适用于这批文件**。实测行数：
`prescription.csv` 46,914 / `compound_protein.csv` 211,151 / `compounds.csv` 32,281 / `herb.csv` 8,203。

## ❌ 未能取得（4 个库）

| 库 | 原因（均为实测） |
|---|---|
| **HERB** | 下载接口 `/download/file/?file_path=` 本身可用，但它指向的文件在服务端已不存在（`static/...` 形式返回 `file_path dose not exists`，说明路径格式合法、文件已删）。**官方下载功能损坏。** Wayback 兜底亦无：该域存档中唯一「数据文件」是 `robots.txt`。 |
| **HIT 2.0** | 课题组 Resources 页给出的唯一地址是 `hit2.badd-cao.net`，而它只是指向 `badd-cao.net:2345` 的 frameset，该端口 Connection refused。**服务已停。** |
| **MDIPID** | `mdipid.idrblab.net` 持续返回 HTTP 500；Wayback 无任何数据文件存档。 |
| **MicrobeTCM** | Vue SPA，`/api/index/*` 经查是**文件上传**接口而非取数接口，页面无任何数据链接。Wayback 无任何存档数据文件。 |

> 曾短暂出现在本分支、现已删除的非数据文件：
> - `disbiome/{diseases,methods,organisms,publications}.json` — run #1 的 Angular 首页 HTML（假 200）
> - `herb/*` — 7 个 24 字节的 `Sorry, unavailable path.` 存根
> - `hit2/*` — 9 行演示文件与一个 **SEPPA3**（无关工具）的批量提交脚本包
> - `tcmid/{robots.txt,flash_text.txt}` — 存档里顺带抓到的站点杂项
>
> 保留它们会让人误以为这些库已取得，故一并清除。
> 抓取脚本已加入非数据黑名单（`NOT_DATA`），这些文件不会再被重新下载提交。

## 侦察证据

`_recon/` 下是各站点的前端 bundle、页面 HTML 与接口探测结果，
用于判断取数路径；`_pages/` 是早期的发现页快照。均非数据集本身。
