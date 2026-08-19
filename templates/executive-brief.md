# Executive Brief — 管理层决策简报

```
Review Basis: {company_context_loaded ? "已加载公司法务上下文" : "通用商业标准（未加载公司法务上下文）"} ｜ RETRIEVAL_MODE: {retrieval_mode}（法律依据未经核验）
我方立场: {our_side} ｜ 相对方: {counterparty | "未指定"} ｜ 相关时点: {relevant_time | "当前"} ｜ Lane: {lane} ｜ 适用法域: {jurisdiction | "CN-mainland"}
降级说明: {degradations | "无"}
```

---

## 1. 决策事项（The Decision）
> **{the_decision}**
> *（一句话说明本次需要管理层裁决的核心事项与商业背景）*

---

## 2. 结论与推荐方案（Recommendation & Bottom Line）

### 推荐方案（Recommendation）
**{recommendation}**

### 一分钟要点（Bottom Line）
> **{bottom_line}**
> *（提炼给最高决策层的核心结论：能不能做、核心代价与底线抓手）*

---

## 3. 风险全景评估（Risk Profile）

| 风险等级 | 法律确定性 | 证据充分度 | 可逆性 | 核心风险敞口简述 |
|---|---|---|---|---|
| **`{risk.level}`** *(BLACK/Critical/High/Medium/Low)* | `{risk.modifiers.legal_certainty}` | `{risk.modifiers.evidence_strength}` | `{risk.modifiers.reversibility}` | {risk.summary} |

- **主要不利后果预估**：{risk.worst_case_scenario}
- **最大财务敞口**：{risk.financial_exposure | "待量化"}

---

## 4. 走向推演（Scenario Analysis）

### 方案 A：推进实施（If We Proceed）
- **商业收益**：{if_we_proceed.benefits}
- **法律合规代价与控制措施**：{if_we_proceed.risks_and_controls}

### 方案 B：放弃/搁置（If We Don't）
- **商业机会损失**：{if_we_dont.commercial_loss}
- **替代解决方案**：{if_we_dont.alternative_paths}

---

## 5. 商业落地七问（Business Decision）

1. **能不能做？**：`{business_decision.can_we_do_it}` *(可以 / 有条件可以 / 不建议 / 不能)*
2. **怎么做风险最低？**：{business_decision.lowest_risk_path}
3. **如果业务坚持必须做，最不坏的路径是什么？**：{business_decision.least_bad_if_business_insists}
4. **Fallback 是什么？**：{business_decision.fallback}
5. **什么条件触发升级？**：{business_decision.escalation_trigger}
6. **谁需要审批？**：{business_decision.approver}
7. **今天应该做什么？**：
   - **动作**：{business_decision.today_action.action}
   - **责任人**：{business_decision.today_action.owner}
   - **时限**：{business_decision.today_action.deadline}
   - **所需材料**：{business_decision.today_action.required_materials}

---

## 6. 结论推翻假设（What Would Change This）
> 以下未知事项一旦核实或发生改变，本简报结论需同步调整：
- [ ] {what_would_change_this[0]}
- [ ] {what_would_change_this[1]}

---

## 7. 待核验清单（Verification Worklist）
*（RETRIEVAL_MODE=none 下强制列出）*

| # | 待核验项 | 类型 | 建议核验入口 | 核验不通过的影响 |
|---|---|---|---|---|
| 1 | {verification_worklist[0].item} | {type} | `{source}` | {impact_if_invalid} |

---

## 8. 支撑文档清单（Supporting Documents）
- 支撑文件 1：`{supporting_documents[0]}`
- 支撑文件 2：`{supporting_documents[1]}`

---
*声明：本简报由 AI 法务系统协助生成，依据未经检索源核验，供企业内部决策参考，重大事项请经法务负责人或外部律师复核。*
