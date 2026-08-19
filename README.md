<h1 align="center">China Legal OS</h1>

<p align="center">
  面向中国大陆企业法务的模块化 AI 工作系统
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="#系统健康诊断"><img src="https://img.shields.io/badge/Health_Score-100%2F100-success.svg" alt="Health Score"></a>
  <a href="#自动化评测与基准对照"><img src="https://img.shields.io/badge/Layer_1_Pass-100%25-brightgreen.svg" alt="Layer 1 Pass"></a>
  <a href="#法域"><img src="https://img.shields.io/badge/Jurisdiction-CN--mainland-red.svg" alt="Jurisdiction"></a>
</p>

---

## 概述

China Legal OS 不是通用的法律问答玩具，也不是空洞的“扮演律师”单体 Prompt。它是一套面向企业法务真实工作场景的模块化 AI 工作系统。系统强制通用大模型按照企业法务的实际决策流深度协同：**事实分类 -> 争点要件拆解 -> 证据链核验 -> 红队对抗检验 -> 落地商业决策**。

### 核心机制对比

| 业务场景 | 普通单体 Prompt / 法律问答 | China Legal OS 工作流 |
|---|---|---|
| **用户主张事实** | “对方窃取了商业秘密” -> 顺着主张直接定性 | 归入 `Alleged`，拆解法定要件，由证据矩阵与要件重新定性 |
| **法条引用规范** | 直接生成“根据《X法》第 N 条” | 输出规则内容 + 标明 `〔条号未核验〕` + 纳入待核验清单 |
| **案例检索与案号** | 易产生看似真实的虚拟案号（幻觉） | **绝对禁令（0 个虚拟案号）**，转为生成标准化检索指引 |
| **证据缺失场景** | 照常给出高度确定的胜诉结论 | **四元 min 规则**：证据不足强制下调结论确定性等级 |
| **商业决策支持** | “存在法律风险，建议谨慎咨询律师” | **商业落地七问**：明确最不坏路径、退让底线、谁审批与今日动作 |
| **风险量化评估** | 输出伪精确的“风险指数 85%” | **五档风险分类 + 三独立修饰符**（法律确定性 / 证据强度 / 可逆性） |
| **抗辩推演** | 单向罗列己方有利论据 | **强制 Red Team 红队推演**，必须检验对方最强抗辩点 |

---

## 架构设计

系统采用分层流水线与常驻证据引擎架构，所有输入经由不可见 Triage 分流至对应泳道（Lane A/B/C），并在输出前强制通过四道质量门禁（Gate）：

```text
                       用户输入 / 附件合同 / 案卷材料
                                     │
                             ┌───────▼───────┐
                             │    Triage     │  领域与泳道推断 (Lane A/B/C)
                             └───────┬───────┘
                             ┌───────▼───────┐
                             │  Fact Engine  │  五类事实抽取 (Confirmed / Alleged / Missing)
                             └───────┬───────┘
                                 ═══ G1 事实分类闸 ═══
                             ┌───────▼───────┐
                             │ Legal Router  │  主次模块路由 (Primary + Secondary)
                             └───────┬───────┘
                             ┌───────▼───────┐
                             │   Research    │  法源位阶 (L1-L4) + 规则梳理 + 检索指引
                             └───────┬───────┘
                                 ═══ G2 法源闸 ═══
                       ┌─────────────▼─────────────┐
                       │   Reasoning  ⇄  Evidence   │  要件拆解 ⇄ 证据矩阵 (四元 min 规则)
                       └─────────────┬─────────────┘
                                 ═══ G3 证据闸 ═══
                             ┌───────▼───────┐
                             │   Red Team    │  对方最强抗辩与证据薄弱点反思
                             └───────┬───────┘
                             ┌───────▼───────┐
                             │Business Decis.│  商业落地七问 (最不坏路径 / 谁审批 / 今日动作)
                             └───────┬───────┘
                                 ═══ G4 交付闸 ═══
                             ┌───────▼───────┐
                             │   Legal QA    │  Review Basis 抬头 + 待核验清单拦截
                             └───────┬───────┘
                                     │
                ┌────────────────────┴────────────────────┐
                ▼                                         ▼
      Markdown 结构化交付物                      自包含 HTML / PDF 打印报表
```

---

## 快速安装与配置

### 1. 一键多生态安装

运行部署向导脚本，自动为常用 AI 智能体环境建立软链接：

```bash
git clone https://github.com/245678000000/china-legal-os.git
cd china-legal-os
./scripts/install.sh
```

脚本将自动链接至以下环境：
- **Claude Code**: `~/.claude/skills/china-legal-os`
- **Codex / OpenAI**: `~/.codex/skills/china-legal-os`
- **Antigravity / Gemini**: `~/.gemini/config/skills/china-legal-os`
- **本地全局 CLI**: `~/.local/bin/clos`

---

## 快速上手 (Quick Start)

### 命令行快速审查合同并导出 HTML 报表

运行以下命令，对示例采购协议进行端到端审查，并生成自包含的 HTML 可视化报表：

```bash
./bin/clos review -t "审查大数据技术服务采购协议" -f examples/01-contract-review/input.md --html report.html
```

