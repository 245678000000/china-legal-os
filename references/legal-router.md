# Legal Router

把一个自然语言请求变成 `{primary, secondary[], lane, engines, reason, conflicts[]}`。

---

## 1. 三步

### 步骤 0 — 法域判定（先于一切）

默认 `CN-mainland`。出现以下信号时先确认法域，再决定是否继续：
香港 / HK / 澳门 / 台湾 / 新加坡 / 境外主体 / 跨境交易 / 外国法作为准据法 / 离岸架构。

非中国大陆法域 → **不勉强回答**：

> 这份合同的准据法是香港法。China Legal OS v0.1 只覆盖中国大陆法域，香港法下的结论我给不了可靠答案。
> 我能做的是：① 从中国大陆法域角度指出与内地强制性规定相关的部分（如涉及内地主体的外汇、数据出境、劳动用工）；② 列出需要香港律师确认的具体问题清单。要哪一个？

架构上 `references/jurisdictions/` 是可插拔挂载点，未来加法域不需要改路由结构。

### 步骤 1 — Triage（不可见）

一次廉价判断，只为三件事：
1. 领域猜测 → 决定 Fact Engine 用哪个事实抽取模板
2. Lane 初判
3. `our_side` 是否已知

Triage 不输出给用户，也不作为最终路由。

### 步骤 2 — Router（事实齐备后）

输出最终路由，对用户可见，**只写一行**：

> 按 商业秘密（主）+ 劳动、反不正当竞争（辅）处理，Lane C，证据分析为核心。

---

## 2. 多路由规则

| 规则 | 内容 |
|---|---|
| R-1 | **一个 primary，最多三个 secondary** |
| R-2 | primary 决定**交付物形态**和分析主线 |
| R-3 | secondary 只贡献**争点与要件**，不各自生成完整报告 |
| R-4 | `evidence` / `business-decision` 是常驻引擎，**永不作为路由目标** |
| R-5 | 模块结论冲突时**显式暴露冲突**，标明各自依据，不静默选择一方 |
| R-6 | 不为了显得全面而加载模块。每个 secondary 必须能回答"它贡献了哪个独立的争点或请求权基础" |

### R-6 的检验方法

加载一个 secondary 之前问自己：**去掉它，结论会不会变？**

- 会变 → 保留（例：商业秘密案件中 `labor` 贡献了竞业限制这条独立义务来源）
- 不会变，只是"相关" → 不加载，最多在末尾一句提示

---

## 3. Lane 判定

| Lane | 条件（满足全部） | 引擎 | 交付 |
|---|---|---|---|
| **A** | 单一问题 · 事实清楚 · 无对抗方 · 预估风险 ≤ Medium · 不命中升级清单 | Fact(轻) → Router → Research → Reasoning → G1-G4 | 3-10 行 + 依据 + 一个 caveat，不写文件 |
| **B** | 合同审查 / 合规评估 / 单一领域实体事项 | 全部；Red Team 仅对 High/Critical/BLACK | 一个主格式，写成文件 |
| **C** | 满足任一：多路由 · 争议已发生或迫近 · 存在 Critical 或 BLACK · 命中强制升级清单 · 涉及金额或影响重大 | 全部 + **强制** Red Team + **强制** Evidence Matrix + **强制** Business Decision | Executive Brief 置顶 + 1-2 个支撑格式 |

**升 Lane 容易，降 Lane 难。** 分析过程中发现 BLACK 风险、发现争议已进入程序、发现命中升级清单 → 立即升到 C，不要因为"用户只是随口问一句"而保持 A。

**四个 Gate 在三条 Lane 中都不可跳过。Lane 只改变深度与交付物厚度。**

---

## 4. 路由表

