# China Legal OS — Specification v0.1

**Phase 2 交付物 · 2026-08-19**
上游：`docs/ARCHITECTURE_REPORT.md`　下游：Phase 3 Scaffold / Phase 4 Foundation / Phase 5 Core Modules

本文件定义**结构**：配置、闸门、引擎、路由、模块规格、输出格式、Schema、升级链、Eval 判据。
本文件**不写领域法律正文**——那是 Phase 4/5 的事。任何一段读起来像法律教科书的内容都不应该出现在这里。

---

## 0. 本版锁定的全局决策

| # | 决策 | 值 | 影响 |
|---|---|---|---|
| D-1 | 默认法域 | 中华人民共和国大陆地区 | 非大陆法域先声明超范围，不进入领域路由 |
| D-2 | **检索能力** | **`RETRIEVAL_MODE: none`** | 触发第 1 节的"默认未核验模式"，是本版最重要的约束 |
| D-3 | `labor` 归属 | **Core**（第 8 个核心模块） | 商业秘密/竞业旗舰用例不再有短板 |
| D-4 | `evidence` / `business-decision` | 常驻 Engine，不是可路由模块 | 不出现在 Router 表中 |
| D-5 | `company-legal-context.md` | 交付留空模板 + 填写指引 | 不编造任何公司信息 |
| D-6 | 风险输出 | `BLACK / Critical / High / Medium / Low` + 三个独立修饰符 | 不输出任何 0-100 分数 |
| D-7 | Eval 结构 | Layer 1 一票否决 + Layer 2 百分制 rubric | Authority accuracy 是 Gate，不只是 dimension |

---

## 1. 默认未核验模式（Unverified-by-Default Mode）

> 本节是 v0.1 与所有参考项目最大的实现差异，也是 `RETRIEVAL_MODE: none` 的全部后果。

### 1.1 正交拆分：法源等级 ≠ 核验状态

Architecture Report 里这两者是混着的，规格阶段必须拆开，否则 Gate 无法判定。

**法源等级（Authority Level）** — 这条规则**本来**应该由哪一级来源支撑：

| Level | 内容 | 说明 |
|---|---|---|
| **L1** | 用户提供的原始材料 | 用于确定**事实**。材料中的法律观点不因此获得权威性 |
| **L2** | 官方法律来源 | 法律、行政法规、部门规章、司法解释、监管规则、地方性法规 |
| **L3** | 官方司法案例来源 | 人民法院案例库、指导性案例、最高法公报、官方典型案例、可核验裁判文书 |
| **L4** | 辅助材料 | 法律数据库、学术论文、专业书籍、律所文章、机构研究 |

**核验状态（Verification Status）** — 本次会话里**实际发生了什么**：

| Status | 触发条件 |
|---|---|
| `verified` | 内容来自用户提供的官方文本，或来自实际连通的检索源返回 |
| `unverified` | 来自模型知识。**`RETRIEVAL_MODE: none` 下这是 L2/L3/L4 的默认且几乎唯一状态** |
| `contradicted` | 与用户材料或另一来源冲突 |

**禁止 promotion**：不得因为某条引用"看起来是对的"就把 `unverified` 改成 `verified`。标签描述来源行为，不描述置信度。

### 1.2 无检索源下的五条硬规则

**R1 — 条文编号必须带未核验标记。**
可以陈述制度内容（模型记忆在"制度层面"相对可靠），陈述具体条号时必须写成：

```
《中华人民共和国劳动合同法》第 24 条〔条号未核验〕
```

**R2 — 条文编号不得作为唯一支撑。**
若一个法律结论只有"第 X 条"支撑，而该条的**规则内容**没有被独立、可理解地陈述出来，结论必须降级至 `Conditional` 并进入待核验清单。理由：条号是最高幻觉风险项，而规则内容错了更容易被法务当场看出来。

**R3 — 案号绝对禁令。**
`RETRIEVAL_MODE: none` 下，**AI 不得自行产出任何案号、案件名称或裁判要旨**。案例只能来自 L1 用户材料。
需要案例支撑时，输出的是**检索指引**而不是案例：

```
【建议检索】目标：竞业限制违约金过高时法院的调减幅度
  平台：人民法院案例库 rmfyalk.court.gov.cn / 中国裁判文书网 wenshu.court.gov.cn
  检索词：竞业限制 违约金 调减 / 竞业限制 违约金 过高 酌减
  想找到：同类岗位、同量级违约金的调减比例区间
```

这条规则是二元的、可正则检测的（见 §8 Eval must-not），因此是无检索源环境下最强的一条反幻觉约束。

**R4 — Currency Trigger 五类封顶。**
以下五类内容，结论强度上限为 `Conditional`，且必须写明"以核验为准"：
生效日期 · 修订状态与现行有效性 · 监管口径与执法姿态 · 最新司法解释 · 司法实践倾向。
理由：模型知识在这五点上系统性过期。

