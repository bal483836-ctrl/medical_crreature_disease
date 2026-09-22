# HERB / HERB 2.0 — 规模最大的综合库，唯一带临床证据层

- 官网：http://herb.ac.cn/ ，下载：http://herb.ac.cn/Download/
- 文献：
  - Fang S, et al. *HERB: a high-throughput experiment- and reference-guided database of traditional Chinese medicine.* Nucleic Acids Research 2021;49(D1):D1197–D1206. https://academic.oup.com/nar/article/49/D1/D1197/6017358
  - *HERB 2.0: an updated database integrating clinical and experimental evidence for traditional Chinese medicine.* Nucleic Acids Research 2025;53(D1):D1404. https://academic.oup.com/nar/article/53/D1/D1404/7903361
- 分发格式：下载页提供**分表文件**（草药、成分、靶点、疾病及各配对关系），免注册

## 规模

| 实体 | 数量 |
|---|---|
| 草药 | 7,263 |
| 成分 | 49,258 |
| 基因靶点 | 12,933 |
| 疾病关联 | 28,212 |

提供中药-成分-靶点-疾病之间的**六种两两配对关系**（herb–ingredient、herb–target、herb–disease、
ingredient–target、ingredient–disease、target–disease）。

## 两个差异化价值

**1. 高通量实验证据。** 不同于纯文献挖掘的库，HERB 整合了中药处理后的**基因表达谱**
（高通量实验数据），可以直接看某味药/成分处理后哪些基因被显著调控。HERB 2.0 更新到 2,231 项高通量实验。

**2. 临床证据层（2.0 新增，本批 9 个库里独一份）。**
- 收录 **8,558 项临床试验** 与 **8,032 项 meta 分析**
- 为其中 **1,941 项临床试验** 和 **593 项 meta 分析** 提取了**明确的临床结论**
- 人工策展文献扩充到 6,644 篇

## 字段说明

| 表 | 关键字段 |
|---|---|
| `herb` | `Herb_id`（`HERB000xxx`）、`Herb_pinyin_name`、`Herb_cn_name`、`Herb_en_name`、`Herb_latin_name`、`Properties`、`Meridians`、`UsePart`、`Function`、`Indication`、`Toxicity`、`Clinical_manifestations`、`TCMID_id`、`TCMSP_id`、`SymMap_id` |
| `ingredient` | `Ingredient_id`（`HBIN…`）、`Ingredient_name`、`Alias`、`Ingredient_formula`、`Ingredient_Smile`、`Ingredient_weight`、`OB_score`、`CAS_id`、`PubChem_id`、`DrugBank_id`、`HERB_target_ids` |
| `target` | `Target_id`（`HBTAR…`）、`Gene_symbol`、`Gene_name`、`Ensembl_id`、`UniProt_id`、`HGNC_id`、`TTD_id` |
| `disease` | `Disease_id`（`HBDIS…`）、`Disease_name`、`DisGeNET_disease_id`、`OMIM_id`、`MeSH_id`、`TTD_id`、`Drugbank_DisGeNET_id` |
| 关系表 | 两列实体 ID + `Evidence_type`（Reference / Experiment）+ `PMID` / `Experiment_id` |
| `experiment`（2.0） | `Experiment_id`、`Herb / Ingredient`、`Platform`、`Tissue / Cell line`、`DEG_list`、`GEO_id` |
| `clinical_trial`（2.0） | `Trial_id`、`Intervention`、`Condition`、`Phase`、`Sample_size`、`Conclusion`、`Registry_id` |

## 示例片段

见 [`samples/herb_herb.example.tsv`](../samples/herb_herb.example.tsv)、
[`samples/herb_ingredient_target.example.tsv`](../samples/herb_ingredient_target.example.tsv)。

## 使用提示

- **跨库对齐的最佳枢纽**：HERB 的 herb 表同时带 `TCMID_id`、`TCMSP_id`、`SymMap_id`，
  disease 表带 `DisGeNET / OMIM / MeSH / TTD` ID。要把这批库连起来，**以 HERB 为中心表做 join 最省事**。
- 关系表要注意区分 `Evidence_type`：Reference（文献人工策展，可信度高）
  与 Experiment（高通量差异表达推断，噪声大）。做机制论证时应分开统计，不要混算。
- 草药数 7,263 远超 SymMap 的 499——因为 HERB 不限于《中国药典》收录品种。
  如果研究范围限定药典内，需要先用 SymMap 的草药列表过滤。