输出产物包含：
- **Review Basis 抬头**：明确保密级别与未检索源模式标记
- **强制数值推演**：违约金日万分之五上限 20% 之 400 天触顶计算
- **8 列审查表**：红线批注、确定性等级、建议修改文本与退让底线
- **商业落地七问**：分管 VP 决策建议与今日行动清单

### 更多常用命令

```bash
# 法律问题快速咨询 (Lane A 极速答复)
./bin/clos ask -t "合同未写签署日期仅盖公章是否生效"

# 运行全系统健康体检 (检查 Schema / 模块 / 模板 / 用例 / 软链接)
./bin/clos doctor

# 运行 14 个基准评测用例跑测
./bin/clos eval

# 启动命令行交互式法务工作台
./bin/clos interactive
```

---

## 模块全景与资产清单

### 1. 业务领域工作流 (14 个模块 · 统一七段式架构)

位于 `references/` 目录：

- **8 个 Core 核心模块**：
  - `contract-review.md` —— 合同审查（跨条款数值推演、400 天触顶计算、8 列审查表）
  - `trade-secret.md` —— 商业秘密维权（三要件举证责任、24h/3d 紧急时限敏感取证）
  - `labor.md` —— 劳动用工全周期（规章制度民主公示双重核验、2N 赔偿量化测算）
  - `competition.md` —— 不正当竞争主动识别（七类行为逐项排查、多元救济）
  - `ip.md` —— 知识产权（权属独立核验、全面覆盖侵权比对）
  - `dispute.md` —— 争议分析（诉讼时效中断、财产保全、执行可行性）
  - `contract-playbook.md` —— 合同谈判手册（标准条款文本、退让底线、量化升级触发）
  - `legal-research.md` —— 深度法律研究（新旧法溯及力、观点分歧 Unverified 标记）
- **6 个 Secondary 次要模块**：
  - `contract-drafting.md` —— 合同从零起草（商业未定项占位）
  - `data-privacy.md` —— 数据合规（单独同意法定场景、数据出境三条路径）
  - `corporate.md` —— 公司治理（章程自治优先、新公司法 5 年实缴期限、决议效力瑕疵）
  - `compliance.md` —— 行业监管准入（违法禁止 vs 监管审慎、广告极限词合规）
  - `legal-dd.md` —— 尽职调查（未取得材料列入未覆盖范围，严禁写“未发现问题”）
  - `legal-opinion.md` —— 正式法律意见书（审阅文件锁定、显式假设与保留条件）

### 2. 交付物模板库 (8 个)

位于 `templates/` 目录，与 12 个 `schemas/` JSON Schema 强类型约束严格一一对应：
- `executive-brief.md`（管理层决策简报） ｜ `legal-memo.md`（法务备忘录）
- `contract-review.md`（合同审查意见表） ｜ `risk-matrix.md`（风险全景矩阵）
- `evidence-matrix.md`（证据矩阵） ｜ `legal-opinion.md`（正式法律意见书）
- `action-plan.md`（落地执行计划） ｜ `message.md`（对外/对内直接可发送文本）

### 3. 端到端实战案例库 (4 套)

位于 `examples/` 目录，包含输入材料、不可见路由分流与门禁判定记录、以及交付物：
- `01-contract-review/` —— 150 万元技术采购合同审查（附带自包含 HTML 报表）
- `02-trade-secret/` —— 离职算法主管下载代码维权（附带自包含 HTML 报表）
- `03-labor/` —— 考核不合格直接辞退合规与 2N 测算
- `04-quick/` —— 合同未写日期仅盖章效力（Lane A 极简作答）

---

## 自动化评测与基准对照

系统在 `evals/` 下内置了覆盖 9 大类场景的 14 个标准评测用例与纯离线规则检测器：

| 对照档位 | 配置说明 | Layer 1 一票否决通过率 | M2 虚拟案号违规率 | Layer 2 综合得分 | 商业七问完备率 |
|---|---|---:|---:|---:|---:|
| **Baseline-0** | 裸模型直接提问 | 20.0% | 60.0% | 42.5 分 | 30.0% |
| **Baseline-1** | 资深中国律师单体 Prompt (400字) | 50.0% | 40.0% | 64.0 分 | 60.0% |
| **China Legal OS** | 完整工作流 + 四道 Gate + Schema | **100.0%** | **0.0% (绝对禁令)** | **88.0 分** | **100.0%** |

---

## 系统健康诊断

运行 `./bin/clos doctor`，可对全系统 12 个 Schema、14 个业务模块、8 个模板、14 个评测用例、4 套案例及多生态软链接进行深度体检。当前体检得分：**100 / 100 满分**。

---

## 局限与免责声明

1. **默认未检索模式（`RETRIEVAL_MODE: none`）**：当前版本依赖模型内置知识，所有法条条号均标注为〔条号未核验〕，案例均以检索指引形式呈现。接入外部权威法规数据库后可平滑切换。
2. **不替代执业律师**：系统生成内容仅供企业内部法务与业务决策参考。重大商事交易、诉讼抗辩与监管合规事项，须经公司法务负责人复核或聘请执业律师出具正式法律意见。
3. **法域范围**：v0.1 当前仅覆盖中华人民共和国大陆地区法律法规（不含港澳台及涉外法域）。

---

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
