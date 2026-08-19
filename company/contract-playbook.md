# Contract Playbook

我方的标准立场。`contract-review` 会逐条对照它判断偏离，`contract-drafting` 会用它生成初稿。

**没有 Playbook 时**，OS 用通用商业标准审查，并在抬头标注 `Review Basis: 通用商业标准`。这仍然可用，但它回答的是"这个条款有没有风险"，而不是"相对于我们公司的标准，这偏离了多少、谁有权批准这个偏离"——后者才是企业法务的工作。

---

## 填写规则

三段式，每条条款都要填满：

| 字段 | 要求 |
|---|---|
| **Preferred Position** | **可直接插入合同的中文条款文本**，不是概念描述。对方律师收到的是条款，不是"我们希望责任对等" |
| **Acceptable Fallback** | 可以接受的退让，不需要升级审批 |
| **Escalation Trigger** | **可判定的条件**。"金额超过 500 万"可判定；"金额较大"不可判定 |
| **审批人** | 岗位（对应 `company-legal-context.md` 的升级链） |
| **性质** | `法律强制` / `商业选择` —— 前者不可谈判，后者可以换 |

---

## 模板

复制下面这块，按合同类型分别填写。

### [合同类型：例如「采购合同 — 我方为采购方」]

#### 责任限制 Limitation of Liability
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 赔偿 Indemnification
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 知识产权归属与许可
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 保密
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 数据与个人信息
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 期限与终止
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 付款
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 违约责任
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 陈述与保证
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 不可抗力
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 转让与控制权变更
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 争议解决与管辖
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

#### 保险
- Preferred Position：
- Acceptable Fallback：
- Escalation Trigger：
- 审批人：
- 性质：

---

## 谈判优先级

| 层级 | 含义 | 条款 |
|---|---|---|
| **Tier 1 Must-have** | 不解决不能签 |  |
| **Tier 2 Should-have** | 实质影响风险，有谈判空间 |  |
| **Tier 3 Concession** | 可以用来交换的让步筹码 |  |

策略：Tier 1 先提；用 Tier 3 换 Tier 2；Tier 1 不让步，除非升级批准。

---

## 怎么快速建起来

不必一次填完。有效顺序：

1. 找出最近 10 份实际签署的同类合同
2. 看哪些条款每次都在改 → 那些就是需要 Preferred Position 的条款
3. 看最后实际接受的版本 → 那通常就是真实的 Acceptable Fallback
4. 看哪些改动当时惊动了上级 → 那就是 Escalation Trigger

**从"我们实际怎么做的"倒推，比从"我们应该怎么做"正推更准，也更快。**

也可以让 China Legal OS 帮你做：把历史合同交给它，路由到 `contract-playbook`，它会提取实际立场并生成初稿供你修改。
