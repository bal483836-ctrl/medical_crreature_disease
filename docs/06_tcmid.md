# TCMID 2.0 — 复方粒度 + 质谱数据

- 官网：http://www.tcmid.org/ （历史地址 http://www.megabionet.org/tcmid/）
- 文献：Huang L, Xie D, et al. *TCMID 2.0: a comprehensive resource for TCM.* Nucleic Acids Research 2018;46(D1):D1117–D1120. https://academic.oup.com/nar/article/46/D1/D1117/4584630
- 分发格式：**纯文本（.txt）分表打包下载**
- 注意：站点历史上多次迁移/不可用，下载前先确认可达

## 规模

| 实体 | 数量 |
|---|---|
| 草药成分 | 18,203 |
| 药物 | 1,356 |
| 疾病 | 842 |
| 草药质谱图谱 | 778 张（覆盖 170 味草药） |
| 成分质谱图谱 | 3,895 张（覆盖 729 个成分） |

## 两个差异化价值

**1. 复方粒度。** TCMID 是少数系统收录**复方（prescription）及其组成**的库。
2.0 版特别考虑到「煎煮过程中会发生化学变化、产生新成分」，因此**单独收集了复方层面的成分**，
而不是简单地把各味药的成分做并集——这对复方研究很重要。

**2. 质谱数据。** 778 张草药 MS 谱用于展示不同产地药材的质量差异、辨别道地药材；
3,895 张成分 MS 谱作为成分鉴定的佐证材料。这是其它库都没有的。

## 字段说明（主要分表）

| 表 | 关键字段 |
|---|---|
| `prescription` | `Prescription_id`、`Chinese_name`、`Pinyin_name`、`Composition`（组成草药列表）、`Indication`、`Source`（出处方书） |
| `herb` | `Herb_id`、`Chinese_name`、`Pinyin_name`、`Latin_name`、`English_name`、`Properties`、`Meridians`、`Function`、`Indication` |
| `ingredient` | `Ingredient_id`、`Ingredient_name`、`Herb`、`Molecular_formula`、`Molecular_weight`、`PubChem_id`、`CAS`、`SMILES` |
| `target` | `Target_id`、`Gene_symbol`、`UniProt_id`、`Ingredient`、`Evidence`、`PMID` |
| `disease` | `Disease_id`、`Disease_name`、`OMIM_id`、`MeSH_id` |
| `drug` | `Drug_id`、`Drug_name`、`DrugBank_id`、`Target`、`Indication` |
| `spectrum` | `Spectrum_id`、`Herb / Ingredient`、`Origin`（产地）、`MS_type`、`File`（谱图文件） |

关系表以 ID 对的形式提供：prescription–herb、herb–ingredient、ingredient–target、target–disease、target–drug。

## 示例片段

见 [`samples/tcmid_prescription.example.tsv`](../samples/tcmid_prescription.example.tsv)
与 [`samples/tcmid_ingredient_target.example.tsv`](../samples/tcmid_ingredient_target.example.tsv)。

## 使用提示

- **靶点侧很薄**（2.0 版仅 82 个相关靶点级别的新增），不要拿 TCMID 当靶点来源；
  它的价值在复方和质谱，靶点交给 dbPTH / HERB。
- 数据较老（2018），成分与靶点的交叉引用 ID 可能已失效，入库后建议用 PubChem/UniProt 重新解析一遍。
- 复方表的 `Composition` 常是自由文本的药味列表，需要做一次中文药名解析与标准化
  （可用 SymMap 的 `Chinese_name` / `Pinyin_name` 做词表对齐）。