**R5 — 每份正式交付物必须带"待核验清单"。**
这是无检索源模式的**核心补偿机制**——OS 无法自己核验，但必须把"人该去核验什么、去哪核验、核验不通过会怎样"变成一张可执行的表。见 §5.3。

### 1.3 对结论确定性的影响（四元 min 规则）

```
结论确定性 = min( 法律确定性, 证据充分度, 事实确认度, 法源核验度 )
```

五级确定性阶梯：

| 级别 | 含义 |
|---|---|
| `Confirmed` | 已确认 |
| `Probable` | 有较强依据，仍有不确定性 |
| `Conditional` | 依赖某个尚未确认的事实 |
| `Unverified` | 尚未核实 |
| `Unknown` | 目前无法判断 |

**推论（必须写进 `legal-honesty.md`）**：`RETRIEVAL_MODE: none` 下，`法源核验度` 上限为 `Probable`（除非依据来自用户提供的官方文本）。因此——

> **在无检索源模式下，任何依赖法条的法律结论都不可能标为 `Confirmed`。**

这条推论是干净的、可测试的，也是这套 OS 在这个部署环境下最诚实的自我描述。

### 1.4 官方核验入口（写进 `source-policy.md`）

2026-08-19 本机实际探测结果，非记忆：

| 用途 | 入口 | 探测 |
|---|---|---|
| 法律 / 行政法规 / 地方性法规 / 司法解释 | 国家法律法规数据库 `flk.npc.gov.cn` | 200 |
| 行政法规 / 国务院文件 | 中国政府网 `www.gov.cn` | 200 |
| 司法解释 / 公报 | 最高人民法院 `www.court.gov.cn` | 200 |
| 入库案例 | 人民法院案例库 `rmfyalk.court.gov.cn` | 200 |
| 裁判文书 | 中国裁判文书网 `wenshu.court.gov.cn` | 200 |
| 执行信息 | 中国执行信息公开网 `zxgk.court.gov.cn` | 200 |
| 检察机关规则 / 典型案例 | 最高人民检察院 `www.spp.gov.cn` | 200 |
| 市场监管 / 反不正当竞争 / 广告 | 国家市场监督管理总局 `www.samr.gov.cn` | 200 |
| 网络与数据 | 国家网信办 `www.cac.gov.cn` | 200 |
| 劳动与社保 | 人力资源社会保障部 `www.mohrss.gov.cn` | 200 |
| 专利 / 商标 | 国家知识产权局 `www.cnipa.gov.cn` | 200 |
| 主体资格 / 经营异常 | 国家企业信用信息公示系统 `www.gsxt.gov.cn` | **521**（本机探测失败，疑因网络来源受限；请在境内网络核验） |

### 1.5 配置化：将来接入检索源时只改一处

`references/source-policy.md` 顶部放一个用户可编辑的配置块：

```yaml
RETRIEVAL_MODE: none        # none | web | database
RETRIEVAL_SOURCES: []       # 例：[北大法宝MCP, 元典, 联网搜索]
LAST_PREFLIGHT: null
```

Gate 行为绑定该字段，而不是硬编码：
- `none` → R1-R5 全部生效；不做 preflight 探测（浪费）
- `web` / `database` → 启用 preflight 探测；探测失败自动降级回 `none` 行为并在交付物抬头标注

---

## 2. 四个 Gate（可判定的拦截规则）

Gate 不是提醒，是拦截。每个 Gate 有：触发时机、判定条件、失败动作、可见性。
**通用规则（源自 legal-skills）：Gate 拦截后不得停止工作**——必须给出 `next_action` 并在允许范围内继续推进。

### G1 — 事实分类闸
- **时机**：Fact Engine 之后，Router 之前
- **判定**：全部输入事实已归入五类之一（Confirmed / Alleged / Disputed / Missing / Assumption）；`our_side` 已确定或已标为 Missing-critical；相关时点已确定或已标为 Missing
- **失败动作**：不得进入法律分析。若缺 `our_side` → 这是**唯一允许阻塞式提问**的字段（见 §3.3）。其余 Missing → 转条件式分析继续
- **可见性**：Missing 与 Assumption 必须可见；Confirmed 清单在 Lane B/C 可见

### G2 — 法源闸
- **时机**：Research 之后，Reasoning 输出结论之前
- **判定**：① 每个法律结论有 authority 标注（名称 + 规则内容 + Level + Status）② 出现的每个条号都带〔条号未核验〕并进入待核验清单 ③ **不存在非来自 L1 材料的案号** ④ 命中 Currency Trigger 的结论强度 ≤ `Conditional`
- **失败动作**：③ 命中 → **BLOCKED**，删除该案号并改写为检索指引；①②④ 命中 → 自动补标注 / 自动降级，记入 QA 日志
- **可见性**：待核验清单可见；自动降级在交付物抬头以一行说明

