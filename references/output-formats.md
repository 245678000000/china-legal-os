# Output Formats

**不要所有任务输出同一种格式。** 格式由读者和决策类型决定，不由任务难度决定。

---

## 1. 选择规则

| Lane | 输出 |
|---|---|
| **A** | 直接回答，3-10 行 + 依据 + 一个 caveat。**不写文件，不套格式** |
| **B** | 一个主格式，写成文件 |
| **C** | Executive Brief 置顶 + 1-2 个支撑格式，写成文件 |

Lane B/C 交付物**写成文件**，不要堆在对话里——这些是要转发出去的文档。文件名：`[类型]-[主题]-[日期].md`

## 2. 八种格式

| 格式 | 读者 | 何时用 | Schema |
|---|---|---|---|
| **Executive Brief** | 管理层 | 需要一个决定 | `executive-brief.schema.json` |
| **Legal Research Memo** | 法务 | 研究类问题、需要留档的分析 | `legal-memo.schema.json` |
| **Contract Review** | 法务 + 业务 | 合同审查 | `contract-review.schema.json` |
| **Risk Matrix** | 法务 + 合规 | 多个风险点并列，需要排序处理 | `risk-matrix.schema.json` |
| **Evidence Matrix** | 法务 | 任何需要举证的事项 | `evidence-matrix.schema.json` |
| **Legal Opinion** | 对外 | 正式出函 | `legal-opinion.schema.json` |
| **Action Plan** | 执行人 | 方向已定，需要落地 | `action-plan.schema.json` |
| **Message / Email / Letter** | 业务/员工/客户/供应商/对方律师 | 需要直接发出的文本 | `message.schema.json` |

### 常见组合

| 场景 | 组合 |
|---|---|
| 重大合同 + 需要老板拍板 | Executive Brief + Contract Review |
| 商业秘密维权评估 | Executive Brief + Evidence Matrix + Action Plan |
| 员工纠纷处理 | Legal Memo + Message（给员工的通知）+ Action Plan |
| 新业务合规评估 | Risk Matrix + Action Plan |
| 尽调 | Risk Matrix + 未覆盖范围说明 |

---

## 3. 统一抬头（Lane B/C 强制）

每份交付物第一行：

```
Review Basis: 通用商业标准（未加载公司法务上下文） ｜ RETRIEVAL_MODE: none（法律依据未经核验）
我方立场: 甲方（采购方） ｜ 相关时点: 2026-08 ｜ Lane: B ｜ 生成日期: 2026-08-19
```

**抬头是 G4 交付闸的判定对象。** 缺失即 BLOCKED。

抬头要写实际情况：加载了 company context 就写 `Review Basis: 公司合同 Playbook v2 + 法务上下文`。

---

## 4. 通用骨架

除 Message 外，所有格式遵循：

```
[抬头]

## 结论 / 一句话
[如果只读一段，读这段。给决定，不给推导过程]

## [格式特有的主体部分]

## 需要注意的
[已知的不确定性、假设、限制条件]

## 待核验清单
[RETRIEVAL_MODE: none 下强制。按"核验不通过的影响"严重程度排序]

## 下一步
[做什么 · 谁 · 何时 · 需要什么。时限敏感项置顶]

---
本文由 AI 法务系统生成，依据未经检索核验，仅供内部工作参考，不构成法律意见。
重大事项请经执业律师或法务负责人复核。
```

**结论在最前面。** 法务和管理层读的是决定，不是推导过程。想看推导的人会往下读。

---

## 5. 各格式要点

### Executive Brief
- 一页。超过一页就不是 Brief
- 开头写清"要决定的是什么"
- 给推荐方案，不是列选项让老板选
- 必答"如果做会怎样"和"如果不做会怎样"
- 法律论证不放这里，放支撑文件

### Legal Research Memo
- 先给 short answer，再展开 IRAC
- 每个结论带确定性标签 + 封顶项
- 禁止只返回法条名清单或搜索结果列表

### Contract Review
- 按风险排序，不按条款顺序
- 每条给可直接插入的**中文条款文本**，不是"建议增加责任限制"
- `rationale_for_counterparty` 是可以直接发给对方律师的措辞，语气专业中性
- 必须包含跨条款数值推演结果

### Risk Matrix
- **必须写"未覆盖范围"**。不得以"未发现问题"表述未调查的部分
- 按处理优先级排序，不按发现顺序

### Evidence Matrix
- 时限敏感动作抽出置顶，写明"不做会怎样"
- 缺失证据具体到文件/系统/时间范围

### Legal Opinion
- 假设与限制条件必须显式且完整
- 无检索源下必须包含"依据未经核验"的限制声明
- 语气正式，不用口语

### Action Plan
- 每条：做什么 · 谁 · 何时前 · 需要什么
- 有顺序依赖的写明依赖关系

### Message / Email / Letter
- **只输出可直接发送的文本**，不要混入内部分析
- 单列 `不应包含的内容`：内部策略、证据弱点、法律不确定性——这些不能让收件人看到
- 标注是否需要法务/律师定稿
- 给对方律师的函件：措辞留有余地，不把话说死，不承认不利事实

---

## 6. 禁止

| 禁止 | 为什么 |
|---|---|
| 所有任务都用同一种格式 | 读者不同，需求不同 |
| Lane A 也套完整模板 | "这个 NDA 能签吗"不需要 8 页报告 |
| 把结论放在最后 | 读者可能读不到 |
| 内部策略分析出现在对外文本中 | 泄露谈判底线和证据弱点 |
| 缺抬头或缺待核验清单 | G4 BLOCKED |
| 全是负面发现 | 已经可以接受的条款也要说一句，否则报告读起来像机器生成的，会连带削弱真正重要的发现 |