| 触发信号 | primary | 常见 secondary |
|---|---|---|
| 查法律怎么规定 / 是否合法 / 找依据 / "有没有法律规定" | `legal-research` | 领域模块 |
| 看合同 / 审合同 / 对方发来的版本 / 能不能签 / 有什么坑 | `contract-review` | `contract-playbook`、领域模块 |
| 建立标准立场 / 底线 / 审批规则 / 谈判手册 / 标准模板条款 | `contract-playbook` | `contract-review` |
| 起草合同 / 拟条款 / 出个模板 | `contract-drafting` | `contract-playbook` |
| 被起诉 / 要起诉 / 仲裁 / 收到律师函 / 纠纷怎么处理 | `dispute` | 领域模块、`labor` |
| 商标 / 专利 / 著作权 / 软件 / 被侵权 / 被指侵权 | `ip` | `competition`、`dispute` |
| 员工带走资料 / 泄密 / 保密协议 / 客户名单 / 技术外流 | `trade-secret` | `labor`、`competition` |
| 抹黑 / 仿冒 / 虚假宣传 / 刷单 / 爬数据 / 挖人 / 搭便车 | `competition` | `trade-secret`、`ip` |
| 辞退 / 竞业限制 / 加班 / 工伤 / 规章制度 / 劳动仲裁 / 调岗降薪 | `labor` | `trade-secret`、`dispute` |
| 个人信息 / 数据出境 / 隐私政策 / 用户授权 / 数据合作 | `data-privacy` | `compliance`、`contract-review` |
| 股权 / 董事会 / 决议 / 章程 / 关联交易 / 对外投资 | `corporate` | `compliance` |
| 新业务能不能做 / 牌照 / 广告合规 / 监管检查 / 整改 | `compliance` | 领域模块 |
| 尽调 / 投前法律审查 / 标的排查 | `legal-dd` | `corporate`、`ip`、`labor` |
| 出具正式法律意见 / 对外出函 | `legal-opinion` | 任一实体模块 |

### 歧义处理

匹配不明确时**不要停下来问用户选哪个**。选最可能的 primary 开始工作，在路由行里说明并给出切换选项：

> 按 合同审查（主）处理。如果你要的是"我们以后所有采购合同的标准立场"，说一声，我切到 contract-playbook。

---

## 5. 多路由示例

### 例 1：前员工带走客户名单入职竞争对手

```
primary   : trade-secret        客户名单是否构成商业秘密是本案主争点，决定全部路径
secondary : labor               竞业限制/保密义务是独立的请求权基础，且不依赖秘密性成立
            competition         对新雇主可能存在独立请求权
engines   : evidence（核心）、business-decision
lane      : C
不加载    : dispute —— 用户尚未决定维权，加载它会把分析引向程序问题而非可行性
conflicts : 若客户名单不构成商业秘密，trade-secret 路径关闭，但 labor 路径仍可能成立。
            两条路径的举证难度和救济范围不同，必须并列呈现
```

**为什么 labor 是必要的 secondary**：即使客户名单最终不被认定为商业秘密，竞业限制协议下的违约责任仍可能成立。这是一条**独立**的路径，去掉它会漏掉可能是最容易赢的那条。这就是 R-6 的检验。

### 例 2：对方发来的 SaaS 服务协议

```
primary   : contract-review
secondary : data-privacy（协议涉及用户个人信息处理）
engines   : business-decision
lane      : B
不加载    : compliance —— 与 data-privacy 重叠，无独立贡献
```

### 例 3：想辞退一个绩效不达标的员工

```
primary   : labor
secondary : （无）
engines   : evidence（核心 —— 本类问题的败诉主因是举证不能）、business-decision
lane      : B
升 C 条件 : 涉及三人以上 / 员工是孕期哺乳期 / 已有工伤 / 员工已投诉或曝光
```

---

## 6. 路由输出格式

对用户可见的**只有一行**。完整路由记录进内部状态，供 QA 与 chaining 使用：

```yaml
primary: trade-secret
secondary: [labor, competition]
engines: [evidence, business-decision, red-team]
lane: C
reason: 客户名单秘密性为主争点；竞业限制为独立请求权基础；新雇主责任为第三路径
conflicts:
  - 商业秘密路径与竞业限制路径的成立条件不同，需并列评估
excluded:
  - dispute: 用户尚未决定维权
```
