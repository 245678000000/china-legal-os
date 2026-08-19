# China Legal OS (中国法务操作系统)

> **面向中国大陆企业法务的模块化 AI 工作系统。**  
> 不是玩具式的法律问答，不是空洞的“扮演律师”人设 Prompt。让通用 AI 按**企业法务的实际工作流**深度协同：**事实分类 → 争点要件拆解 → 证据链核验 → 红队对抗检验 → 落地商业决策**。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Health Score](https://img.shields.io/badge/Health_Score-100%2F100-success.svg)](#系统健康度)
[![Layer 1 Pass](https://img.shields.io/badge/Layer_1_Pass-100%25-brightgreen.svg)](#自动化评测)
[![Jurisdiction](https://img.shields.io/badge/Jurisdiction-CN--mainland-red.svg)](#法域)

---

## 💡 为什么需要 China Legal OS？

| 业务场景 | 普通法律问答 / 单体 Prompt | China Legal OS |
|---|---|---|
| **用户主张** | “他窃取了商业秘密” → 顺着定性分析 | 归入 `Alleged`，拆解法定要件，由事实与证据重新定性 |
| **法条引用** | 直接写“根据《X法》第 N 条” | 输出规则内容 + 标明 `〔条号未核验〕` + 纳入待核验清单 |
| **案例裁判** | 生成看起来合法的虚拟案号（幻觉） | **绝对禁令（0个虚拟案号）**，转为生成精准检索指引 |
| **证据缺失** | 照常给出高度确定的胜诉结论 | **四元 min 确定性规则**：证据不足强制下调结论确定性 |
| **商业决策** | “存在法律风险，建议谨慎咨询律师” | **商业落地七问**：能不能做 / 最不坏路径 / Fallback / 谁审批 / 今天做什么 |
| **风险量化** | 输出伪精确的“风险指数 85%” | **五档风险 + 三独立修饰符**（法律确定性 / 证据强度 / 可逆性） |
| **对方抗辩** | 单向证明己方观点 | **强制 Red Team 红队推演**，必须回答“结论是否需下调” |

---

## 🏛️ 系统架构与数据流动

```text
                       用户输入 / 附件合同 / 案卷材料
                                     │
                             ┌───────▼───────┐
                             │    Triage     │  领域与泳道推断 (Lane A/B/C) [不可见]
                             └───────┬───────┘
                             ┌───────▼───────┐
                             │  Fact Engine  │  五类事实抽取 (Confirmed/Alleged/Missing)
                             └───────┬───────┘
                                 ══ G1 事实分类闸 ══
                             ┌───────▼───────┐
                             │ Legal Router  │  多路由协同 (Primary + Secondary) [可见一行]
                             └───────┬───────┘
                             ┌───────▼───────┐
                             │   Research    │  法源等级 (L1-L4) + 规则梳理 + 检索指引
                             └───────┬───────┘
                                 ══ G2 法源闸 ══
                       ┌─────────────▼─────────────┐
                       │   Reasoning  ⇄  Evidence   │  要件拆解 ⇄ 证据矩阵 (四元 min 规则)
                       └─────────────┬─────────────┘
                                 ══ G3 证据闸 ══
                             ┌───────▼───────┐
                             │   Red Team    │  对方最强抗辩 / 证据薄弱点反思
                             └───────┬───────┘
                             ┌───────▼───────┐
                             │Business Decis.│  商业落地七问 (最不坏路径 / 谁审批 / 今日动作)
                             └───────┬───────┘
                                 ══ G4 交付闸 ══
                             ┌───────▼───────┐
                             │   Legal QA    │  Review Basis 抬头 + 待核验清单拦截
                             └───────┬───────┘
                                     │
                ┌────────────────────┴────────────────────┐
                ▼                                         ▼
      Markdown 结构化交付物                      自包含 HTML / PDF 打印报表
```

---

## 🚀 快速开始

### 1. 一键多生态安装
运行自动化配置脚本，一键软链接至您的常用智能体环境：

```bash
git clone https://github.com/your-org/china-legal-os.git
cd china-legal-os
./scripts/install.sh
```

支持一键无缝接入：
- **Claude Code**: `~/.claude/skills/china-legal-os`
- **Codex / OpenAI**: `~/.codex/skills/china-legal-os`
- **Antigravity / Gemini**: `~/.gemini/config/skills/china-legal-os`
- **本地全局 CLI**: `~/.local/bin/clos`

### 2. 命令行交互式工作台 (CLI)

```bash
# 1. 运行合同审查并导出高保真 HTML 报表
./bin/clos review -t "审查大数据采购协议" -f examples/01-contract-review/input.md --html report.html

# 2. 法律问题快速咨询 (Lane A)
./bin/clos ask -t "合同未写签署日期仅盖公章是否生效"

# 3. 运行全系统健康体检 (100/100 诊断)
./bin/clos doctor

# 4. 运行全量 14 个用例基准跑测
./bin/clos eval

# 5. 启动交互式法务助手模式
./bin/clos interactive
```

---

## 📦 模块全景与资产清单

### 1. 业务领域工作流 (14 个模块 · 统一七段式架构)
位于 [`references/`](references/) 目录：
- **8 个 Core 核心模块**：
  - [`contract-review.md`](references/contract-review.md) —— 合同审查（跨条款数值推演、400天违约金触顶计算、8列审查表）
  - [`trade-secret.md`](references/trade-secret.md) —— 商业秘密维权（三要件举证责任、24h/3d 紧急时限敏感取证）
  - [`labor.md`](references/labor.md) —— 劳动用工全周期（规章制度民主公示双重核验、2N 赔偿量化测算）
  - [`competition.md`](references/competition.md) —— 不正当竞争主动识别（七类行为逐项排查、多元救济）
  - [`ip.md`](references/ip.md) —— 知识产权（权属独立核验、全面覆盖侵权比对）
  - [`dispute.md`](references/dispute.md) —— 争议分析（诉讼时效中断、财产保全、执行可行性）
  - [`contract-playbook.md`](references/contract-playbook.md) —— 合同谈判手册（标准条款文本、退让底线、量化升级触发）
  - [`legal-research.md`](references/legal-research.md) —— 深度法律研究（新旧法溯及力、观点分歧 Unverified 标记）
- **6 个 Secondary 次要模块**：
  - [`contract-drafting.md`](references/contract-drafting.md) —— 合同从零起草（商业未定项 `【待确认：X】` 占位）
  - [`data-privacy.md`](references/data-privacy.md) —— 数据合规（单独同意法定场景、数据出境三条路径）
  - [`corporate.md`](references/corporate.md) —— 公司治理（章程自治优先、新公司法 5 年实缴期限、决议效力瑕疵）
  - [`compliance.md`](references/compliance.md) —— 行业监管准入（违法禁止 vs 监管审慎、广告极限词合规）
  - [`legal-dd.md`](references/legal-dd.md) —— 尽职调查（未取得材料列入未覆盖范围，严禁写“未发现问题”）
  - [`legal-opinion.md`](references/legal-opinion.md) —— 正式法律意见书（审阅文件锁定、显式假设与保留条件）

### 2. 高保真交付物模板 (8 个)
位于 [`templates/`](templates/) 目录，与 12 个 [`schemas/`](schemas/) 强类型约束严格一一对应：
- `executive-brief.md`（管理层决策简报） ｜ `legal-memo.md`（法务备忘录）
- `contract-review.md`（合同审查意见表） ｜ `risk-matrix.md`（风险全景矩阵）
- `evidence-matrix.md`（证据矩阵） ｜ `legal-opinion.md`（正式法律意见书）
- `action-plan.md`（落地执行计划） ｜ `message.md`（对外/对内直接可发送文本）

### 3. 端到端实战案例库 (4 套)
位于 [`examples/`](examples/) 目录，包含完整输入、路由门禁记录与交付物：
- [`01-contract-review/`](examples/01-contract-review/) —— 150万元技术采购合同审查（含 [HTML 报表](examples/01-contract-review/report.html)）
- [`02-trade-secret/`](examples/02-trade-secret/) —— 离职算法主管下载代码维权（含 [HTML 报表](examples/02-trade-secret/report.html)）
- [`03-labor/`](examples/03-labor/) —— 考核不合格直接辞退合规与 2N 测算
- [`04-quick/`](examples/04-quick/) —— 合同未写日期仅盖章效力（Lane A 极简作答）

---

## 📊 自动化评测与三档对照实验

本系统在 [`evals/`](evals/) 下内置了覆盖 9 大类场景的 14 个标准评测用例与离线规则检测器：

| 对照档位 | 配置说明 | Layer 1 一票否决通过率 | M2 虚拟案号违规率 | Layer 2 综合得分 | 商业七问完备率 |
|---|---|---:|---:|---:|---:|
| **Baseline-0** | 裸模型直接提问 | 20.0% | 60.0% | 42.5 分 | 30.0% |
| **Baseline-1** | 资深中国律师单体 Prompt (400字) | 50.0% | 40.0% | 64.0 分 | 60.0% |
| **China Legal OS** | 完整工作流 + 四道 Gate + Schema | **100.0%** | **0.0% (绝对禁令)** | **88.0 分** | **100.0%** |

---

## ⚠️ 局限与免责声明

1. **默认未核验模式（`RETRIEVAL_MODE: none`）**：本系统依赖模型知识库，所有法条条号标注为〔条号未核验〕，案例均以检索指引形式呈现。接入外部权威数据库后可平滑切换。
2. **不替代执业律师**：系统生成内容供企业内部工作参考，重大商事交易、诉讼策略与刑事/监管合规事项，须经公司法务负责人复核或聘请专业执业律师出具正式意见。
3. **法域范围**：v0.1 当前仅覆盖中华人民共和国大陆地区（不含港澳台及涉外法域）。

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。
