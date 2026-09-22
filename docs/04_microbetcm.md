# MicrobeTCM — 中药-微生物-疾病（最接近完整链条）

- 官网：https://www.microbetcm.com
- 文献：*MicrobeTCM: A comprehensive platform for the interactions of microbiota and traditional Chinese medicine.* Pharmacological Research 2024. https://pubmed.ncbi.nlm.nih.gov/38272335/
- 分发格式：**Web 平台，交互式检索 + 可视化**；无批量下载接口

## 为什么它是这批里最关键的一个

其它 8 个库要么只管「中药侧」，要么只管「微生物侧」。**MicrobeTCM 是唯一原生建立
「草药/复方 → 微生物 → 疾病」这条链的库**——也就是你要的完整链条中最难自己拼出来的那一段。

数据来自 **419 篇体内实验文献的双人独立提取**（double-entry extraction），
外加 6 个权威数据库的整合，因此证据级别较高但覆盖面相对窄。

## 规模

| 实体 | 数量 |
|---|---|
| 疾病 | 171 |
| 微生物 | 725 |
| 复方（herb-formula） | 1,468 |
| 草药 | 1,032 |
| 化学成分 | 15,780 |
| 穴位组方（acupoint-formula） | 35 |
| 穴位 | 77 |

> 注意它还收了**针灸**（穴位/穴位组方 → 微生物），这在其它库里完全没有。

## 字段说明

平台按实体检索，返回关联表。核心关联与字段：

### 草药/复方 → 微生物

`Herb / Formula`、`Microbe`（属或种）、`Variation`（增加/减少）、`Disease Model`、
`Sample Site`、`Host`（大鼠/小鼠等）、`Dose & Duration`、`Reference (PMID)`。

### 微生物 → 疾病

`Microbe`、`Disease`、`Variation`、`Evidence Type`、`Reference`。

### 预测得分表

除人工提取的证据外，平台提供**预测模块**，输入中药或疾病后返回打分表，字段通常含：
`Disease`、`Microbe`、`Target`（基因/蛋白）、`Score`（预测得分）、`Rank`。
这部分是算法推断结果，**与人工证据要分开对待**，不要混进同一张证据表。

## 示例片段

见 [`samples/microbetcm_herb_microbe.example.tsv`](../samples/microbetcm_herb_microbe.example.tsv)
与 [`samples/microbetcm_prediction.example.tsv`](../samples/microbetcm_prediction.example.tsv)。

## 使用提示

- **没有下载接口是主要障碍**。可行路径：（1）按 1,032 个草药 + 1,468 个复方逐个请求详情页抓取；
  （2）直接向通讯作者索取结构化数据——对这种人工提取的中等规模库，通常比爬取更省事，也更规范。
- 419 篇文献的体量意味着关系条数是「千」级而非「万」级，**覆盖稀疏**。
  建议把它当作**高置信度的种子集 / 验证集**，而不是唯一的骨架；
  用 Disbiome + MDIPID 扩展微生物-疾病侧，用 dbPTH/HERB 扩展成分-靶点侧。
- 它的成分表（15,780）与 SymMap/HERB 的成分表可通过 PubChem CID 或 InChIKey 对齐，
  这是把 MicrobeTCM 的链条接到分子层的最实用切入点。
