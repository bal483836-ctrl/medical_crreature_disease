# dbPTH 1.0 — 中药成分-靶点（实验验证，覆盖率最高）

- 官网：http://dbpth.biocuckoo.cn/
- 文献：Peng J, Huang X, Yang K, Wang N, Peng D, Tian S, Xue Y, Chen J. *dbPTH: A Comprehensive Database for Protein Targets of Herbal Ingredients.* Genomics, Proteomics & Bioinformatics 2026. https://academic.oup.com/gpb/advance-article/doi/10.1093/gpbjnl/qzag040/8703982
- 分发格式：整库打包下载，**数据量约 21.4 GB**
- 免费访问

## 规模与相对优势

| 指标 | 数量 |
|---|---|
| 实验验证的成分-靶点互作（ITI） | **165,967** |
| 蛋白靶点 | **27,981** |
| 草药成分 | **4,856** |
| 覆盖物种 | **8** |

相对同类库的实验验证 ITI 数量增幅：

| 对比库 | 增幅 |
|---|---|
| TCMSP | **41.81×** |
| HERB | **34.47×** |
| HIT 2.0 | **16.55×** |
| BATMAN-TCM 2.0 | **9.72×** |

**跨物种同源靶点映射**是它的另一个特色：人以外还覆盖小鼠、大鼠等 7 个物种，
并提供同源基因对应关系——做动物实验验证或跨物种外推时直接可用。

## 字段说明

核心为成分-靶点互作表，典型字段：

| 字段 | 含义 |
|---|---|
| `Ingredient_ID` | dbPTH 成分主键 |
| `Ingredient_name` | 成分名 |
| `PubChem_CID` / `InChIKey` / `SMILES` | 化学标识符（跨库对齐用这几个） |
| `Target_ID` | 靶点主键 |
| `Gene_symbol` / `UniProt_ID` | 基因符号 / UniProt 登录号 |
| `Species` | 靶点所属物种（8 个之一） |
| `Homolog_group` | 跨物种同源组 ID |
| `Interaction_type` | 互作类型（结合/抑制/激活等） |
| `Assay / Method` | 实验方法 |
| `Activity_value` / `Activity_type` | 活性值与类型（IC50 / Kd / Ki …） |
| `Evidence_source` | 证据来源库或文献 |
| `PMID` | 文献 |
| `Herb` | 该成分所属草药（若有） |

## 示例片段

见 [`samples/dbpth_ITI.example.tsv`](../samples/dbpth_ITI.example.tsv)。

## 使用提示

- **21.4 GB** 不是随手下载的体量：预留磁盘、用断点续传（`curl -C -` / `wget -c`），
  落地后建议先按 `Species == 'Homo sapiens'` 过滤再入库，人类子集通常小一个量级。
- 它**只覆盖「成分→靶点」一段**，没有草药-成分归属（部分有 `Herb` 字段）、也没有靶点-疾病。
  标准组合是：**草药-成分用 SymMap/HERB，成分-靶点用 dbPTH，靶点-疾病用 DisGeNET/OMIM/HERB**。
- 跨库对齐成分时，**用 InChIKey 而不是成分名**——中药成分的同名异物/异名同物非常多。
