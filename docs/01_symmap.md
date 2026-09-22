# SymMap — 中药-成分-靶点-症状-疾病

> ✅ **已实际下载**（GitHub Actions run #1，26 个 XLSX / 21 MB）。
> 数据在 [`datasets` 分支的 `symmap/`](../../../tree/datasets/symmap)，
> 真实截取见 `samples/symmap_v*_SM*.real.tsv`。
> **本页字段说明取自下载到的真实文件表头，不是据文献推测。**

- 官网：http://www.symmap.org/ ｜ 下载：http://www.symmap.org/download/
  （注意：**只有 http 可用，https 拒绝连接**）
- 文献：Wu Y, et al. *SymMap: an integrative database of traditional Chinese medicine
  enhanced by symptom mapping.* Nucleic Acids Research 2019;47(D1):D1110–D1117.
  https://academic.oup.com/nar/article/47/D1/D1110/5150228
- 格式：**Excel (.xlsx)，每个实体一个文件**，另有配套的 `key file`（站内检索词表）

## 下载页实际提供的文件

**v1.0 与 v2.0 两套并存**，各 6–7 张实体表，每张表都有一个对应的 `key file`：

| 表 | 实体 | v1.0 行数 | v2.0 行数 |
|---|---|---:|---:|
| `SMHB` | Herb 草药 | 499 | **703** |
| `SMIT` | Ingredient 成分 | 19,595 | **27,690** |
| `SMTT` | Target 靶点/基因 | 4,302 | **20,965** |
| `SMDE` | Disease 疾病 | 5,235 | **14,434** |
| `SMTS` | TCM symptom 中医症状 | 1,717 | **2,364** |
| `SMMS` | MM symptom 现代医学症状 | 961 | **1,148** |
| `SMSY` | Syndrome 证候 | — | **233** |

⚠️ **文献里引用的数字（499 草药 / 19,595 成分 / 4,302 靶点 / 5,235 疾病）是 v1.0 的。**
v2.0 规模大得多，靶点从 4,302 涨到 20,965（近 5 倍），疾病从 5,235 涨到 14,434。
**做分析请用 v2.0**；引用文献数字时注意标明版本。`SMSY`（证候）是 v2.0 才有的表。

## 真实字段（下载文件的实际表头）

### SMHB 草药

**v1.0（14 列）**
```
Herb_id  Chinese_name  Pinyin_name  Latin_name  English_name
Properties  Meridians  Function  Class_Chinese  Class_English  UsePart
TCMID_id  TCM-ID_id  TCMSP_id
```

**v2.0（19 列）**——药性与归经拆成中英两列，并新增别名与 HERB 交叉引用
```
Herb_id  Chinese_name  Pinyin_name  Latin_name  English_name
Properties_Chinese  Properties_English  Meridians_Chinese  Meridians_English
Class_Chinese  Class_English  UsePart
TCMID_id  TCM-ID_id  TCMSP_id  Link_herb_id  Alias  HERBDB_ID  Suppress
```

实际数据长这样（v1.0 第 1 行）：

| Herb_id | Chinese_name | Pinyin_name | Properties | Meridians | Class_Chinese |
|---|---|---|---|---|---|
| 1 | 矮地茶 | Ai Di Cha | Mild,Pungent,Bitter | Lung,Liver | 止咳平喘药 |

**要点**：
- `Herb_id` 是**纯整数**（1, 2, 3…），不是 `SMHB00001` 那种带前缀的字符串。其它表同理。
- `Properties` / `Meridians` 是**逗号分隔的多值字段**，英文，需要 split 后才能用。
- `Function` 是编号的自由文本（"1. To … 2. To …"），不是结构化字段。

### SMIT 成分

**v1.0（12 列）**
```
MOL_id  Molecule_name  Molecule_structure  Molecule_formula  Molecule_weight
OB_score  Alias  PubChem_id  CAS_id  TCMID_id  TCM-ID_id  TCMSP_id
```

**v2.0（15 列）**
```
Mol_id  Molecule_name  PubChem_CID  Molecule_structure  Molecule_formula
Molecule_weight  OB_score  CAS_id  TCMID_id  TCM-ID_id  TCMSP_id
Version  Type  Link_ingredient_id  Suppress
```

**要点**：主键叫 `MOL_id`（v1.0）/ `Mol_id`（v2.0），**不是 `Ingredient_id`**。
`Molecule_structure` 存的是结构串（SMILES）。**没有 InChIKey 列**——跨库按结构对齐要先自行从
SMILES 算 InChIKey，或走 `PubChem_id` / `PubChem_CID`。

### SMTT 靶点

