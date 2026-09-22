# Disbiome — 微生物-疾病

> ✅ **已实际下载**（Actions run #3）：**10,866 条实验记录，11.75 MB**。
> 数据在 [`datasets` 分支的 `disbiome/experiments.json`](../../../tree/datasets/disbiome)，
> 真实截取见 `samples/disbiome_experiments.real.tsv` 与 `samples/disbiome_biothings.real.json`。
> **本页字段取自下载到的真实数据。**

- 官网：https://disbiome.ugent.be/
- 文献：Janssens Y, et al. *Disbiome database: linking the microbiome to disease.*
  BMC Microbiology 2018;18:50.
  https://bmcmicrobiol.biomedcentral.com/articles/10.1186/s12866-018-1197-5

## 🚨 怎么拿数据：走 BioThings 镜像，不要走官网 API

**实测（run #2、#3）：`disbiome.ugent.be/api/disbiome/experiments`、`/api/experiments`、
`/api/organisms`、`/api/diseases`、`/api/methods` 全部返回 HTTP 200 + Angular 首页 HTML，
不是数据。** 该站是单页应用，任何未知路由都被前端兜底成首页——**只看状态码会误判为下载成功**
（本仓库第一版脚本就踩了这个坑，把 5 份 HTML 当数据提交了）。

**唯一可用的全量入口是 BioThings 镜像：**

```
https://pending.biothings.io/disbiome/query?q=__all__&fetch_all=true
```

单次查询上限 1000 条，**必须用 `fetch_all=true` 拿 `_scroll_id` 再翻页**，
否则只拿到第一页还会以为是全量。本仓库 `scripts/gh_fetch.py` 的 `fetch_biothings()`
已实现该分页，实测取满 10,866 条。

## 真实数据结构（BioLink 嵌套格式）

⚠️ BioThings 返回的是 **BioLink 风格的嵌套 JSON**，与官网网页 CSV 导出的扁平结构不同。
一条记录 = 一次实验观察：

```json
{
 "_id": "009b898ba8464889b03de9bcc2352f0d",
 "subject": {                                  // 微生物
   "id": "taxid:265975", "taxid": 265975,
   "name": "oribacterium", "scientific_name": "oribacterium",
   "rank": "genus", "parent_taxid": 186803,
   "lineage": [265975, 186803, 3085636, 186801, 1239, 1783272, 2, 131567, 1],
   "type": "biolink:Bacterium"
 },
 "object": {                                   // 疾病
   "id": "MedDRA:10052358", "meddra": 10052358,
   "meddra_level": "preferred_term",
   "name": "invasive colorectal cancer",
   "type": "biolink:Disease"
 },
 "association": {                              // 观察到的关系
   "qualifier": "decreased",
   "sources": "feces",
   "method_name": "16S rRNA sequencing",
   "host_type": "human",
   "control_name": "early colorectal cancer patient",
   "predicate": "OrganismalEntityAsAModelOfDiseaseAssociation"
 },
 "publications": {
   "pmid": "31609493", "doi": "10.1111/jgh.14868",
   "publication_id": 1162, "title": "…"
 }
}
```

**注意**：`subject.lineage` 给出了完整的 NCBI 分类谱系数组——
**要把种级记录上卷到属级或门级，直接用它，不必另外查分类库**。这是很实用的一个字段。

## 实测取值分布（全部 10,866 条）

**`association.qualifier`（变化方向）——只有两个值：**

| 值 | 条数 |
|---|---:|
| `increased` | 5,713 |
| `decreased` | 5,153 |

**`association.sources`（采样部位）top 8：**

| 部位 | 条数 |
|---|---:|
| feces | 5,500 |
| tissue biopsie | 942 |
| saliva | 766 |
| subgingival plaque | 544 |
| skin swab | 314 |
| urine | 265 |
| vaginal swab | 229 |
| bronchoalveolar lavage | 173 |

> 粪便样本占一半以上，**但另外近一半来自口腔、皮肤、泌尿生殖道等部位**。
> 做肠道菌群研究时务必先按 `sources` 过滤，否则会把口腔菌群的结论混进来。
> 注意 `tissue biopsie` 是数据库里的原始拼写（少个 s），别写成 `biopsies`。

**`association.method_name`（检测方法）top 6：**

| 方法 | 条数 |
|---|---:|
| 16S rRNA sequencing | 6,631 |
| MiSeq sequencing | 696 |
| Metagenomic sequencing | 626 |
| 16S rDNA pyrosequencing | 541 |
| 16S rRNA pyrosequencing | 435 |
| qPCR | 406 |

> 方法名**没有做归一化**：`16S rRNA sequencing` / `16S rDNA pyrosequencing` /
> `16S rRNA pyrosequencing` / `MiSeq sequencing` 实际都是 16S 扩增子测序。
> 按方法分层分析前要先自行合并同类项。

## 标准化（Disbiome 的核心优势）

- **疾病** → MedDRA（`object.meddra` + `object.meddra_level`）
- **微生物** → NCBI Taxonomy（`subject.taxid` + `subject.lineage`）
- **文献** → PMID + DOI

**SymMap 的 `SMDE` 表自带 `MedDRA_id` 和 `UMLS_id`**（已由实际下载的文件确认），
所以 **Disbiome ↔ SymMap 可以直接在 MedDRA 上 join，不需要额外做映射**。
HERB 用 MeSH/OMIM/DisGeNET，与 Disbiome 对接才需要经 UMLS 绕一次。

## 一键拉全量

```bash
python3 scripts/gh_fetch.py --out data --datasets disbiome
```

## 使用提示

- `qualifier` 只有升高/降低两极，**没有效应量**；需要定量得回溯原文（`publications.pmid`）。
- 同一「菌-病」对常有多条来自不同研究的记录，方向可能冲突。建图前建议按
  `(subject.taxid, object.meddra)` 聚合并统计方向一致性，把冲突比例作为边的置信度。
- 菌名字段是**全小写**（`oribacterium`、`bacteroides caccae`），与其它库按名称 join 前要统一大小写；
  更稳妥的做法是直接用 `taxid`。
- `publications.pmid` 可能为空（实测有记录只有 DOI 没有 PMID），去重时别只用 PMID 做键。