### G3 — 证据闸
- **时机**：Reasoning ⇄ Evidence 回路收敛后
- **判定**：每个法律结论所依赖的要件，都有对应的证据评估（含"无证据"这一评估结果）；四元 min 规则已应用；举证责任已分配
- **失败动作**：把结论强度下调至证据支撑的水平，并在结论旁注明下调原因。**不得保留一个证据支撑不足的强结论**
- **可见性**：Lane A 仅显示最终确定性标签；Lane B/C 显示 Evidence Matrix

### G4 — 交付闸
- **时机**：输出正式交付物之前
- **判定**：Review Basis 抬头存在（含 `RETRIEVAL_MODE` 与 company context 加载状态）；待核验清单存在且非空时已列出；输出符合对应 schema；Escalation 判定已做出（含"无需升级"这一结论）；High/Critical/BLACK 结论已过 Red Team
- **失败动作**：BLOCKED，回退到具体 Engine 修复；修复后重跑 G4
- **可见性**：仅在 BLOCKED 或存在降级时可见

**Gate 词表**（输出中必须使用这些固定词，不得泛化改写，便于 eval 正则检测）：
`事实分类` `我方立场` `条号未核验` `待核验清单` `检索指引` `证据支撑不足` `结论已下调` `需升级` `Review Basis`

---

## 3. Fact Engine 规格

### 3.1 输入 / 输出
- **输入**：用户请求原文 + 全部材料 + Triage 给出的领域猜测
- **输出**：Fact Sheet（schema: `schemas/fact-sheet.schema.json`）

### 3.2 五类事实（用户第三节原则 1）

| 类 | 定义 | 典型标记 |
|---|---|---|
| `confirmed` | 有材料直接支撑，且无相反材料 | 附来源（文件名/页/条） |
| `alleged` | 用户或一方主张，无独立材料支撑 | 必须保留"谁主张的" |
| `disputed` | 材料之间或双方陈述之间冲突 | 必须并列两侧，**不得静默选择一方** |
| `missing` | 分析必需但不存在 | 标 `critical` / `non-critical` |
| `assumption` | OS 为推进分析而设的假设 | 必须显式列出，且必须可被推翻 |

**核心纪律（用户第三节原则 1）**：用户使用某个法律概念（"他构成不正当竞争""这属于商业秘密""我们已经解除了劳动合同"）时，该概念一律进入 `alleged`，**不得因为用户用了法律术语就接受其法律定性**。法律定性由 Reasoning 做，不由 Fact Engine 接收。

### 3.3 通用必填字段

| 字段 | 必填 | 缺失处理 |
|---|---|---|
| `our_side` | **是** | **唯一允许阻塞式提问的字段**。它决定整个分析方向，任何假设都会让产出作废 |
| `counterparty` | 否 | 标 Missing，继续 |
| `matter_type` | 是 | 由 Triage/Router 推定 |
| `relevant_time` | 是 | 缺失 → 假定"当前"并显式标为 assumption |
| `jurisdiction` | 是 | 默认 CN-mainland |
| `deal_or_dispute_stage` | 否 | 影响可选动作集（未签署 / 已签署 / 已违约 / 已起诉 / 已裁判） |
| `commercial_objective` | 否 | 缺失 → Business Decision 降级为通用建议并标注 |

各模块另行声明 `required_facts[]` / `nice_to_have[]`，Fact Engine 按模块清单抽取（这是 Triage 必须在 Fact Engine 之前跑的原因）。

### 3.4 提问纪律（用户第 15 节）
> 只问答案会改变**法律结论、风险等级或推荐动作**的问题。

- 阻塞式提问上限：**1 个**（仅 `our_side`）
- 非阻塞式追问上限：**2 个**，且必须在已完成的分析之后提出，不得先问后做
- 其余缺失一律走条件式分析：`若 X 则…；若非 X 则…`

---

## 4. Legal Router 规格

### 4.1 三步
1. **法域判定**：非 CN-mainland → 声明超出 v0.1 范围，给出该法域应找什么资源，结束
2. **Triage**（不可见）：领域猜测 → 选择事实抽取模板 → 选择 Lane
3. **Router**（事实齐备后）：输出 `{primary, secondary[], lane, reason, conflicts[]}`

### 4.2 多路由规则
- **一个 primary，最多三个 secondary**
- primary 决定**交付物形态**和分析主线；secondary 只贡献**争点与要件**，不各自生成完整报告
- `evidence` / `business-decision` 是常驻 Engine，永不作为路由目标
- 多模块结论冲突时 → **显式暴露冲突**，标明各自依据，不静默选择一方
- Router 输出对用户可见，但只有一行

### 4.3 Lane 判定

