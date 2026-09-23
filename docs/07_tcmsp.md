# TCMSP 2.3 — 中药网络药理学的 ADME 基础库

> ✅ **已实际下载**（Actions，2026-09-23）：四张主表，**5.35 MB**。
> 数据在 [`datasets` 分支的 `tcmsp/`](../../../tree/datasets/tcmsp)（同时提供 `.json` 与 `.tsv`），
> 真实截取见 `samples/tcmsp_*.real.tsv`。**本页字段与数字均来自下载到的真实数据。**

- 官网：https://www.tcmsp-e.com/
- 文献：Ru J, et al. *TCMSP: a database of systems pharmacology for drug discovery from
  herbal medicines.* Journal of Cheminformatics 2014;6:13.
  https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-6-13

## 🎯 取数方法：browse.php 内联全表，**不需要爬虫**

TCMSP 确实没有下载按钮，本仓库前几轮也一直判定它「需要逐草药爬取」。**这个判断是错的。**

实测：`browse.php` 把整张表直接内联在 Kendo Grid 的 `dataSource.data` 里，
**四次请求就能拿到四张主表**：

| URL | 内容 | 实测行数 |
|---|---|---:|
| `browse.php?qc=herbs` | 草药 | **502** |
| `browse.php?qc=ingredients` | 成分（含全部 ADME 参数） | **13,729** |
| `browse.php?qc=targets` | 靶点 | **3,339** |
| `browse.php?qc=diseases` | 疾病 | **867** |

```bash
python3 scripts/gh_fetch.py --out data --datasets tcmsp
```

## 真实字段

### ingredients（15 列）—— TCMSP 不可替代的部分

```
MOL_ID  molecule_ID  molecule_name  mw  hdon  hacc  alogp  halflife
ob  caco2  bbb  dl  FASA  tpsa  rbn
```

| 字段 | 含义 | 领域惯用阈值 |
|---|---|---|
| `ob` | 口服生物利用度（%） | **≥ 30** |
| `dl` | 类药性 | **≥ 0.18** |
| `caco2` | Caco-2 透膜性 | > -0.4 视为可吸收 |
| `bbb` | 血脑屏障 | > -0.3 视为可透过 |
| `halflife` | 半衰期 | — |
| `mw` / `alogp` / `hdon` / `hacc` | 分子量 / 脂水分配系数 / 氢键供体 / 受体 | Lipinski 五规则 |
| `tpsa` / `rbn` / `FASA` | 拓扑极性表面积 / 可旋转键数 / 相对溶剂可及表面积 | — |

真实数据（抽查知名成分，与 TCMSP 公布值一致）：

| MOL_ID | molecule_name | ob | dl | mw | caco2 | bbb | halflife |
|---|---|---|---|---|---|---|---|
| MOL000098 | quercetin | 46.4333 | 0.27525 | 302.250 | 0.04842 | -0.76890 | 14.4005 |
| MOL000422 | kaempferol | 41.8822 | 0.24066 | 286.250 | 0.26096 | -0.55335 | 14.7434 |
| MOL001454 | berberine | 36.8612 | 0.77665 | 336.390 | 1.24179 | 0.56718 | 6.5659 |
| MOL000358 | beta-sitosterol | 36.9139 | 0.75123 | 414.790 | 1.32463 | 0.98588 | 5.3555 |

### ⚠️ 两个实测坑

**1. 所有数值字段都是字符串。** JSON 里 `"ob":"46.4333481195"` 而非数字，
直接做大小比较会得到错误结果（字符串比较下 `"9" > "30"`）。**必须先转数值**：

```python
df[["ob","dl","mw","caco2","bbb"]] = df[["ob","dl","mw","caco2","bbb"]].apply(
    pd.to_numeric, errors="coerce")
active = df[(df.ob >= 30) & (df.dl >= 0.18)]      # 实测得 2,583 个活性成分（18.8%）
```

全部 13,729 个成分的 `ob` / `dl` 都能成功转为数值（无缺失）；
但 `halflife` 有空值，转换时要容错。

**2. 应用领域惯例阈值后只剩 2,583 个成分（18.8%）。**
这是 TCMSP 网络药理学流程的实际起点规模，建库时心里有数。

### herbs（5 列）

```
herb_cn_name  herb_pinyin  herb_en_name  child_cn_name  child_en_name
```
`child_*` 是功效分类（如 止咳平喘药 / Antitussive Antiasthmetics）。

实际数据：`矮地茶 | Aidicha | Ardisiae Japonicae Herba | 止咳平喘药 | Antitussive Antiasthmetics`

### targets（5 列）

```
target_ID  TAR_ID  drugbank_ID  target_name  kegg
```
自带 **DrugBank** 与 **KEGG** 交叉引用。

### diseases（5 列）

```
disease_ID  DIS_ID  disease_name  ICD9  ICD10
```
**自带 ICD9 / ICD10 编码**（此前本仓库未记录这一点）。实际数据：
`1 | DIS00001 | Abdominal aortic aneurysm | 442 | 172`。部分疾病编码为空。

## ⚠️ 本次下载拿不到的部分

四张主表是**实体表**，不含「成分↔靶点」「靶点↔疾病」的**配对关系**。
关系数据在 `tcmspsearch.php?qr=<名称>&qsr=herb_en_name&token=<token>` 的逐草药结果页里，
要拿需按 502 味草药逐个请求（页面里带 token，抓取时需一并带上）。
本次未做此步，故**关系表尚未获取**。

## 使用提示

- 跨库对齐：`MOL_ID` 是 TCMSP 内部编号，SymMap 的 `SMIT` 表带 `TCMSP_id`、
  SymMap 的 `SMTT` 表带 `TCMSP_id`，可直接当映射表用，省去按名称对齐。
- `targets` 的 `drugbank_ID` / `kegg` 可直连 DrugBank 与 KEGG。
- 该库靶点部分含预测结果（SysDT 等模型），做机制论证时应与 dbPTH / HIT 2.0 的实验证据交叉验证。
