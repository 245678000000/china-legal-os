# Contract Review — 合同审查报告与红线批注

```
Review Basis: {company_context_loaded ? "已加载公司法务上下文及 Playbook" : "通用商业标准（未加载公司法务上下文）"} ｜ RETRIEVAL_MODE: {retrieval_mode}（法律依据未经核验）
我方立场: {our_side} ｜ 相对方: {counterparty | "未指定"} ｜ 合同类型: {deal_identification.contract_type} ｜ Lane: {lane}
标的金额: {deal_identification.deal_value | "未指定"} ｜ 审查日期: 2026-08-19
```

---

## 1. 交易识别与基本概况（Deal Identification）

- **合同名称**：{deal_identification.contract_title}
- **签约主体**：我方（{deal_identification.our_role}） vs 对方（{deal_identification.counterparty_name}）
- **交易目的与商业模式**：{deal_identification.commercial_objective}
- **准据法与管辖条款状态**：
  - 准据法约定：`{governing_law_found ? governing_law_found : "未约定（缺失）"}`
  - 争议解决约定：`{dispute_resolution_found ? dispute_resolution_found : "未约定（缺失）"}`

---

## 2. 跨条款强制数值推演（Numeric Checks）

| 推演维度 | 计算公式 / 逻辑推演 | 计算结果 | 风险定性与实操影响 |
|---|---|---|---|
| **违约金上限可达性** | 日费率 `{numeric_checks.rate}` × 触顶天数 | 需连续违约 **`{numeric_checks.days_to_cap}`** 天触顶 | {numeric_checks.cap_assessment} |
| **履约时序闭合性** | 交付期 → 异议期 → 账期 → 开票时序 | 时序差：`{numeric_checks.timing_gap}` | {numeric_checks.timing_assessment} |
| **责任限制穿透推演** | 责任上限金额 vs 除外情形涵盖范围 | 除外情形：`{numeric_checks.carve_outs}` | {numeric_checks.lol_permeability} |

---

## 3. 跨条款联动影响图（Cross-Clause Interactions）
- **违约赔偿 ↔ 责任上限 ↔ 终止权**：{cross_clause_interactions.summary}
- **核心 IP 权属 ↔ 商业秘密 ↔ 竞业义务**：{cross_clause_interactions.ip_and_confidentiality}

---

## 4. 逐条审查与红线批注表（Findings Matrix）

| # | 条款定位（Clause） | 风险等级（Risk） | 判定依据（Basis） | 确定性（Confidence） | 风险实质剖析（Why） | 建议修改文本（Suggested Revision） | 退让底线（Fallback） | 审批触发（Escalation） |
|---|---|---|---|---|---|---|---|---|
| 1 | 第 X 条【{findings[0].clause_title}】<br>*(原文字：{findings[0].original_snippet})* | **`{findings[0].risk_level}`** *(BLACK/RED/YELLOW/GREEN)* | `{findings[0].basis}` | `{findings[0].confidence}` | {findings[0].why} | `{findings[0].suggested_revision}` | `{findings[0].fallback}` | `{findings[0].escalation}` |

---

## 5. 缺漏必要条款（Missing Clauses）
> 以下属于该合同类型必备但在文本中缺失的关键保护条款：
- [ ] **{missing_clauses[0].title}**：{missing_clauses[0].rationale}（建议补入条款：`{missing_clauses[0].suggested_text}`）
- [ ] **{missing_clauses[1].title}**：{missing_clauses[1].rationale}

---

## 6. 对外谈判策略与沟通版本（Negotiation Strategy）

### (1) 整体谈判抓手与退让阶梯
- **核心必争红线（Must-Have）**：{negotiation_strategy.must_have}
- **可适度妥协点（Nice-to-Have）**：{negotiation_strategy.nice_to_have}
- **一揽子对冲交换策略**：{negotiation_strategy.trade_offs}

### (2) 供业务直接发送的对外回复话术
```markdown
尊敬的【对方公司名称】团队：
关于贵方发来的《{deal_identification.contract_title}》，我方法务团队已审阅完毕。为保障双方长期健康合作，我方就以下核心条款提出修订建议：
1. 关于第 X 条【条款名称】：我方建议修改为“……”，主要考虑……
2. 关于第 Y 条【条款名称】：……
详见附件《合同修订对照版》。期待贵方确认！
```

---

## 7. 待核验清单（Verification Worklist）

| # | 待核验项 | 类型 | 建议核验入口 | 核验不通过的影响 |
|---|---|---|---|---|
| 1 | {verification_worklist[0].item} | {type} | `{source}` | {impact_if_invalid} |

---
*声明：本文由 AI 法务系统生成，依据未经检索核验，仅供内部工作参考，不构成法律意见。*