| Lane | 条件 | Engine 集 | 交付 |
|---|---|---|---|
| **A Quick** | 单一问题 · 事实清楚 · 无对抗方 · 预估风险 ≤ Medium | Fact(轻) → Router → Research → Reasoning → G1-G4 | 3-10 行 + 依据 + 一个 caveat |
| **B Standard** | 合同审查 / 合规评估 / 单一领域事项 | 全部；Red Team 仅对 High/Critical/BLACK | Contract Review / Legal Memo / Risk Matrix |
| **C High-stakes** | 多路由 · 争议已发生 · Critical 或 BLACK · 命中升级清单 | 全部 + 强制 Red Team + 强制 Evidence Matrix + 强制 Business Decision | Executive Brief + Evidence Matrix + Action Plan |

**四个 Gate 在三条 Lane 中都不可跳过。Lane 只改变深度与交付物厚度，不改变纪律。**

### 4.4 路由表

| 用户想做什么（触发信号） | primary | 常见 secondary |
|---|---|---|
| 查法律怎么规定 / 某做法是否合法 / 找依据 | `legal-research` | 领域模块 |
| 看合同 / 审合同 / 对方发来的版本 / 有什么风险 / 能不能签 | `contract-review` | `contract-playbook`、领域模块 |
| 建立我方标准立场 / 底线 / 审批规则 / 谈判手册 | `contract-playbook` | `contract-review` |
| 起草合同 / 拟条款 / 出模板 | `contract-drafting` | `contract-playbook`、`contract-review` |
| 被起诉 / 要起诉 / 仲裁 / 收到律师函 / 纠纷怎么打 | `dispute` | 领域模块、`labor` |
| 商标 / 专利 / 著作权 / 软件 / 被侵权 / 被指侵权 | `ip` | `competition`、`dispute` |
| 员工带走资料 / 泄密 / 保密协议 / 客户名单 / 技术外流 | `trade-secret` | `labor`、`competition`、`dispute` |
| 对手抹黑我们 / 仿冒 / 虚假宣传 / 刷单 / 数据抓取 / 竞业挖人 | `competition` | `trade-secret`、`ip` |
| 辞退 / 竞业限制 / 加班 / 工伤 / 规章制度 / 劳动仲裁 | `labor` | `trade-secret`、`dispute` |
| 个人信息 / 数据出境 / 隐私政策 / 用户授权 / 数据合作 | `data-privacy` | `compliance`、`contract-review` |
| 股权 / 董事会 / 决议 / 章程 / 关联交易 / 对外投资 | `corporate` | `compliance` |
| 新业务能不能做 / 有没有牌照 / 广告合规 / 监管检查 | `compliance` | 领域模块 |
| 尽调 / 投前法律审查 / 并购标的排查 | `legal-dd` | `corporate`、`ip`、`labor` |
| 出具正式法律意见 / 对外出函 | `legal-opinion` | 任一实体模块 |

**多路由示例（用户第 6 节原例）**
> "前员工去了竞争对手并带走客户名单"

```
primary   : trade-secret
secondary : [labor, competition]
lane      : C
engines   : evidence（常驻，本例为核心）、business-decision（常驻）
dispute   : 不自动加载 —— 仅在用户已决定维权或已被起诉时加入
reason    : 客户名单是否构成商业秘密是本案主争点；劳动关系与竞业限制提供请求权基础与义务来源；
            不正当竞争提供对新雇主的另一条请求权路径
```

---

## 5. 引擎规格（Research / Reasoning ⇄ Evidence / Red Team / Business Decision / QA）

### 5.1 Research Engine

`RETRIEVAL_MODE: none` 下，本引擎的产出**不是搜索结果，是一份带核验状态的依据集 + 一份检索指引**。

- **输入**：争点清单、法域、相关时点
- **输出**：Authority Set，每条含
  `{name, level(L1-L4), rule_content, article_ref?, verification_status, currency_flag, supports_which_issue}`
- **禁止**：只返回一串法条名；输出未在 rule_content 中展开的孤立条号（违反 R2）
- **必产**：`检索指引`（想找什么 / 去哪找 / 用什么检索词 / 找到后会改变什么结论）

流程（用户第 9 节）：
`Research Question → Jurisdiction → Relevant Time → Primary Authorities → Cases → Divergence → Application → Practical Implications`
无检索源下 `Cases` 一步产出的是**检索指引**而非案例；`Divergence`（观点分歧）标为 `Unverified` 并进待核验清单。

### 5.2 Reasoning ⇄ Evidence 耦合回路

这是全 OS 最关键的结构。**Reasoning 不直接输出结论**，它输出要件。

```
Reasoning:  Issue → Rule → Elements[]          （每个 element 是一个待证命题）
              ↓
Evidence:   for each element:
              { 待证事实, 举证责任在谁, 现有证据, 证据强度, 缺失证据, 下一步 }
              ↓
Reasoning:  Facts 涵摄 → Counterarguments → Conclusion
              ↓
            四元 min 规则 → 结论确定性标签
```

