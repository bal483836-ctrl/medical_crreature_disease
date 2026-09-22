# Disbiome — 微生物-疾病

- 官网：https://disbiome.ugent.be/
- 导出：https://disbiome.ugent.be/export
- API：https://disbiome.ugent.be/api
- 文献：Janssens Y, et al. *Disbiome database: linking the microbiome to disease.* BMC Microbiology 2018;18:50. https://bmcmicrobiol.biomedcentral.com/articles/10.1186/s12866-018-1197-5
- 分发格式：**CSV（网页导出）或 JSON（REST API）**
- 技术栈：PostgreSQL + LimeDS（根特大学）

> **这是本批 9 个库里唯一能「一条命令拉全量」的。** 做管线时应当第一个接入。

## 标准化（Disbiome 的核心优势）

- **疾病** → MedDRA 分类体系
- **微生物** → NCBI Taxonomy + SILVA 分类
- **检测方法** → 标准化方法名（16S rRNA sequencing、qPCR、shotgun metagenomics …）

这意味着 Disbiome 的记录可以直接和其它挂了 NCBI taxid / MeSH 的库做 join，而不用先清洗菌名。

## API 端点

| 端点 | 返回 |
|---|---|
| `GET /api/disbiome/experiments` | 全部实验记录（主表） |
| `GET /api/disbiome/organisms` | 微生物词表 + NCBI/SILVA ID |
| `GET /api/disbiome/diseases` | 疾病词表 + MedDRA ID |
| `GET /api/disbiome/publications` | 文献 |
| `GET /api/disbiome/methods` | 检测方法词表 |

返回 JSON 数组，无需鉴权。

## 字段说明（experiments 主表）

| 字段 | 含义 | 取值示例 |
|---|---|---|
| `disease_name` | 疾病名（MedDRA 标准化） | Stevens-Johnson syndrome |
| `meddra_id` / `meddra_level` | MedDRA ID 与层级 | |
| `organism_name` | 微生物名 | Faecalibacterium |
| `ncbi_id` | NCBI Taxonomy ID | 216851 |
| `silva_id` | SILVA 分类 ID | |
| `qualitative_outcome` | 变化方向 | **Reduced / Elevated** |
| `quantitative_outcome` | 定量结果（部分记录有） | |
| `sample_name` | 样本/身体部位 | Faeces、Saliva、Skin |
| `method_name` | 检测方法 | 16S rRNA sequencing |
| `host_type` | 宿主 | Human / Mouse |
| `control_name` | 对照组描述 | Healthy controls |
| `publication_title` / `pubmed_url` | 文献标题与链接 | |

> 论文中的典型记录：**Faecalibacterium 在 Stevens-Johnson 综合征中减少**。

## 示例片段

见 [`samples/disbiome_experiments.example.json`](../samples/disbiome_experiments.example.json)
与 [`samples/disbiome_experiments.example.csv`](../samples/disbiome_experiments.example.csv)。

## 一键拉全量

```bash
python3 scripts/fetch_disbiome.py --out data/disbiome
# 产出 experiments.json / organisms.json / diseases.json / publications.json
#      + 对应的扁平化 .csv
```

## 使用提示

- `qualitative_outcome` 只有「升高/降低」两极，没有效应量；需要定量的话要回溯原文。
- 同一「菌-病」对常有多条来自不同研究的记录，方向可能冲突。建图前建议按
  `(organism, disease)` 聚合并统计方向一致性，把冲突比例作为边权重或置信度。
- 疾病用 MedDRA 编码。**SymMap 的 SMDE 表自带 `MedDRA_id` 和 `UMLS_id`**（已由实际下载的文件确认），所以 Disbiome ↔ SymMap 可以直接 join，不需要额外做映射。
  HERB 用 MeSH/OMIM/DisGeNET，与 Disbiome 对接时才需要经 UMLS 绕一次。
