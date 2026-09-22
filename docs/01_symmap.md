# SymMap — 中药-成分-靶点-症状-疾病

- 官网：http://www.symmap.org/
- 下载：http://www.symmap.org/download/
- 文献：Wu Y, et al. *SymMap: an integrative database of traditional Chinese medicine enhanced by symptom mapping.* Nucleic Acids Research 2019;47(D1):D1110–D1117. https://academic.oup.com/nar/article/47/D1/D1110/5150228
- 分发格式：**Excel (.xlsx) 或制表符分隔文本 (.tsv)，每个实体一个文件**，直接点链接下载

## 六大实体（SymMap 的核心设计）

SymMap 把中医与现代医学在**两个层面**对接：分子层（草药→成分→靶点→疾病）与**症状层**
（中医症状 ↔ UMLS 现代医学症状）。六个实体对应六张表：

| 表 | 实体 | 规模 |
|---|---|---|
| `SMHB` | Herb 草药 | 499（《中国药典》收录） |
| `SMIT` | Ingredient 成分 | 19,595 |
| `SMTT` | Target 靶点（基因/蛋白） | 4,302 |
| `SMDE` | Disease 疾病 | 5,235 |
| `SMTS` | TCM symptom 中医症状 | 1,717 |
| `SMMS` | MM symptom 现代医学症状 | 961 |
| `SMSY` | Syndrome 证候（较新版本新增） | 233 |

> 每张实体表还有一个对应的 **key 文件**（检索词表），结构为
> `<Entity>_id` + `Field_name`（该实体的可检索字段名）+ `Field_context`（检索词内容），
> 用于站内搜索，做数据分析时通常用不到。

## 字段说明

### SMHB（草药，约 20 个字段）

| 字段 | 含义 |
|---|---|
| `Herb_id` | SymMap 草药主键，形如 `SMHB00001` |
| `Chinese_name` | 中文名 |
| `Pinyin_name` | 拼音名 |
| `Latin_name` | 拉丁学名 |
| `English_name` | 英文名 |
| `Properties` / `Properties_English` | 药性（寒热温凉平）中/英 |
| `Meridians` / `Meridians_English` | 归经中/英 |
| `UsePart` | 药用部位 |
| `Function` / `Function_English` | 功效主治 |
| `Indication` / `Indication_English` | 适应症 |
| `Toxicity` / `Toxicity_English` | 毒性 |
| `Clinical_manifestations` | 临床表现 |
| `Therapeutic_class` / `TCM_ID` 等 | 治疗分类、交叉引用 |
| `TCMID_id`、`TCMSP_id`、`TCM-ID_id` | 到 TCMID / TCMSP / TCM-ID 的外部 ID |

### SMIT（成分）

`Ingredient_id`（`SMIT…`）、`Molecule_name`、`Alias`、`Molecular_formula`、`Molecular_weight`、
`OB_score`（口服生物利用度）、`CAS_id`、`PubChem_id`、`DrugBank_id`、`Canonical_SMILES`、`Standard_InChI`、
`Standard_InChIKey`、`TCMID_id`、`TCMSP_id`、`TCM-ID_id`。

### SMTT（靶点）

`Target_id`（`SMTT…`）、`Gene_symbol`、`Gene_name`、`Protein_name`、`Alias`、
`Ensembl_id`、`UniProt_id`、`HGNC_id`、`Chromosome`、`Gene_locus`、`TTD_id`、`DrugBank_id`。

### SMDE（疾病）

| 字段 | 含义 |
|---|---|
| `Disease_id` | 主键，形如 `SMDE00001` |
| `Disease_name` | 疾病名 |
| `Disease_definition` | 定义（部分疾病有） |
| `MeSH_id` | MeSH 交叉引用 |
| `OMIM_id` | OMIM 交叉引用 |
| `Orphanet_id` | Orphanet（罕见病）交叉引用 |

### SMTS / SMMS（症状）

- `SMTS`：`Symptom_id`、`Symptom_name`（中文）、`Symptom_pinyin`、`Symptom_definition`、`Symptom_locus`
- `SMMS`：`MM_symptom_id`、`MM_symptom_name`、`UMLS_cui`、`UMLS_semantic_type`、`MeSH_id`、`HPO_id`

### SMSY（证候）

`Syndrome_id`、`Syndrome_name`（中文）、`Syndrome_English`、`Syndrome_Pinyin`。

## 配对关系表

下载页除实体表外还提供成对关系（herb–ingredient、ingredient–target、target–disease、
herb–TCM symptom、TCM symptom–MM symptom 等），格式为两列 ID + 证据来源。
**拼链条时真正要的是这些关系表**，实体表只提供注释。

## 示例片段

见 [`samples/symmap_SMHB.example.tsv`](../samples/symmap_SMHB.example.tsv)、
[`samples/symmap_SMIT.example.tsv`](../samples/symmap_SMIT.example.tsv)、
[`samples/symmap_SMTT.example.tsv`](../samples/symmap_SMTT.example.tsv)、
[`samples/symmap_SMDE.example.tsv`](../samples/symmap_SMDE.example.tsv)。

## 使用提示

- 实体表可直接 `pandas.read_excel` / `read_csv(sep='\t')` 载入，ID 前缀即实体类型，很适合直接建图。
- 症状层是 SymMap 的独家资产：要做「症状驱动的方剂推荐」或「中西医术语对齐」，这条链在别的库里找不到。
- 靶点只有 4,302 个，覆盖率明显低于 dbPTH（27,981）和 HERB（12,933）；做靶点富集建议以 dbPTH 为主、SymMap 作交叉验证。