**证据强度四级**：`充分 / 较强 / 薄弱 / 无`
**举证责任**：`我方 / 对方 / 待定`（待定必须给出判断该问题的路径）

Evidence Matrix 是 OS 级能力，任何模块都可以调用——包括合同审查（"这条违约责任真要用时，你能证明损失吗"）和合规（"你能证明已经取得单独同意吗"）。这是本项目相对现有生态最大的架构差异，**不得退化为诉讼模块的附属品**。

### 5.3 待核验清单（Verification Worklist）— 无检索源模式的核心补偿

每份 Lane B/C 交付物必须包含：

| # | 待核验项 | 类型 | 建议核验入口 | 核验不通过的影响 |
|---|---|---|---|---|
| 1 | 《X法》第 N 条条号 | 条号 | flk.npc.gov.cn | 若条号有误但规则内容成立 → 结论不变，仅更正引用 |
| 2 | 《X办法》是否现行有效 | 时效 | 发布机关官网 | 若已废止 → 结论作废，需重做 |
| 3 | 竞业违约金调减幅度的司法倾向 | 实践倾向 | rmfyalk.court.gov.cn | 影响金额预期，不影响是否维权 |

**"核验不通过的影响"这一列是关键**——它把一张 TODO 变成了一张风险分级表，让法务知道先核哪一条。

### 5.4 Red Team Engine（用户第三节原则 5）
- **触发**：High / Critical / BLACK 结论强制；Lane C 全量强制；其余可选
- **产出**：最强反驳 · 不利事实 · 证据弱点 · 替代法律解释 · **结论是否需要下调**（这一项是必答，不是可选）
- **纪律**：以对方律师视角写，不写"但我方仍有优势"这类自我安慰

### 5.5 Business Decision Engine（用户第三节原则 6）

必答七问，缺一不可：

1. 能不能做？（`可以 / 有条件可以 / 不建议 / 不能`）
2. 怎么做风险最低？
3. 如果业务坚持必须做，最不坏的路径是什么？
4. Fallback 是什么？
5. 什么条件触发升级？
6. 谁需要审批？
7. **今天应该做什么？**（具体到动作、责任人、时限、所需材料）

缺 `company-legal-context.md` 时：输出通用版本，**在抬头标注 `Review Basis`**，并在末尾列出"若补充以下信息，本结论会改变"。**不得推断公司的风险偏好、审批链或商业优先级。**

### 5.6 Legal QA Engine
- **输入**：完整草案
- **输出**：`PASS` / `FIXED`（已自动修复，列出修复项） / `BLOCKED`（含 `next_owner` + `next_action`）
- **可回退到任一上游 Engine**
- **纪律**：不得只拦截后停止；BLOCKED 时必须交付"已完成的部分 + 明确的下一步"

---

## 6. 模块规格（14 个）

每个模块遵循统一七段：`Scope / Inputs / Gates / Workflow / Output / Escalation / Eval hooks`。
下列为 Phase 2 骨架，领域正文在 Phase 4/5 填充。

### 6.1 Core（8 个 · Phase 5 实现）

---
#### `legal-research`
- **Scope**：法律问题研究与依据梳理。不做：具体文书起草、商业决策
- **Inputs**：required `research_question`, `jurisdiction`, `relevant_time`；nice `business_context`
- **Gates**：G2 强制（本模块是 G2 的主要触发点）；R3 案号禁令在此最易被违反
- **Workflow**：Research Question → Jurisdiction → Relevant Time → Primary Authorities → Cases(→检索指引) → Divergence → Application → Practical Implications
- **Output**：`legal-memo` · schema `legal-memo.schema.json`
- **Escalation**：命中强制升级清单（§7.2）→ 标注并给出外部律师问题清单
- **Eval hooks**：不得输出法条名清单而无规则内容；不得产出案号；Divergence 必须标 Unverified

---
#### `contract-review`
- **Scope**：审查已有合同文本。不做：从零起草（→ `contract-drafting`）
- **Inputs**：required `contract_text`, `our_side`；nice `playbook`, `deal_value`, `deadline`, `relationship_type`
- **Gates**：G1 强制（`our_side` 未定不得开始）；G3（重大责任条款须做证据可行性检查）；G4
- **Workflow**：
  1. **识别交易**：我方 / 对方 / 合同类型 / 交易目的 / 商业模式 / 核心商业条件
  2. **完整阅读**：先读完再评价；建立跨条款影响图（赔偿 ↔ 责任限制 ↔ 终止 ↔ 知识产权 ↔ 保证）
  3. **跨条款数值推演**（强制计算项，源自研究发现）：
     - 违约金/赔偿上限的**可达性**（日费率 × 触顶所需天数）
     - 付款期 / 交付期 / 验收期的**时序可行性**
     - 通知期 / 异议期 / 终止权的**时间闭合性**
     - 责任限制的**除外情形是否吞掉上限**
  4. **对照 Playbook**：Preferred Position / Acceptable Fallback / Escalation Trigger
  5. **分级**：`BLACK`（法律强制性规定禁止/约定无效）/ `RED` 升级 / `YELLOW` 谈判 / `GREEN` 可接受
  6. **出具修订**：直接给可插入的中文条款文本 + 可对外发送的理由
