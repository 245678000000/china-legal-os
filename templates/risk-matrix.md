# Risk Matrix — 法律与合规风险矩阵

```
Review Basis: {company_context_loaded ? "已加载公司法务上下文" : "通用商业标准（未加载公司法务上下文）"} ｜ RETRIEVAL_MODE: {retrieval_mode}（法律依据未经核验）
评估主体/事项: {subject} ｜ 我方立场: {our_side} ｜ Lane: {lane} ｜ 评估日期: 2026-08-19
```

---

## 1. 评估范围说明（Scope Statement）

### (1) 已覆盖核查范围（Scope Covered）
- [x] {scope_covered[0]}
- [x] {scope_covered[1]}

### (2) 未覆盖与除外范围（Scope Not Covered）
> **【底线纪律】以下事项因材料缺失或超出本次范围未作核查，不代表无风险：**
- [ ] {scope_not_covered[0]}
- [ ] {scope_not_covered[1]}

---

## 2. 风险全景排序表（Prioritized Risk Matrix）

| 序号 | 风险事项与分类 | 风险等级 | 确定性 | 发生概率 | 财务/法律影响预估 | 控制措施与整改方案 | 责任人 | 完成时限 |
|---|---|---|---|---|---|---|---|---|
| R-01 | **【{items[0].category}】** {items[0].title}<br>*(依据：{items[0].legal_basis})* | **`{items[0].risk_level}`** *(BLACK/Critical/High/Medium/Low)* | `{items[0].certainty}` | `{items[0].probability}` | **财务敞口**：{items[0].financial_impact}<br>**最坏情形**：{items[0].worst_case} | {items[0].controls} | `{items[0].owner}` | `{items[0].deadline}` |

---

## 3. 风险条目深度剖析（Itemized Risk Deep-Dive）

### 风险点 R-01：{items[0].title}
- **事实与行为描述**：{items[0].description}
- **法律定性与处罚依据**：{items[0].legal_analysis}
- **三项修饰符**：
  - 法律确定性：`{items[0].modifiers.legal_certainty}`
  - 证据充分度：`{items[0].modifiers.evidence_strength}`
  - 可逆性：`{items[0].modifiers.reversibility}`
- **具体落地整改动作**：
  1. {items[0].action_steps[0]}
  2. {items[0].action_steps[1]}

---

## 4. 待核验清单（Verification Worklist）

| # | 待核验项 | 类型 | 建议核验入口 | 核验不通过的影响 |
|---|---|---|---|---|
| 1 | {verification_worklist[0].item} | {type} | `{source}` | {impact_if_invalid} |

---
*声明：本文由 AI 法务系统生成，依据未经检索核验，仅供内部工作参考，不构成法律意见。*