**v1.0（18 列）**
```
Gene_id  Gene_symbol  Chromosome  Gene_name  Protein_name
HIT_id  TCMSP_id  Ensembl_id  NCBI_id  HGNC_id  Vega_id
GenBank_Gene_id  GenBank_Protein_id  UniProt_id  PDB_id  OMIM_id
miRBase_id  IMGT/GENE-DB_id
```
v2.0（20 列）把 `OMIM_id` 改名为 `MIM_id`，并加 `Version`、`Suppress`。

**要点**：主键叫 `Gene_id`，**不是 `Target_id`**。交叉引用非常全（12 个外部库 ID），
其中 **`HIT_id` 直接指向 HIT 2.0**，**`TCMSP_id` 直接指向 TCMSP**——
这两列让 SymMap 成为现成的跨库映射表，省掉自己做基因名对齐。

### SMDE 疾病

**v1.0（9 列）**
```
Disease_id  Disease_Name  Disease_definition
MeSH_id  OMIM_id  Orphanet_id  ICD10CM_id  UMLS_id  MedDRA_id
```
v2.0（12 列）额外有 `Version`、`Link_disease_id`、`Suppress`。

**要点（重要）**：SMDE **自带 `MedDRA_id` 和 `UMLS_id`**。
这意味着 **SymMap 的疾病可以直接和 Disbiome（MedDRA 编码）做 join**，
不需要再经 UMLS 绕一圈做 MedDRA↔MeSH 映射。这是把中药链条接到微生物链条上最省事的一个接口。
注意列名是 `Disease_Name`，**N 大写**。

### SMTS 中医症状 / SMMS 现代医学症状

```
SMTS v1.0 (6):  TCM_symptom_id  TCM_symptom_name  Symptom_pinyin_name
                Symptom_definition  Symptom_locus  Symptom_property
SMTS v2.0 (9):  … Symptom_pinYin（拼写变了）… + Type  Version  Suppress
SMMS v1.0 (9):  MM_symptom_id  MM_symptom_name  MM_symptom_definition
                MeSH_tree_numbers  UMLS_id  OMIM_id  ICD10CM_id  HPO_id  MeSH_id
SMMS v2.0 (11): … + Version  Suppress
```
⚠️ v1.0 的 `Symptom_pinyin_name` 在 v2.0 变成了 `Symptom_pinYin`——**跨版本合并时会踩坑**。

### SMSY 证候（仅 v2.0）

```
Syndrome_id  Syndrome_name  Syndrome_English  Syndrome_PinYin
Syndrome_definition  Version  Type  Suppress
```

实际数据：

| Syndrome_id | Syndrome_name | Syndrome_English | Syndrome_PinYin | Version |
|---|---|---|---|---|
| 1 | 下元虚冷 | deficiency-cold of kidney | Xia Yuan Xu Leng | v1,v2 |
| 2 | 下脘虚冷 | deficiency-cold of abdomen | Xia Wan Xu Leng | v2 |

## v2.0 新增的三个管理字段

`Version`（该行出现在哪些版本，如 `v1,v2`）、`Suppress`（标记是否废弃）、
`Link_*_id`（指向合并后的主记录）。

**载入数据时应当先按 `Suppress` 过滤掉废弃记录**，否则会把已撤销的条目算进统计。

## ⚠️ 关键限制：下载页**没有**配对关系表

实测下载页上的全部静态链接共 26 个，**就是上面那 6–7 张实体表及其 key 文件，
再无其它**。herb–ingredient、ingredient–target、target–disease、
herb–TCM symptom、TCM symptom–MM symptom 这些**成对关系表不在批量下载范围内**。

这意味着：

- **光靠批量下载无法建出 SymMap 的网络**，拿到的只是各实体的注释信息。
- 关系数据只能从网页检索结果里取（每查一个实体返回其关联列表），需要按实体逐个抓取。
  以 v2.0 的 703 味草药为起点逐个请求，是最小可行的抓取规模。
- 若只需要注释和跨库 ID 映射（如用 `SMTT.HIT_id` / `SMTT.TCMSP_id` / `SMDE.MedDRA_id`
  做对齐），批量下载的这 26 个文件已经够用。

> 本仓库早先的版本称「下载页除实体表外还提供成对关系」，与实测不符，已更正。

另注：v2.0 `SMIT` 的 `Type` 列记录的是**草药与成分的关联类型**
（QC / blood / metabolic 等），可据此区分质控成分、入血成分与代谢产物。

## 使用提示

- `openpyxl` 直接读；`Herb_id` 等主键是整数，建图前统一转成 `str` 加前缀，避免不同表的 ID 撞号。
- 用 v2.0，别用 v1.0（除非要复现引用 v1.0 数字的老论文）。
- SMTT 的 `HIT_id` / `TCMSP_id` 和 SMDE 的 `MedDRA_id` / `UMLS_id` 是跨库对齐的现成锚点，优先用。