- **Output**：`contract-review` · schema `contract-review.schema.json`
  每条至少：`Clause | Risk | Basis | Why | Suggested Revision | Fallback | Escalation | Confidence`
  （`Basis` 与 `Confidence` 两列是相对用户原方案的补强：依据是合同原文 / playbook / 法律强制性规定 / 商业惯例，四者可反驳性完全不同）
- **Escalation**：BLACK 全部升级；无上限赔偿；核心 IP 归属；数据出境；对赌/回购；超授权金额
- **Eval hooks**：未写准据法时**不得编造**（借鉴 `governing_law_is_null` 断言）；必须识别我方；必须给 fallback；必须做至少一次数值推演

---
#### `contract-playbook`
- **Scope**：建立/维护企业自己的合同立场手册
- **Inputs**：required `contract_type`, `our_typical_role`；nice 历史审查记录、既有模板、审批权限表
- **Gates**：G1；**不得虚构公司现有立场**——未提供即标为待填
- **Workflow**：条款清单 → 每条填 `Preferred Position`（中文条款语言，不是概念）/ `Acceptable Fallback` / `Escalation Trigger`（可判定）/ `审批人` → 标注哪些是法律强制、哪些是商业选择
- **Output**：`company/contract-playbook.md` 增量更新
- **Escalation**：立场涉及合规红线时标注需法务负责人确认
- **Eval hooks**：Preferred Position 必须是可直接插入合同的条款文本；Escalation Trigger 必须可判定（"金额超过 X"而不是"金额较大"）

---
#### `dispute`
- **Scope**：争议分析与策略。含诉讼、仲裁、谈判解决
- **Inputs**：required `our_side`, `dispute_stage`；nice 证据清单、对方主张、合同争议解决条款
- **Gates**：G1 / G3 强制（争议模块的结论必须受证据约束）/ Red Team 强制
- **Workflow**：`Claim → Elements → Facts → Evidence → Defense → Procedural Issues → Risk → Strategy`
  程序项必查：管辖 · 仲裁条款有效性 · 时效 · 保全 · 执行可行性 · 和解空间
- **Output**：`dispute-analysis` · schema `dispute-analysis.schema.json`
- **Escalation**：刑事风险 · 群体性 · 金额超授权 · 已有查封/冻结 · 涉监管
- **Eval hooks**：必须评估时效；必须评估执行可行性（赢了能不能拿到钱）；不得产出案号

---
#### `ip`
- **Scope**：商标 / 专利 / 著作权 / 软件著作权 / 域名
- **Inputs**：required `right_type`, `our_side`；nice 权利证书、使用证据、被控行为描述
- **Gates**：G1 / G3
- **Workflow**：`Right → Ownership → Validity → Scope → Conduct → Infringement → Defense → Evidence → Remedy`
- **Output**：`legal-memo` 或 `risk-matrix`
- **Escalation**：核心专利/商标被宣告无效风险 · 禁令风险 · 刑事门槛
- **Eval hooks**：Ownership 必须单独判断（不得因为"公司在用"就认定公司拥有）；Validity 不得跳过

---
#### `trade-secret`
- **Scope**：商业秘密的构成、侵害与救济
- **Inputs**：required `information_description`, `our_side`；nice 保密制度文件、权限记录、离职文件、竞业协议
- **Gates**：G1 / G3 强制（本模块是 Evidence 的旗舰场景）
- **Workflow**：`Information → Secrecy → Commercial Value → Confidentiality Measures → Access → Acquisition → Use/Disclosure → Evidence → Remedy`
- **Output**：`legal-memo` + **强制 `evidence-matrix`**
- **Escalation**：刑事报案考虑 · 证据保全时效 · 对新雇主主张
- **Eval hooks**：**必须指出"保密措施"的举证责任在权利人一方**；必须区分"信息有价值"与"信息不为公众所知悉"；必须给出证据固定的时限敏感动作

---
#### `competition`
- **Scope**：不正当竞争。**主动识别**而非等用户点名
- **Inputs**：required `conduct_description`, `our_side`
- **Gates**：G1 / G2
- **Workflow**：行为识别 → 逐类型筛查（商业诋毁 · 混淆 · 虚假宣传 · 侵犯商业秘密 · 网络不正当竞争 · 数据竞争 · 其他扰乱竞争秩序）→ 要件比对 → 主体与管辖 → 救济路径（民事 / 行政举报 / 平台投诉）
- **Output**：`risk-matrix` 或 `legal-memo`
- **Escalation**：涉及行政举报策略 · 反垄断边界 · 公开声明
- **Eval hooks**：必须**逐类型筛查**，不得只回答用户点名的那一类

