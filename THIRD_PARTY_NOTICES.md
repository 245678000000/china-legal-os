# Third Party Notices

China Legal OS 的架构受下列开源项目启发。本文件逐项记录：借鉴了什么、是否存在直接复制、以及各自的许可状态。

**总原则**
1. 优先重新表达与重新设计，不做多仓库拼贴
2. 借鉴 architecture / workflow / prompt pattern / schema / eval methodology，不复制受版权保护的具体文本
3. 无 License 的仓库只借鉴思想（思想不受版权保护），逐字重写
4. 下表"是否直接复制"一栏，**当前全部为「否」**

**核查基线**：2026-08-19，全部仓库实际克隆或按文件拉取后阅读。研究记录见 `docs/ARCHITECTURE_REPORT.md`。

---

## 1. Yuzzyuk / marketing-os

- **来源**：https://github.com/Yuzzyuk/marketing-os
- **License**：MIT — Copyright (c) 2026 Marketing OS contributors
- **借鉴内容**：SKILL.md 作为纯 Router 的分层方式；references 按任务动态加载的 Progressive Disclosure；honesty spine 作为独立章节并声明适用于全部模块；chaining 显式列出常见链路并要求携带上游结论；外置 context 文件（`brand-context.md`）在缺失时降级而非中断
- **是否直接复制**：**否**。路由表、模块清单、honesty 条目、chaining 链路全部为法务领域重新设计
- **对应改造**：`Router → Specialist → Deliverable` 改为 `Legal Router → Legal Specialist → Legal Deliverable`，并在其前后各插入一层营销场景不需要的结构（Fact Engine + G1，QA + G4）；`brand-context.md` → `company/company-legal-context.md`

## 2. SenryLee / legal-prompts

- **来源**：https://github.com/SenryLee/legal-prompts
- **License**：MIT — Copyright (c) 2024 SenryLee
- **借鉴内容**：六段式 Prompt 骨架（任务目标 / 角色设定 / 输入要求 / 分析框架 / 输出格式 / 特别说明）；输入要求再分「必须提供 / 建议补充 / 立场确认机制」的做法；把信息来源写进分析框架而非留给模型自由发挥
- **是否直接复制**：**否**。未复制其 252 个 Prompt 中的任何正文
- **对应改造**：六段式抽象为七段模块规格（增加 `Gates`）；「立场确认机制」提升为全局 Fact Engine 的 `our_side` 必填字段（且是唯一允许阻塞式提问的字段），不再由每个 Prompt 各问一次

## 3. anthropics / knowledge-work-plugins（legal 插件）

- **来源**：https://github.com/anthropics/knowledge-work-plugins（`legal/`）
- **License**：Apache-2.0
- **借鉴内容**：Playbook 三段式 Preferred Position / Acceptable Range / Escalation Trigger；GREEN/YELLOW/RED 偏离分级且每级绑定动作；Tier 1 Must-have / Tier 2 Should-have / Tier 3 Concession 的谈判优先级框架；"读完整份合同再标问题，条款之间相互作用"的要求；Playbook 缺失时标注 Review Basis 的做法；Severity × Likelihood 风险矩阵
- **是否直接复制**：**否**。未复制其 SKILL.md 文本、条款指引正文或输出模板
- **对应改造**：三段式的 Preferred Position 要求写成**可直接插入的中文条款文本**；Escalation Trigger 绑定中国企业的实际审批链（E1-E5）；GREEN/YELLOW/RED 增加第四类 **BLACK**（法律强制性规定禁止 / 约定无效）——这是中国法下必要的独立性质判断，不是程度判断；Severity × Likelihood 仅作内部推导，输出为五档 + 三修饰符，不输出分数

## 4. pa1nrui1 / legal-skills

- **来源**：https://github.com/pa1nrui1/legal-skills
- **License**：MIT — Copyright (c) 2026 Legal Skills Contributors
- **借鉴内容**：硬闸门（Hard Gate）机制——正式交付物必须先完成分类，未过闸门不得写正文；固定门禁词表，使闸门执行情况可被检测；来源标签体系；冲突处理协议（暴露冲突 / 标明来源 / 不静默选择一方）；"不得只拦截后停止"的失败兜底原则；事项隔离
- **是否直接复制**：**否**。Gate 结构、词表、标签体系均重新设计并大幅收敛
- **对应改造**：其 7 类正式交付强制链路（含飞书、图片、DOCX trackRevisions 等实现细节）对企业法务 v0.1 过重，收敛为 4 个 Gate（G1 事实分类 / G2 法源 / G3 证据 / G4 交付）；12 个来源标签收敛为 6 个；固定词表重新拟定为 6 个中文 Gate 词以便正则检测

## 5. judicialmind / awesome-legal-agent-templates

