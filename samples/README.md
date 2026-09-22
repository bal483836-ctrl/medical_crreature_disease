# samples/ — 数据片段

本目录有**两类**文件，务必区分：

## 1. `*.real.tsv` —— 真实数据 ✅

从实际下载的数据集里截取的前 5 行，**可以直接引用**。
目前只有 SymMap 有（GitHub Actions run #1 抓取成功），
原始文件在 [`datasets` 分支](../../../tree/datasets/symmap)。

## 2. `*.example.tsv` / `*.example.json` —— 占位示例 ⚠️

其余 8 个库尚未下载成功（站点 404/500/拒绝连接，见 `../DOWNLOAD_STATUS.md`），
这些文件是**依据官方文档与原始论文还原的「列结构示例」**，用于展示：

- 每张表有哪些列、列名怎么写
- 每一列的取值形态（ID 格式、枚举值、单位、分隔符）
- 表与表之间靠哪个字段连接

**取值本身是占位内容，不可用于任何分析、统计或引用。**
少数几行取自各库论文中公开举例的真实记录（如 Disbiome 的
"Faecalibacterium 在 Stevens-Johnson 综合征中减少"、MDIPID 的
"Finasteride → Ruminococcaceae UCG-002 减少, Stool"），这些行在文件中有标注。

> SymMap 的占位示例已被真实数据取代并删除。**这也说明占位示例不可尽信**：
> 真实表头与我按文献还原的版本有多处出入——主键是整数而非 `SMHB00001` 式字符串，
> 成分表主键叫 `MOL_id` 而非 `Ingredient_id`，靶点表主键叫 `Gene_id` 而非 `Target_id`，
> 且疾病表自带 `MedDRA_id`。其余 8 个库的占位示例很可能有同类偏差，
> **拿到真实数据前不要据此写解析代码**。

## 文件清单

| 文件 | 对应表 |
|---|---|
| `symmap_v1_0_*.real.tsv`（6 张） | **SymMap v1.0 真实数据** ✅ |
| `symmap_v2_0_*.real.tsv`（7 张） | **SymMap v2.0 真实数据** ✅ |
| `mdipid_DEIM.example.tsv` | MDIPID 药物影响微生物 |
| `mdipid_MMDR.example.tsv` | MDIPID 微生物调控药物应答 |
| `mdipid_MBDA.example.tsv` | MDIPID 微生物-疾病关联 |
| `disbiome_experiments.example.json` | Disbiome API 返回 |
| `disbiome_experiments.example.csv` | Disbiome CSV 导出 |
| `microbetcm_herb_microbe.example.tsv` | MicrobeTCM 中药→微生物 |
| `microbetcm_prediction.example.tsv` | MicrobeTCM 预测得分表 |
| `dbpth_ITI.example.tsv` | dbPTH 成分-靶点互作 |
| `tcmid_prescription.example.tsv` | TCMID 复方 |
| `tcmid_ingredient_target.example.tsv` | TCMID 成分-靶点 |
| `tcmsp_molecule.example.tsv` | TCMSP 成分 + ADME |
| `tcmsp_mol_target.example.tsv` | TCMSP 成分-靶点 |
| `herb_herb.example.tsv` | HERB 草药 |
| `herb_ingredient_target.example.tsv` | HERB 成分-靶点 |
| `hit2_ingredient_target.example.tsv` | HIT 2.0 成分-靶点活性 |