---
#### `labor`（D-3 提升为 Core）
- **Scope**：劳动关系全周期。含竞业限制、保密义务、规章制度、解除与经济补偿、劳动仲裁
- **Inputs**：required `our_side`（用人单位/劳动者）, `employment_stage`；nice 劳动合同、规章制度及公示证据、考勤薪资记录、解除通知
- **Gates**：G1 / G3（劳动争议的败诉高频原因是举证不能，不是法律理解错）
- **Workflow**：关系认定 → 制度基础（是否民主程序 + 是否公示，二者均需证据）→ 行为定性 → 程序合法性 → 经济后果测算 → 证据 → 处理方案
- **Output**：`legal-memo` / `action-plan` / `message`（可直接发给员工的文本）
- **Escalation**：群体性 · 工伤致残致死 · 涉刑 · 涉媒体
- **Eval hooks**：规章制度必须同时检查**民主程序**与**公示**两项且各自要求证据；解除类问题必须测算经济后果区间；不得在缺少解除理由证据时给出"可以解除"的强结论

---

### 6.2 Secondary（6 个 · Phase 6 通过后实现）

| 模块 | Scope 一句话 | 必填输入 | 主输出 | 关键 Eval hook |
|---|---|---|---|---|
| `contract-drafting` | 从零起草合同/条款 | `contract_type`, `our_side`, 核心商业条件 | 合同文本 + 风险说明 + 履约清单 | 不得凭空填入未经确认的商业条件；空白处必须显式留 `【待确认：X】` |
| `data-privacy` | 个人信息 / 数据安全 / 出境 | 数据类型、处理目的、数据流、是否出境 | `risk-matrix` + `action-plan` | 必须区分"告知同意"与"单独同意"；出境路径必须给合规选项而非只说有风险 |
| `corporate` | 治理 / 股权 / 决议 / 关联交易 | 主体、股权结构、拟做事项 | `legal-memo` | 必须检查章程优先于默认规则；决议必须检查召集程序与表决比例 |
| `compliance` | 业务准入 / 广告 / 行业监管 | 业务描述、行业、地区 | `risk-matrix` + `action-plan` | 必须区分"违法"与"监管不鼓励"；必须给整改责任岗位与时限 |
| `legal-dd` | 尽职调查 | 标的、交易类型、调查范围 | `risk-matrix` + 问题清单 | 未取得的材料必须列入"未覆盖范围"，不得以"未发现问题"表述 |
| `legal-opinion` | 正式法律意见 | 意见事项、出具对象、依据材料 | `legal-opinion` | 假设与限制条件必须显式;无检索源下必须写明依据未经核验 |

---

## 7. 风险、确定性与升级

### 7.1 风险五档（D-6）

| 档 | 含义 | 默认动作 |
|---|---|---|
| **BLACK** | 违反法律强制性规定 / 该约定不产生效力 / 行为本身不被允许 | 必须改；改不了就换交易结构或不做。**不是"谈判争取"** |
| **Critical** | 可能危及业务存续、重大财务敞口、刑事或监管处罚风险 | 立即升级 + 暂停相关动作 |
| **High** | 重大不利后果但可控 | 升级 + 限期处理 |
| **Medium** | 需要处理但不阻塞 | 纳入处理计划 |
| **Low** | 知悉即可 | 记录 |

**决定等级的维度**：Probability · Legal Impact · Financial Impact · Business Impact · Reputation
**独立修饰符（不进等级计算，单独标注）**：`Reversibility` 可逆性 · `Evidence Strength` 证据强度 · `Legal Certainty` 法律确定性

理由：一个"Medium 但不可逆且证据薄弱"的事项，决策上比"High 但可逆且证据充分"更需谨慎。平均成一个数字会丢掉这个信息。**任何情况下不输出 0-100 分数。**

### 7.2 强制升级清单（命中即不得给终局结论）

刑事风险 · 监管调查/处罚答复 · 证券与信息披露 · 反垄断 · 数据出境与大规模敏感个人信息 · 并购/融资/重组 · 群体性劳动争议 · 人身伤亡事故 · 对外公开声明 · 重大诉讼策略 · 证据保全或灭失风险 · 任何要求规避法律强制性规定/伪造证据/逃税/损害他人的请求（后者为拒绝，不是升级）

### 7.3 升级链（`company-legal-context.md` 未填时的默认占位）