- **来源**：https://github.com/judicialmind/awesome-legal-agent-templates
- **License**：MIT — Copyright (c) 2026 JudicialMind.ai
- **借鉴内容**：模板作为完整可执行规格的字段结构（inputs + validation / retrieval / output JSON Schema / human_review / tests）；`human_review` 用 `confidence_field` + `review_if_confidence_in` 使人工复核可程序判定；每个模板自带断言式测试；`VERIFICATION.md` 对失败的诚实归类方式
- **是否直接复制**：**否**。未复制其 205 个模板的任何 system_prompt、schema 或测试数据
- **对应改造**：`human_review` 改造为 `escalation`——不只回答"是否需要复核"，而是"需要谁批、触发条件、需要什么材料、时限"；`jurisdiction: [US]` → `[CN-mainland]`；断言从 `keys_present` 扩展为否定断言（如"合同未约定准据法时 `governing_law_found` 必须为 null"）

## 6. vivy-yi / Greater-China-Legal ⚠️

- **来源**：https://github.com/vivy-yi/Greater-China-Legal
- **License**：**无 LICENSE 文件 —— 保留所有权利**
- **借鉴内容**：**仅思想，逐字重写**。① 法域可插拔（`LEGAL_FRAMES/` 按法域分文件）② Pre-flight Citation Check——引用前先验证检索源是否真的在响应，未连通则明确告知 ③ 禁止 promotion——不得因为引用"看起来对"就把未验证标为已验证 ④ Currency Trigger——生效日期、监管口径等必须联网 ⑤ 法律推理原子能力可跨场景复用的思路
- **是否直接复制**：**否**。因该仓库无 License，未复制任何行文本；上述机制在 `references/source-policy.md` 与 `references/legal-reasoning.md` 中重新表述与重新设计
- **对应改造**：法域可插拔保留为 `references/jurisdictions/`，但 v0.1 只实装大陆，其余法域声明超范围；其 37 个原子推理 Skill 收敛为 8 个共享推理原语放在单个文件中
- **反面借鉴**：该仓库将法规清单内联进 Prompt，且其中存在明显的条文编号讹误。本项目据此确立 `jurisdictions/cn-mainland.md` **不放法条正文**的规则（见 `docs/ARCHITECTURE_REPORT.md` §B4）

## 7. Daknniel-0881 / qulv-china-legal-counsel-skill

- **来源**：https://github.com/Daknniel-0881/qulv-china-legal-counsel-skill
- **License**：MIT — Copyright (c) 2026 Suze
- **借鉴内容**：分层法源优先级；Citation Verification 的 PASS / WARN / FAIL 三态及各自的纠正动作；把 hallucination traps 作为仓库内一等资产；scoring rubric 中的 **Automatic failure** 列表（编造法条/案号直接判负，不参与打分）；强制升级清单；`agents/openai.yaml` 的跨平台适配层形态
- **是否直接复制**：**否**。法源层级、rubric、陷阱用例、升级清单均重新设计
- **对应改造**：七级法源压缩为 L1-L4 四级，并与「核验状态」正交拆分（这是原仓库没有区分的）；Automatic failure 升级为 Eval 的 Layer 1 十条一票否决；强制升级清单绑定 E1-E5 审批链

## 8. evan66547 / Contract-Reviewer-Agent-Eval

- **来源**：https://github.com/evan66547/Contract-Reviewer-Agent-Eval
- **License**：MIT — Copyright (c) 2026 evan66547
- **借鉴内容**：多层能力对照实验的方法形态（裸模型 / 人设 Prompt / Agent 架构 用同一批用例横向评测）；output schema 中的 `citation_verified` + `confidence_degrade` 字段设计；合同审查必须做**跨条款数值推演**的洞察；README 顶部的 Compliance Disclaimer 写法
- **是否直接复制**：**否**。未复制其 25 个测试用例、Agent Prompt 或评分脚本
- **对应改造**：`citation_verified` 布尔升级为三态 `verification: verified/unverified/contradicted` 并与法源等级正交；分层对照实验作为 `evals/BASELINES.md` 的方法；数值推演固化为 `contract-review` 的强制计算项（`numeric_checks`，schema 中 `minItems: 1`）
- **明确不借鉴**：其 v1.2 的"defensive perfection"战斗姿态与 LLM-judge 中"写得越狠越完美分数越高"的评分导向（理由见 `docs/ARCHITECTURE_REPORT.md` §B2）；其自评分数不作为任何结论依据

---

## 学术基准（仅借鉴评测方法论，不使用其数据集）

| 名称 | 出处 | 借鉴 |
|---|---|---|
| **LegalBench** | arXiv 2308.11462 | 162 任务 / 6 类法律推理的分层方式，以及把法学界描述推理的框架映射到评测任务的做法 |
| **LawBench** | arXiv 2309.16289 | 中文法律能力按「记忆 / 理解 / 应用」三层认知分级 |
| **PLawBench** | arXiv 2601.16669 | 每题配专家撰写的 rubric（850 题 / 约 12,500 条 rubric item）的细颗粒评测方式 |

三者均未使用其数据、题目或评分脚本。`evals/RUBRIC.md` 的 rubric item 结构受 PLawBench 启发，内容为本项目自建。

---

## 本项目

China Legal OS 以 MIT 许可发布。

若后续引入上述任一项目的**具体文本**，必须：① 在本文件中把"是否直接复制"改为「是」并写明范围 ② 保留其版权与许可声明 ③ Apache-2.0 来源另需标注改动。
