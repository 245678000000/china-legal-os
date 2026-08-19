# Evidence Matrix — 证据矩阵与举证分析表

```
Review Basis: {company_context_loaded ? "已加载公司法务上下文" : "通用商业标准（未加载公司法务上下文）"} ｜ RETRIEVAL_MODE: {retrieval_mode}（法律依据未经核验）
案件/事项名称: {matter} ｜ 我方立场: {our_side} ｜ Lane: {lane} ｜ 评估日期: 2026-08-19
全案证据封顶强度: `{overall_evidence_ceiling}` (充分 / 较强 / 薄弱 / 无)
```

---

## 1. 证据效力总评与结论封顶（Overall Evidence Ceiling）

> **【四元 min 规则约束】**：本案综合证据充分度评定为 **`{overall_evidence_ceiling}`**。
> 任何依赖事实证明的法律主张，其最终确定性均受此封顶限制。

---

## 2. 争点要件与证据逐项映射表（Evidence Mapping Matrix）

| 争点与法定要件（Element） | 待证事实（Fact to Prove） | 举证责任（Burden of Proof） | 现有在案证据（Existing Evidence） | 证据强度（Strength） | 缺失证据（Missing Evidence） | 补强取证路径（How to Obtain） | 证据三性与采信风险（Admissibility Risks） |
|---|---|---|---|---|---|---|---|
| **【争点 1】**<br>要件 E1：{rows[0].element_name} | {rows[0].fact_to_prove} | `{rows[0].burden_of_proof}` *(我方/对方/待定)* | - {rows[0].existing_evidence[0]}<br>- {rows[0].existing_evidence[1]} | **`{rows[0].evidence_strength}`** *(充分/较强/薄弱/无)* | {rows[0].missing_evidence} | {rows[0].how_to_obtain} | {rows[0].admissibility_risks} |

---

## 3. 紧急时限敏感取证动作（Time-Sensitive Actions）

> **【证据保全倒计时】以下证据面临灭失或被篡改风险，必须在指定时限内完成固定：**

| 优先级 | 紧急程度 | 目标证据材料 | 取证动作与保全方式 | 责任岗位 | 截止时限 |
|---|---|---|---|---|---|
| 🚨 P0 | **当日紧急（24h内）** | {time_sensitive_actions[0].target} | {time_sensitive_actions[0].action} | `{time_sensitive_actions[0].owner}` | `{time_sensitive_actions[0].deadline}` |
| ⚠️ P1 | **3日内必办** | {time_sensitive_actions[1].target} | {time_sensitive_actions[1].action} | `{time_sensitive_actions[1].owner}` | `{time_sensitive_actions[1].deadline}` |

---

## 4. 证据补强与举证指引（Evidence Action Plan）
1. **书证原件核验**：确保关键合同、通知回执、付款凭证持有原件原件。
2. **电子数据存证**：对微信聊天记录、企业邮箱、服务器日志进行公证处可信存证或司法区块链存证。
3. **证人证言与谈话录音**：在法律允许范围内固定关键知情人口述录音。

---

## 5. 待核验清单（Verification Worklist）

| # | 待核验项 | 类型 | 建议核验入口 | 核验不通过的影响 |
|---|---|---|---|---|
| 1 | {verification_worklist[0].item} | {type} | `{source}` | {impact_if_invalid} |

---
*声明：本文由 AI 法务系统生成，依据未经检索核验，仅供内部诉讼/维权准备参考，不构成法律意见。*
