# MDIPID — 微生物-药物-疾病（三向）

- 官网：https://idrblab.org/mdipid/ ，镜像 https://mdipid.idrblab.net/
- 文献：Yin J, et al. *MDIPID: Microbiota-drug interaction and disease phenotype interrelation database.* iMeta 2025. https://onlinelibrary.wiley.com/doi/full/10.1002/imt2.70019 ｜ PMC11995188
- 分发格式：**Web 界面动态展示，交互表格**；无公开的整库打包下载，部分页面支持导出
- 无需注册登录

## 三类关系（MDIPID 的数据骨架）

| 代号 | 全称 | 方向 | 规模 |
|---|---|---|---|
| `MMDR` | Microbiota & their related proteins Modulation on Drug Response | 微生物 → 药物 | 6,669 条；628 个微生物物种调控 881 个药物；592 个微生物相关蛋白（MRPs）来自 282 个物种；15 类调控方式（代谢修饰、螯合、活化等） |
| `DEIM` | Drug or other Exogenous substances Impact on Microbiota | 药物 → 微生物 | 11,760 条；1,066 个药物/外源物引起 921 种微生物丰度变化；10 类影响方式（提高/降低相对丰度、抑制生长等） |
| `MBDA` | MicroBiota-Disease Associations | 微生物 ↔ 疾病 | 15,146 条；2,209 个微生物物种与 482 种疾病；10 类变化类型（decrease、increase、enrich 等） |

合计覆盖 **1,818 个药物/外源物、2,708 个微生物物种、482 种疾病、592 个微生物相关蛋白**。

## 字段说明

### DEIM（药物影响微生物）— 最常用的一张表

| 字段 | 含义 | 取值示例 |
|---|---|---|
| `Drug` | 药物 / 外源物名称 | Finasteride |
| `Microbiota` | 微生物物种 / 分类单元 | Ruminococcaceae UCG-002 |
| `Variation` | 丰度变化方向 | Decrease / Increase |
| `Sample Site` | 采样部位 | Stool（肠道）、Oral（口腔） |
| `Model` | 实验模型 | Mouse（小鼠）、Zebrafish（斑马鱼）、Human |
| `Mechanism` | 作用机制描述 | 自由文本 |
| `Reference` | 文献出处（PMID） | |

> 官网检索 "Finasteride" 的实际返回：**Ruminococcaceae UCG-002 丰度减少，样本来源 Stool**。

### MMDR（微生物调控药物应答）

`Microbiota`（物种）、`Microbiota-related Protein`（MRP，含 UniProt ID）、`Drug`、
`Modulation Type`（15 类之一：metabolic modification / sequestration / activation …）、
`Effect on Drug Response`、`Model`、`Mechanism`、`Reference`。

### MBDA（微生物-疾病关联）

`Microbiota`、`Disease`、`Variation`（decrease / increase / enrich …，10 类）、
`Sample Site`、`Cohort / Model`、`Detection Method`、`Reference`。

## 示例片段

见 [`samples/mdipid_DEIM.example.tsv`](../samples/mdipid_DEIM.example.tsv)、
[`samples/mdipid_MMDR.example.tsv`](../samples/mdipid_MMDR.example.tsv)、
[`samples/mdipid_MBDA.example.tsv`](../samples/mdipid_MBDA.example.tsv)。

## 使用提示

- **没有批量下载接口是最大障碍**。实际取数要么按药物/微生物/疾病列表逐个查询页面抓取，
  要么直接联系作者索取。建库前先评估这部分工作量。
- MDIPID 与 Disbiome 在 MBDA 这一层**有重叠**，但 Disbiome 标准化（MedDRA + NCBI/SILVA）做得更彻底、
  且有 API；建议 **Disbiome 打底 + MDIPID 补充**，而不是反过来。
- MDIPID 独有价值在 **MMDR**——「微生物如何改变药效」这个方向，Disbiome 和 MicrobeTCM 都没有。
  如果研究目标涉及中药成分被肠菌代谢转化，这张表是关键。