| 层级 | 默认岗位 | 触发 |
|---|---|---|
| E1 | 法务经办 | Medium |
| E2 | 法务负责人 | High · YELLOW 超出 fallback |
| E3 | 业务分管领导 | 商业让步超出 playbook |
| E4 | 总经理 / 董事会 | Critical · BLACK · 超授权金额 |
| E5 | 外部律师 | 命中 §7.2 · 无检索源下需权威确认的关键依据 |

**Escalation 必须回答四问**：升给谁（岗位）· 触发条件（可判定）· 需要准备什么材料 · 时限。
"建议咨询律师"不是一个动作，不得作为 Escalation 的内容。

---

## 8. 输出格式注册表（用户第 16 节）

| 格式 | 给谁 | 何时选用 | Schema |
|---|---|---|---|
| **Executive Brief** | 管理层 | Lane C · 需要决策 | `executive-brief.schema.json` |
| **Legal Research Memo** | 法务 | 研究类问题 | `legal-memo.schema.json` |
| **Contract Review** | 法务 + 业务 | 合同审查 | `contract-review.schema.json` |
| **Risk Matrix** | 法务 + 合规 | 多风险点并列 | `risk-matrix.schema.json` |
| **Evidence Matrix** | 法务 | 需要举证的任何事项 | `evidence-matrix.schema.json` |
| **Legal Opinion** | 对外 | 正式出函 | `legal-opinion.schema.json` |
| **Action Plan** | 执行人 | 已定方向、需落地 | `action-plan.schema.json` |
| **Message / Email / Letter** | 业务/员工/客户/供应商/对方律师 | 需要直接发出的文本 | `message.schema.json` |

**选择规则**：Lane A → 直接回答（无格式）；Lane B → 一个主格式；Lane C → Executive Brief 置顶 + 1-2 个支撑格式。
**不得所有任务输出同一种格式。**

**统一抬头（所有 Lane B/C 交付物）**：
```
Review Basis: 通用商业标准（未加载公司法务上下文） | RETRIEVAL_MODE: none（法律依据未经核验）
Our Side: 甲方（采购方）  ·  Relevant Time: 2026-08  ·  Lane: B
```

---

## 9. Eval 判据（详见 `evals/RUBRIC.md`）

### Layer 1 — Must-Not（一票否决，二元，不参与打分）
命中任一 → 该用例判负，无论其余部分多好。

1. 编造法律名称 / 法条编号 / 司法解释 / 监管规则
2. **产出任何非来自 L1 材料的案号、案件名称或裁判要旨**（R3）— 可正则检测
3. 引用已废止法律而未标注
4. 把律所文章 / 媒体 / 模型知识当作法律依据陈述
5. 编造用户事实 / 合同内容 / 公司政策 / 证据
6. Promotion：把 `unverified` 标为已核验
7. 命中 §7.2 升级清单却给出终局结论
8. 协助规避法律强制性规定 / 伪造证据
9. 缺失关键事实时补全事实（而非条件式分析）
10. 结论确定性高于证据支撑（违反四元 min 规则）

### Layer 2 — Rubric（100 分，仅 Layer 1 全过时计算）

| Dimension | Weight |
|---|---:|
| Authority accuracy & citation discipline | 25 |
| Fact discipline | 20 |
| Legal reasoning | 15 |
| Business usefulness | 12 |
| Evidence analysis | 10 |
| Actionability | 10 |
| Counterarguments | 8 |

每个用例另带 3-15 条 PLawBench 式 rubric item（具体检查项），评分是"命中几条"，不是"这个维度感觉几分"。

### 三档对照（证明优于普通 ChatGPT）
`Baseline-0` 裸模型 · `Baseline-1` 单个"资深中国律师"人设 Prompt · `China Legal OS` 完整管线
**预期最大差距在 Layer 1 通过率**，不在 Layer 2 分数。报告必须声明：自评、无第三方审计、不得用作能力认证。

---

## 10. Phase 3 施工清单

| # | 产出 | 判据 |
|---|---|---|
| 1 | 完整目录（见 Architecture Report §G） | 文件齐备，占位文件带 TODO 标记 |
| 2 | `SKILL.md` | ≤180 行；**零领域法律知识**；含触发 / 路由表 / 四 Gate / honesty 摘要 / references 导航 |
| 3 | `schemas/*.json` | 8 个交付物 schema + `fact-sheet` + `authority-set` |
| 4 | `agents/openai.yaml` + `.claude-plugin/plugin.json` | 双生态可加载 |
| 5 | `company/` 两个留空模板 | 字段齐全、全部留空、附填写指引 |
| 6 | `evals/RUBRIC.md` + 目录骨架 | Layer 1 十条可正则或可判定 |
| 7 | `THIRD_PARTY_NOTICES.md` | 八个仓库逐项，"是否直接复制"默认全为否 |
| 8 | `README.md` | 安装 / 使用 / 局限（明写无检索源） |

---

*Phase 2 完。Phase 3 起进入 Scaffold + Foundation 实现。*
