# TCMSP 2.3 — 中药网络药理学的 ADME 基础库

- 官网：https://www.tcmsp-e.com/ ，旧版 https://old.tcmsp-e.com/
- 文献：Ru J, et al. *TCMSP: a database of systems pharmacology for drug discovery from herbal medicines.* Journal of Cheminformatics 2014;6:13. https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-6-13
- 分发格式：**网页表格，逐草药翻页查看**；网络图可导出 XGMML（供 Cytoscape 使用）；**无整库下载**

## 唯一的不可替代之处：ADME 参数

TCMSP 的数据量在今天已不算大，但它是**唯一系统提供十二项 ADME 相关药动学参数**的中药库：

| 参数 | 含义 | 领域惯用阈值 |
|---|---|---|
| `OB` | Oral Bioavailability 口服生物利用度（%） | **≥ 30%** |
| `DL` | Drug-Likeness 类药性 | **≥ 0.18** |
| `Caco-2` | Caco-2 细胞单层透膜性 | > -0.4 视为可吸收 |
| `BBB` | Blood-Brain Barrier 血脑屏障透过性 | > -0.3 视为可透过 |
| `HL` | Half-Life 半衰期 | |
| `MW` | 分子量 | Lipinski ≤ 500 |
| `AlogP` | 脂水分配系数 | Lipinski ≤ 5 |
| `Hdon` / `Hacc` | 氢键供体/受体数 | Lipinski ≤ 5 / ≤ 10 |
| `TPSA` | 拓扑极性表面积 | |
| `RBN` | 可旋转键数 | |
| `FASA-` | 相对溶剂可及表面积 | |

> 中药网络药理学论文里几乎人人写的那句「以 OB ≥ 30%、DL ≥ 0.18 筛选活性成分」，
> 参数来源就是 TCMSP。**如果研究要沿用这个惯例，TCMSP 无法被替代。**

## 字段说明

| 表 | 字段 |
|---|---|
| 草药 | `Herb_id`、`Herb_name_pinyin`、`Herb_name_Chinese`、`Herb_name_English`、`Herb_name_Latin` |
| 成分 | `MOL_ID`（形如 `MOL000098`）、`Molecule_name`、`MW`、`AlogP`、`Hdon`、`Hacc`、`OB`、`Caco-2`、`BBB`、`DL`、`FASA-`、`HL`、`TPSA`、`RBN` |
| 靶点 | `MOL_ID`、`Target_name`、`Gene_symbol`、`UniProt_id`、`Organism` |
| 疾病 | `MOL_ID` 或 `Target`、`Disease_name`、`Source`（TTD / PharmGKB 等） |

## 示例片段

见 [`samples/tcmsp_molecule.example.tsv`](../samples/tcmsp_molecule.example.tsv)
与 [`samples/tcmsp_mol_target.example.tsv`](../samples/tcmsp_mol_target.example.tsv)。

## 使用提示

- **没有下载入口是最大的坑**。常见做法是按草药列表逐页请求 `old.tcmsp-e.com/tcmspsearch.php`
  并解析返回的表格；旧版站点的 DOM 比新版稳定，爬取优先用 `old.`。
  注意加请求间隔，这个站点对并发很敏感。
- `MOL_ID` 是 TCMSP 的内部编号，**跨库对齐要靠 `Molecule_name` + 分子量，或先解析到 PubChem CID**。
  SymMap 的 `SMIT` 表带 `TCMSP_id` 字段，可以直接当映射表用——这是最省事的一条路。
- 靶点数量少且部分靠预测（SysDT / 加权系综相似度模型），做机制论证时应与 dbPTH / HIT 2.0 的实验证据交叉验证。
