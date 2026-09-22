# dbPTH 1.0 — 中药成分-靶点（覆盖率最高）

> ✅ **已实际下载**（Actions run #3）：**10 个文件，932 MB**。
> 小于 90MB 的 7 个分片在 [`datasets` 分支的 `dbpth/`](../../../tree/datasets/dbpth)，
> 超限的 3 个（`PTH.sql.zip` 346MB、`Enzyme.zip` 298MB、`Other.zip` 126MB）
> 在 [Releases](../../../releases)。真实截取见 `samples/dbpth_Secreted_Protein.real.tsv`。
> **本页字段取自解压后的真实文件。**

- 官网：http://dbpth.biocuckoo.cn/ ｜ 下载页：**`/Download.php`**（注意是 `.php`，`/Download/` 会 403）
- 文献：Peng J, Huang X, Yang K, Wang N, Peng D, Tian S, Xue Y, Chen J.
  *dbPTH: A Comprehensive Database for Protein Targets of Herbal Ingredients.*
  Genomics, Proteomics & Bioinformatics 2026.
  https://academic.oup.com/gpb/advance-article/doi/10.1093/gpbjnl/qzag040/8703982

## 🎯 重要：不必下 21.4 GB 整库

实测下载页列出 **1,325 个 zip 分片**，整库被按两种方式切开：

| 分片方式 | 说明 |
|---|---|
| `Download/ProtGrp/*.zip` | **按蛋白分组**，9 个文件即完整覆盖全库 |
| `Download/IngCls/*.zip` | **按成分分类**，同一批数据的另一种切法 |
| `Download/PTH.zip` | 整库打包，**约 21.4 GB** |
| `Download/PTH.sql.zip` | 整库 SQL dump，**346 MB**（要建数据库用这个） |

**按 ProtGrp 取 9 个分片（实测合计 586 MB）即可得到全库**，无需碰 21.4 GB 的整包：

| 分片 | 大小 | 落位 |
|---|---:|---|
| `Enzyme.zip` | 297.80 MB | Release |
| `Other.zip` | 125.78 MB | Release |
| `Other_Cytosolic_Protein.zip` | 67.40 MB | 分支 |
| `Transcription_Factor.zip` | 22.86 MB | 分支 |
| `Epigenetic_Regulator.zip` | 20.19 MB | 分支 |
| `Ion_Channel.zip` | 16.62 MB | 分支 |
| `Membrane_Receptor.zip` | 14.51 MB | 分支 |
| `Transporter.zip` | 12.05 MB | 分支 |
| `Secreted_Protein.zip` | 8.98 MB | 分支 |

另外单独取了 `PTH.sql.zip`（346 MB，Release）。

## 规模

| 指标 | 数量 |
|---|---|
| 实验验证的成分-靶点互作（ITI） | 165,967 |
| 蛋白靶点 | 27,981 |
| 草药成分 | 4,856 |
| 覆盖物种 | 8（文献口径，实测分片内物种数远多于 8，见下） |

相对同类库的实验验证 ITI 增幅：TCMSP **41.81×**、HERB **34.47×**、HIT 2.0 **16.55×**、
BATMAN-TCM 2.0 **9.72×**。

## 真实字段（解压后的 .txt，制表符分隔）

每个 zip 里是一个同名 `.txt`。以 `Secreted_Protein.txt` 为例，**实测 587,330 行、9 列**：

```
dbPTH ID | Protein Accession | Protein Name | Gene | Ingredient | PubChem |
Chemical Subtype | Protein Subgroups | Specie
```

实际数据：

| dbPTH ID | Protein Accession | Protein Name | Gene | Ingredient | PubChem | Chemical Subtype | Protein Subgroups | Specie |
|---|---|---|---|---|---|---|---|---|
| PTHT0000272 | A0A0G2JGF1 | Interleukin 6 receptor, alpha | Il6ra | Cysteine | 5862 | Small peptides | Secreted_Protein@Membrane_Receptor | Mus musculus (Mouse) |
| PTHT0000272 | A0A0G2JGF1 | Interleukin 6 receptor, alpha | Il6ra | alpha-D-Mannopyranose | 185698 | Saccharides | Secreted_Protein@Membrane_Receptor | Mus musculus (Mouse) |

**字段说明**：

| 字段 | 含义 |
|---|---|
| `dbPTH ID` | 靶点主键，形如 `PTHT0000272`（同一蛋白的多条成分记录共用一个 ID） |
| `Protein Accession` | UniProt 登录号 |
| `Protein Name` / `Gene` | 蛋白名 / 基因符号 |
| `Ingredient` | 成分名 |
| `PubChem` | 成分的 PubChem CID —— **跨库对齐用这一列** |
| `Chemical Subtype` | 成分化学分类（Flavonoids、Saccharides、Steroids、Small peptides…） |
| `Protein Subgroups` | 蛋白分组，**可多值，用 `@` 分隔**（如 `Secreted_Protein@Membrane_Receptor`） |
| `Specie` | 靶点所属物种，格式为 `学名 (俗名)` |

## ⚠️ 与文献描述的差异（实测）

本仓库早先按文献推测的字段（`Interaction_type`、`Activity_type`、`Activity_value`、
`Assay/Method`、`PMID`、`Homolog_group`、`Evidence_source`）**在实际文件里都不存在**。
真实的分片文件只有上面 9 列，**没有活性值、没有实验方法、没有文献 PMID、没有显式的同源组 ID**。

这对用法的影响很直接：

- **dbPTH 给的是「某成分与某蛋白有实验验证的互作」这一事实，不含强度与证据细节。**
  需要活性值（IC50/Kd）或实验方法，得用 **HIT 2.0**（它带活性值与证据质量标签）。
- 跨物种同源映射不是靠一个 `Homolog_group` 列，而是通过**同一 `dbPTH ID` 下出现多个物种的
  `Protein Accession`** 来体现——按 `dbPTH ID` 分组即可得到同源蛋白集合。
- 实测单个分片里的 `Specie` 远多于文献所说的 8 个物种（`Secreted_Protein.txt` 里出现了
  兔、青鳉、山羊、犬、白眉猴、金丝猴、大熊猫等），**做人类研究务必先按
  `Specie` 过滤到 `Homo sapiens`**，否则会把大量非人物种的记录算进去。

`Secreted_Protein.txt` 实测：22,809 个唯一蛋白、3,395 个唯一成分、587,330 行。
`Chemical Subtype` 分布：Other 183,112 / Flavonoids 42,631 / Saccharides 39,182 /
Steroids 30,423 / Small peptides 30,158 / Fatty Acids and Conjugates 30,079。

## 使用提示

- **先按 `Specie` 过滤人类子集再入库**，体量会小一个量级。
- 跨库对齐成分**用 `PubChem` CID，不要用 `Ingredient` 名**——中药成分同名异物/异名同物非常多。
- `Protein Subgroups` 的 `@` 多值要 split，否则按分组统计会漏。
- 要建数据库直接用 `PTH.sql.zip`（Release 里，346 MB），比解析 9 个分片省事。
