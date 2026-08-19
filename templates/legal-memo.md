# Legal Research Memo — 法务备忘录

```
Review Basis: {company_context_loaded ? "已加载公司法务上下文" : "通用商业标准（未加载公司法务上下文）"} ｜ RETRIEVAL_MODE: {retrieval_mode}（法律依据未经核验）
我方立场: {our_side} ｜ 相对方: {counterparty | "未指定"} ｜ 相关时点: {relevant_time | "当前"} ｜ Lane: {lane} ｜ 适用法域: {jurisdiction | "CN-mainland"}
降级说明: {degradations | "无"}
```

---

## 1. 核心问题（Question Presented）
> **{question}**

---

## 2. 简短结论（Short Answer）
> **{short_answer}**

- **结论确定性等级**：`{certainty}` *(Confirmed / Probable / Conditional / Unverified / Unknown)*
- **封顶项说明（Certainty Driver）**：`{certainty_driver}`
  *(四元 min 规则计算结果：min(法律确定性: {c_law}, 证据充分度: {c_evidence}, 事实确认度: {c_fact}, 法源核验度: {c_authority})，由【{c_bottleneck}】封顶)*

---

## 3. 法律依据清单（Authorities）

| 法源层级 | 法源名称 | 规则内容摘要 | 关联条号 | 核验状态 | 时效/特别标记 |
|---|---|---|---|---|---|
| `{authorities[0].level}` *(L1-L4)* | {authorities[0].name} | {authorities[0].rule_content} | `{authorities[0].article_ref}`〔条号未核验〕 | `{authorities[0].verification}` | {authorities[0].currency_flag} |

---

## 4. 检索指引（Search Guidance）
*（无检索源模式下针对核心案例与分歧观点的核验指引）*

```
【建议检索】争点：{search_guidance.issue}
  目标平台：{search_guidance.target_platform}
  推荐检索词：{search_guidance.search_terms}
  核验目的：{search_guidance.objective}
  核验结果影响：{search_guidance.impact}
```

---

## 5. 深度法理分析（Detailed Analysis）

### (1) 争点拆解与法定要件（Issue & Elements）
- **争点**：{analysis.issue}
- **法定构成要件**：
  - 要件 E1：{analysis.elements[0].name}（举证责任：{analysis.elements[0].burden_of_proof}）
  - 要件 E2：{analysis.elements[1].name}（举证责任：{analysis.elements[1].burden_of_proof}）

### (2) 事实涵摄（Facts Subsumption）
- {analysis.subsumption_text}
  *(将已确认的 Confirmed 事实逐一涵摄至法定要件，对 Alleged/Missing 事实进行条件式推导)*

### (3) 观点分歧分析（Divergence Analysis）
- **主流实践观点**：{divergence.majority_view} `[模型知识-未核验]`
- **少数/地方口径**：{divergence.minority_view} `[模型知识-未核验]`

---

## 6. 红队对抗与反驳检验（Counterarguments & Red Team）
- **对方可能主张的最强抗辩**：{counterarguments.strongest_argument}
- **我方不利事实与证据弱点**：{counterarguments.our_weaknesses}
- **结论是否需要因此下调**：`{counterarguments.conclusion_adjusted ? "是，已下调" : "否，维持原判断"}`

---

## 7. 升级建议与下一步（Escalation & Next Steps）
- **升级判定**：`{escalation.needed ? "需升级" : "无需升级"}`
- **升级对象**：{escalation.to_role}
- **触发条件**：{escalation.trigger_condition}
- **准备材料**：{escalation.required_materials}
- **时限要求**：{escalation.deadline}

---

## 8. 待核验清单（Verification Worklist）

| # | 待核验项 | 类型 | 建议核验入口 | 核验不通过的影响 |
|---|---|---|---|---|
| 1 | {verification_worklist[0].item} | {type} | `{source}` | {impact_if_invalid} |

---
*声明：本文由 AI 法务系统生成，依据未经检索核验，仅供内部研究参考，不构成法律意见。*
