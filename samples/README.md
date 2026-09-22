# samples/ — 结构示例片段

## ⚠️ 这些不是真实下载的数据

本会话的出口网络策略拦截了全部 9 个数据库的域名（详见 [`../DOWNLOAD_STATUS.md`](../DOWNLOAD_STATUS.md)），
**没有下载到任何一个数据集**。

因此本目录下的 `*.example.tsv` / `*.example.json` 是**依据各库官方文档、下载页说明与原始论文
还原出来的「列结构示例」**，用于展示：

- 每张表有哪些列、列名怎么写
- 每一列的取值形态（ID 格式、枚举值、单位、分隔符）
- 表与表之间靠哪个字段连接

**取值本身是占位内容，不可用于任何分析、统计或引用。**
少数几行取自各库论文中公开举例的真实记录（如 Disbiome 的
"Faecalibacterium 在 Stevens-Johnson 综合征中减少"、MDIPID 的
"Finasteride → Ruminococcaceae UCG-002 减少, Stool"），这些行在文件中标注了 `# from paper`。

拿到真实数据后，用同名文件直接替换即可——列结构是按官方文档写的。

## 文件清单

| 文件 | 对应表 |
|---|---|
| `symmap_SMHB.example.tsv` | SymMap 草药 |
| `symmap_SMIT.example.tsv` | SymMap 成分 |
| `symmap_SMTT.example.tsv` | SymMap 靶点 |
| `symmap_SMDE.example.tsv` | SymMap 疾病 |
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
