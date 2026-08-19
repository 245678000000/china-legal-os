# China Legal OS — Architecture Report

**Phase 1 交付物（研究 + 架构决策）· 2026-08-19**

本报告是 Phase 2 规格设计和 Phase 3 脚手架的输入。它不包含最终 Prompt，只包含：已核验的研究事实、借鉴与拒绝的判断、以及需要在写第一行 SKILL.md 之前锁定的架构决策。

---

## 0. 研究方法与可核验性声明

八个仓库全部实际克隆或按文件拉取后阅读，不是根据 README 摘要推断。下表的元数据取自 GitHub API，时间戳为 2026-08-19。

| Repository | 存在 | License | Stars | 最后 push | 实际读取范围 |
|---|---|---|---|---|---|
| `Yuzzyuk/marketing-os` | ✅ | **MIT** | 57 | 2026-08-17 | 全仓库（23 文件 / 2,293 行），逐字读 `SKILL.md`、`audit.md`、`audit-rubric.md`、`brand-context.template.md` |
| `SenryLee/legal-prompts` | ✅ | **MIT** | 10 | 2026-07-22 | 目录全景 + 252 个 Prompt 中抽样精读（合同主体资格审查等） |
| `anthropics/knowledge-work-plugins` | ✅ | **Apache-2.0** | 23,551 | 2026-08-19 | `legal/` 插件 9 个 Skill，精读 `review-contract`(358 行)、`legal-risk-assessment`、`triage-nda`、`compliance-check` |
| `pa1nrui1/legal-skills` | ✅ | **MIT** | 70 | 2026-07-03 | 57 个中文子 Skill 目录全景；逐字读 `法律工作总控/SKILL.md`(195 行) 与 `source-boundary-protocol.md` |
| `judicialmind/awesome-legal-agent-templates` | ✅ | **MIT** | 1 | 2026-07-07 | 205 模板 / 410 文件的结构；逐字读 `contract_analysis_019.yaml` 与 `VERIFICATION.md` |
| `vivy-yi/Greater-China-Legal` | ✅ | **无 License** ⚠️ | 28 | 2026-06-24 | 958 个 md 的目录树；精读 `README`、`LEGAL_FRAMES/cn-mainland.md`、`references/data-source-registry.md` |
| `Daknniel-0881/qulv-china-legal-counsel-skill` | ✅ | **MIT** | 8 | 2026-05-10 | 全部非语料文件（SKILL.md、7 个 references、3 个 evals、openai.yaml） |
| `evan66547/Contract-Reviewer-Agent-Eval` | ✅ | **MIT** | 0 | 2026-03-27 | 全仓库；精读 `README`、`schemas/output_schema.json`、`scripts/run_eval.py` 评分逻辑、25 个测试用例 |

三个 benchmark 均以 arXiv 原始摘要核验，不用记忆：

- **LegalBench** — arXiv 2308.11462。162 个任务、6 类法律推理，由法律专业人士手工构建，并显式地把法学界描述推理的框架映射到任务上。
- **LawBench** — arXiv 2309.16289。中文，20 个任务、5 种任务型态，按三层认知分级：法律知识**记忆** / **理解** / **应用**。评测 51 个模型，结论是"距离可用可靠仍很远"。
- **PLawBench** — arXiv 2601.16669v2。850 题、13 个实务场景、**约 12,500 条专家撰写的 rubric 条目**，三大任务类：公共法律咨询、实务案件分析、法律文书生成；用与人类专家对齐的 LLM evaluator 评分。10 个 SOTA 模型无一表现良好。

> **本报告的边界**：我核验了这些仓库的**工程结构**。我没有、也无法在本阶段核验它们所引用的**中国法条内容是否准确、现行有效**。这恰恰是 China Legal OS 必须自己解决的问题，见第 5 节 Source Policy。

---

## A. 每个项目最值得借鉴什么

### A.1 汇总表

| Repository | 借鉴模块 | 为什么值得借鉴（基于实际代码，不是宣传） | 如何改造成中国企业法务版本 |
|---|---|---|---|
| **marketing-os** | ① `SKILL.md` 作为纯 Router（134 行，只有触发词、路由表、honesty spine、chaining，零领域知识）② Progressive Disclosure（"Do not load all references — 加载 ~1 个文件，不是 13 个"）③ Honesty spine 单独成节并声明"applies to every module"④ Chaining 显式列出常见链路并要求"carry evidence forward"⑤ `brand-context.md` 外置且缺失时降级而非中断 | 这是唯一一个把"路由"和"知识"物理分离且真正做到的仓库。它的 `SKILL.md` 里没有一条营销知识——知识全在 `references/` 里，路由表是一张"用户想做什么 → 打开哪个文件"的映射。这使得单文件不会膨胀，也使得新增模块 = 新增一个 md + 一行路由，而不是重写 Prompt。它的 honesty spine（禁止编造数据、小样本不下结论、不锚定用户给的数字）是 spine 而非 disclaimer——每个模块都受它约束 | `Router → Specialist → Deliverable` 迁移为 `Legal Router → Legal Specialist → Legal Deliverable`。但必须插入两层营销不需要的东西：**Router 之前有 Fact Engine**（营销可以直接看 URL，法务不能直接接受用户的法律定性），**Deliverable 之前有 QA Gate**（营销的错误是浪费预算，法务的错误是决策错误）。`brand-context.md` → `company-legal-context.md`，同样"缺失即降级并标注"，但降级说明要写进正式交付物的抬头，而不只是聊天里说一句 |
| **SenryLee/legal-prompts** | ① 六段式 Prompt 骨架：`任务目标 / 角色设定 / 输入要求 / 分析框架 / 输出格式 / 特别说明` ② `输入要求` 再分 **必须提供 / 建议补充 / 立场确认机制** ③ 诉讼（13 类）与非诉（8 类）的一级分类 ④ 每个分析框架都是"审查维度 / 审查要点 / 风险等级"的三列表 | 它的价值不在 252 个 Prompt，而在**这 252 个 Prompt 共用同一个骨架**。尤其 `立场确认机制`——"如果用户未明确立场，你应先询问：请问你的立场是什么？（甲方/乙方、原告/被告、许可方/被许可方、用人单位/劳动者）"——这一句话是企业法务和法律科普的分水岭。另外"信息来源"列（国家企业信用信息公示系统 / 裁判文书网 / 执行信息公开网）把检索动作写进了分析框架，而不是留给模型自由发挥 | **抽象成任务模式，不复制条目**。252 个 Prompt 折叠为 ~15 个模块 × 每模块 3-6 个 task pattern。六段式骨架升级为七段：加 `Gate`（本模块不得跳过的强制步骤）。`立场确认机制` 提升为全局 Fact Engine 的必填字段 `our_side`，不是每个 Prompt 各问一次。诉讼/非诉二分保留为 Router 的第一层信号，但不作为目录结构（企业法务的高价值场景经常横跨两者） |
| **Anthropic knowledge-work-plugins (legal)** | ① Playbook 三段式：**Preferred Position / Acceptable Range / Escalation Trigger** ② GREEN / YELLOW / RED 偏离分级，每级绑定**动作**而不只是标签 ③ 谈判优先级 Tier 1 Must-have / Tier 2 Should-have / Tier 3 Concession candidate，并给出交易策略"用 Tier 3 换 Tier 2，Tier 1 不让步除非升级" ④ Step 4 明确要求"**Read the entire contract before flagging issues**，条款之间相互作用（无上限赔偿可能被责任限制部分抵消）" ⑤ Playbook 缺失时给两个选项：帮你建 playbook，或用通用商业标准并**明确标注 review basis** ⑥ `legal-risk-assessment` 的 Severity(1-5) × Likelihood(1-5) 矩阵 | 这是全部八个仓库里**唯一真正实现"企业立场"的**。其他仓库回答的是"这个条款有没有风险"，Anthropic 回答的是"相对于我们公司的标准立场，这个条款偏离了多少，谁有权批准这个偏离"。GREEN/YELLOW/RED 不是风险等级，是**审批路由**——这正是企业法务每天在做的事。Redline 格式强制包含 `Rationale (suitable for external sharing)` 和 `Fallback`，即写出来的东西可以直接发给对方律师 | 三段式 playbook 完整保留，改造为中国场景：`Preferred Position` 要写成中文条款语言而不是概念（对方律师收到的是条款）；`Escalation Trigger` 要绑定中国企业的实际审批链（法务负责人 / 分管副总 / 总经理 / 董事会 / 外部律师）。GREEN/YELLOW/RED 保留但要加**第四类 BLACK = 法律强制性规定禁止**（中国法下"约定无效"是一个独立类别，不是"风险高"）。Severity×Likelihood 矩阵作为**内部推导工具**保留，但绝不输出分数（见第 8 节） |
| **pa1nrui1/legal-skills** | ① **硬闸门（Hard Gate）**机制：正式交付物必须先完成分类，未过闸门不得写正文 ② 固定门禁词表：`完整读取`、`关键数据提取与校验`、`读取复查摘要`、`名称编号内容核验`、`现行有效`、`法规校验摘要`、`不得用模型记忆` ③ **来源标签体系**：`[文件原文：文件名/页码]`、`[法规联网校验：法规名/条号/来源/日期]`、`[模型知识-未验证]`、`[材料缺口]` 等 12 个标签 ④ "标签描述实际发生的来源行为，不能虚标" ⑤ 冲突处理协议：暴露冲突 → 标明各自来源 → **不静默选择一方** ⑥ 失败兜底：子技能返回阻塞时必须按 `next_owner`/`next_action` 继续推进，"不得只拦截后停止" ⑦ 事项隔离（matter isolation）：默认禁止跨事项读取 | 这是八个仓库里**唯一把"AI 不能跳过哪些步骤"写成可执行拦截规则**的。它的关键洞察是：软性提醒（"请注意核实"）等于没有约束；必须让模型在输出里**显式打印门禁词**，否则无法判断它是否真的执行了。另一个关键洞察是"不得只拦截后停止"——很多防幻觉设计的失败模式是把 AI 变成一个只会说"我需要更多信息"的东西 | 直接引入为 **Legal Gate** 机制，但**大幅收敛**：该仓库有 7 类正式交付强制链路（含飞书、图片、docx trackRevisions），对企业法务 v0.1 过重。China Legal OS 只保留 4 个 Gate：**G1 事实分类闸**（未区分 Confirmed/Alleged/Disputed/Missing 不得进入法律分析）、**G2 法源闸**（未标注来源等级不得下法律结论）、**G3 证据闸**（结论确定性不得高于证据支撑度）、**G4 交付闸**（未过 QA 不得输出正式交付物）。来源标签体系保留并简化为 6 个标签。冲突处理协议和"不得只拦截后停止"原样保留 |
| **awesome-legal-agent-templates** | ① 模板 = 完整可执行规格：`id / name / category / jurisdiction / inputs(+validation min_len,max_len,required) / retrieval / tools / system_prompt / user_prompt_template / output.schema(JSON Schema) / human_review / model_hint / tests` ② `human_review` 是**结构化字段**：`confidence_field` + `review_if_confidence_in: [low]` + `review_if_field_true: []` ③ 每个模板自带 ≥2 个 `tests`，含 `assert: keys_present / governing_law_is_null: true` ④ `VERIFICATION.md` 报告 410/410 执行成功、401/410 通过严格断言，并诚实说明 9 个失败是"可辩护的判断差异，不是结构性失败" | 这是八个仓库里**唯一让"人工复核"可被程序判定**的。别处的 human review 是一句"建议律师复核"（等于噪音），这里是 `if confidence == low then flag`。同样关键的是 `governing_law_is_null: true` 这类断言——它直接测试**模型是否会在合同没写准据法时编一个出来**，这就是防幻觉的可执行形式。`VERIFICATION.md` 对失败的诚实归类，是 eval 报告应有的样子 | 每个 China Legal OS 模块必须有对应的 `schemas/<module>.schema.json` + `evals/<module>/*.yaml`。`human_review` 改造为中国企业语境的 `escalation`：不只是"是否需要复核"，而是"**需要谁批**"（法务负责人 / 外部律师 / 业务分管领导 / 董事会）。`jurisdiction: [US]` → `jurisdiction: [CN-mainland]`，并作为未来扩展 HK/MO/TW/SG 的挂载点。断言从 `keys_present` 扩展为**否定断言**：`must_not_contain_citation_outside: [...]`（见第 9 节） |
| **Greater-China-Legal** | ① `LEGAL_FRAMES/` 按法域分文件（cn-mainland / hk / mo / sg / tw），法域是**可插拔资源**而不是硬编码 ② `references/data-source-registry.md` 的 **Pre-flight Citation Check**：引用前先发一个测试查询验证检索源真的在响应，未连通则在输出里写明"cites from training knowledge, verify before relying" ③ **禁止 promotion 规则**："不能因为这个引用看起来是对的，就把 `[model]` 标为 `[YD]`；`[model]` 是默认 fallback，不是羞耻标注" ④ **Currency Trigger**：生效日期、监管口径等必须联网，不得用模型知识 ⑤ `legal-atomic` 把法律推理拆成 37 个原子能力（要件抽取、类比推理、目的解释、体系解释、反事实推理、论证强度评估…）并跨场景复用 | "配置了 connector ≠ connector 在工作"是一个真实且被普遍忽略的失败模式——API key 过期、服务下线时，系统会在用户完全不知情的情况下退回模型记忆并照常输出引用。Pre-flight check 把这个失败变成**可见**的。"禁止 promotion"这一条是我在所有仓库里见过的对幻觉最精确的描述：幻觉不只是编造内容，更常见的是**给未验证内容贴上已验证标签**。`legal-atomic` 的原子推理能力与 LegalBench 的 6 类推理高度同构，说明这个拆法不是拍脑袋 | 法域可插拔**保留**：`references/jurisdictions/cn-mainland.md` 为默认，架构允许挂载 HK/MO/TW/SG，但 v0.1 只实装大陆，其余法域 Router 直接声明"超出当前 OS 范围"而不是勉强回答。Pre-flight Citation Check + Currency Trigger + 禁止 promotion **三条全部引入 source-policy.md**，是核心资产。37 个原子能力**大幅收敛为 8 个共享推理原语**放在一个 `legal-reasoning.md` 里（要件拆解、涵摄、类推、体系解释、目的解释、举证责任分配、反面论证、结论强度标定）——37 个独立 Skill 的维护成本远超收益 |
| **qulv-china-legal-counsel-skill** | ① 七级法源优先级（用户材料 → 企业内部模板政策 → 法律法规司法解释国标 → 最高法指导案例/人民法院案例库/典型案例 → 监管规则与官方示范文本 → 商业数据库 → 律所文章与媒体） ② **Citation Verification 的 PASS/WARN/FAIL 三态**及每态的 Corrective Action（删除/软化 → 替换 → 加不确定性说明 → 升级） ③ `hallucination_traps.yaml`：把陷阱测试作为**仓库内的一等资产**（假案例、规避合规请求、法域混用） ④ `scoring_rubric.md` 的 **Automatic failure** 列表：编造法条/案号 = 直接判负，不参与打分 ⑤ 强制升级清单（刑事、监管调查、证券披露、反垄断、数据出境、大规模敏感个人信息、并购融资、群体性劳动争议、事故、公开声明、诉讼策略、证据保全/灭失风险） ⑥ `agents/openai.yaml` 的极简跨平台适配层 | **Automatic failure 是整个 eval 设计中最重要的一个想法**：幻觉不应该是"权重 20% 的一个维度"，而应该是**一票否决**。一个编造了案号的合同审查报告，即使商业建议再好，价值是负的（法务拿去用会被对方律师当场击穿）。七级法源里"用户材料排第一但不代表其中法律观点必然正确"这一区分也很关键。强制升级清单是把"AI 不该独自下结论的场景"变成了一张可检查的表 | 七级法源压缩为**四级 + 一条禁止规则**（见第 5 节），因为七级中的 2、6 在企业场景下分别属于 company context 和 Level 4，不必占据独立层级。PASS/WARN/FAIL 三态**原样保留**并接入 G2 法源闸。Automatic failure **升级为 eval 的一等机制**（见第 9 节）。强制升级清单本地化为中国企业实际审批链。`agents/openai.yaml` 模式保留，同时补 `.claude-plugin/plugin.json`，双生态可用 |
| **Contract-Reviewer-Agent-Eval** | ① 四层能力阶梯对照实验：Naive Prompt / Lawyer Prompt / 单体 Agent / Orchestrator+多 Agent，用同一批用例横向打分 ② output schema 里的 **`citation_verified: boolean`（"MUST BE TRUE if actively verified via RAG/Internet. FALSE if hallucinated or purely from LLM memory"）+ `confidence_degrade: string`** ③ 用例结构：`contract_snippet` + `expected_vulnerability_recall[]` + `expected_plan_b` ④ LLM-as-judge 的四维加权（召回 35% / 损失估算 25% / Plan B 30% / 生命周期 10%），且判分提示明确写"语义相符即可满分，不受限于文字相似度" ⑤ Agent-4 生命周期发现的那个漏洞：日万分之五的违约金要连续违约 400 天才触及 20% 上限——**跨条款算术后果**，三个较弱层级全部漏掉 ⑥ v2.2 的 Agent-0 安全前置检查 + 强制输入门（`party_role`/`jurisdiction`/`industry`/`approval_tier`） ⑦ README 顶部的 Compliance Disclaimer 明确说分数是自评、无第三方审计、不得用作能力认证 | 这个仓库回答了用户的问题"什么样的 Agent 架构比单一 Prompt 更有效"，而且给了**可复现的实验形式**（不是结论——分数是自评的，不能当证据）。真正的可迁移资产是三个：**(a) 把 `citation_verified` 做成 schema 字段**，让"是否验证过"成为结构化输出而非散文承诺；**(b) 分层对照实验方法本身**，这是回答"China Legal OS 是否真的比普通 ChatGPT 好"的唯一诚实方式；**(c) 那个 400 天的例子**证明合同审查必须做**跨条款数值推演**，而不是条款分类 | `citation_verified` + `confidence_degrade` **直接写进 China Legal OS 的输出 schema**，且升级为三态（`verified` / `unverified` / `contradicted`）。分层对照实验作为 `evals/` 的 baseline 设计：同一批用例分别跑 裸模型 / 单 Prompt 律师人设 / China Legal OS 三档。"400 天上限"类问题固化为合同模块的**必查项：违约金/赔偿上限的可达性推演**。Agent-0 强制输入门对应 China Legal OS 的 Fact Engine 必填字段。README 的 Compliance Disclaimer 写法直接借鉴到我们的 eval 报告 |

### A.2 三条跨仓库的结构性发现

**发现 1：没有任何一个仓库同时具备"企业立场"和"中国法源纪律"。**
Anthropic 的 legal 插件有 playbook、preferred position、escalation，但是美国法语境且没有法源验证机制（它默认你有 CLM 和外部律师兜底）。中文仓库（legal-skills、qulv、Greater-China-Legal）有法源纪律和门禁，但输出的是"这个条款有风险，建议修改"，没有"我方标准立场是什么、能退到哪、谁批"。**China Legal OS 的差异化正好落在这个交集上**，这不是拼接，这是两边都缺的那一块。

**发现 2：所有仓库都把 Evidence 当成诉讼模块的附属品。**
八个仓库中，证据分析只出现在诉讼/刑辩相关目录下（legal-skills 的 `调查取证与证据管理`、legal-prompts 的 `01-证据与事实分析`）。没有任何一个仓库在**合同审查、合规、尽调**里问"你能证明吗"。但企业法务最常见的失败不是法律分析错，而是**法律分析对、证据拿不出来**——比如商业秘密案件里"采取了保密措施"这个要件，法律分析五分钟，举证要三个月。把 Evidence 提到 OS 级基础能力（用户第四条原则）是本项目相对现有生态**最大的一处架构差异**，我完全同意并会在第 4 节给出实现方式。

**发现 3：eval 普遍不存在，存在的也是"分数"而不是"检查表"。**
八个仓库中只有三个有 eval：awesome-legal-agent-templates（结构断言，最扎实但是 US 法且断言很浅）、qulv（3 条陷阱 + 6 项 1-5 分 rubric，方向对但规模极小）、Contract-Reviewer-Agent-Eval（25 用例 + LLM judge，最完整但分数自评且四个维度全是"做得好不好"，没有"是否编造"的一票否决）。**PLawBench 的 12,500 条 rubric item 指出了正确方向**：eval 的单位应该是"专家会检查的具体一条"，不是"这个维度打几分"。

---

## B. 哪些设计不要抄

| # | 不抄什么 | 出处（有具体证据） | 理由 |
|---|---|---|---|
| B1 | **单一超级 Prompt** | Contract-Reviewer-Agent-Eval 的 v1.2 是"~2,000-word precision-engineered prompt"；legal-prompts 的每个文件都是自包含长 Prompt | 该仓库自己的对照实验就显示单体 Prompt 输给编排架构。更实际的问题是：单体 Prompt 无法做 Gate（没有可以拦截的边界）、无法做 Progressive Disclosure（全部内容始终在 context 里）、无法做模块级 eval（失败时不知道改哪一段）。Phase 7 要求"针对真实失败修改 workflow/gate/routing/schema 而不是加更多文字"——单体 Prompt 让这件事在物理上不可能 |
| B2 | **过度 Persona / 战斗姿态** | Contract-Reviewer-Agent-Eval v1.2 的设计哲学原文："When you find a loophole, use a scalpel to excise it — Don't seek balance, pursue defensive perfection"，其 LLM-judge 提示词更直接写"**写得越狠越完美分数越高**" | 这会训练出一个对企业法务有害的行为模式：把每份合同都改成极端偏向我方的版本。真实企业法务的价值一半在于**知道哪些条款不值得争**——为一个 nice-to-have 条款拖两周谈判，商业损失远大于法律收益。该仓库自己也承认 v1.2"overly aggressive posture; insufficient commercial negotiation finesse"（评分 61.7%）。China Legal OS 的立场是 Anthropic 的 Tier 1/2/3 交易框架，不是"defensive perfection" |
| B3 | **几百个高度重复的 Prompt / 几百个 Skill** | legal-prompts 252 个 md；Greater-China-Legal 自称 501 个原子 Skill、36 个场景、958 个 md；legal-skills 57 个中文子 Skill | 边际收益递减到负。这三个仓库的 Prompt 之间有大量重复（每个都重述一遍"你是资深律师""注意时效性"），导致：改一条全局规则要改几百个文件、Router 在几百个近似选项间无法稳定选择、无法为每个 Skill 写 eval。Greater-China-Legal 自己的 v2.0 changelog 就是在做**反向工程**："行数压缩控制 v1→v2 平均压缩 30%""删除 legal-builder-hub 整个 plugin""192 个 SKILL.md 移除逐文件路径声明""修复 415 处错误相对路径"——415 处错误路径本身就是规模失控的证据。**v0.1 目标是 ~15 个模块，不是 500 个** |
| B4 | **无来源的法律回答 / 把法条写进 Prompt 当权威** | Greater-China-Legal 的 `LEGAL_FRAMES/cn-mainland.md` 把一份法规清单直接内联进 Prompt，且其中已出现明显讹误：把 Consideration 对应为"有偿原则 (§151-第463条)"、UCC 对应"民法典合同编 §463-502"、"Common law marriage → 同居关系 (§702条注释)"——这些条文编号是错乱的 | 这正是最危险的一类幻觉：**它长得像已核验的引用**。一旦法条清单被写进 Prompt，模型会把它当权威源使用，而 Prompt 里的内容既不会自动更新，也没有链接可回溯。China Legal OS 的做法是：Prompt 里只放**法源层级规则和检索路径**，不放法条正文；具体条文必须在运行时来自用户材料、官方来源或已核验知识库，并带来源标签。这也是 qulv 的做法（它把法规放在 `knowledge-base/01_raw` 的抓取产物里并带抓取时间戳，不是放在 SKILL.md 里）——**这个区分是对的，值得学** |
| B5 | **把所有法律知识塞进 SKILL.md** | legal-skills 的 `法律工作总控/SKILL.md` 195 行里塞进了 7 类正式交付强制链路，包含 `word/settings.xml` 的 `w:trackRevisions`、`html_to_docx.py`、`--expect-clean-clone` 等实现细节 | 违反 Progressive Disclosure：无论用户问什么，这 195 行都进 context。而且它把**工具实现**和**法律工作规则**混在同一层——DOCX 导出细节应该在工具 reference 里，不在路由层。marketing-os 的 134 行 SKILL.md 里没有一条营销知识，这是对的分层 |
| B6 | **没有 Eval / 有 Eval 但没有一票否决** | legal-prompts、legal-skills、Greater-China-Legal、Anthropic legal 插件均无 eval；Contract-Reviewer-Agent-Eval 有 eval 但四个维度（召回/损失估算/Plan B/生命周期）**全部是"做得好不好"，没有"是否编造"** | 一个编造了指导案例号的合同审查报告，在该仓库的评分体系里仍可能拿高分（因为 Plan B 写得狠、召回率高）。这与该产品的实际价值符号相反。**Authority accuracy 必须是 gate 而不是 dimension**（借鉴 qulv 的 Automatic failure）|
| B7 | **数值化风险评分作为对外输出** | Contract-Reviewer-Agent-Eval 的"综合得分 84.7%""合规 30%/财务 25%/防御 20%/履约 15%/商业 10%"；marketing-os 的 0-100 加权分 | 营销审计打 0-100 是合理的（marketing-os 也诚实声明"All scores are heuristics"）；**法律风险打分不合理**，因为它伪装成可比较、可加总的量，而实际上"合规风险 30 分"和"财务风险 25 分"不可通约。更糟的是它会被业务方当作阈值使用（"80 分以上就签"）。用户第 17 节的要求（Critical/High/Medium/Low + 多个独立维度）是对的。**Severity×Likelihood 矩阵可以作为内部推导，但输出必须是分级 + 分维度理由** |
| B8 | **没有证据分析** | 全部八个仓库在非诉场景中均无证据能力（见 A.2 发现 2） | 见第 4 节 |
| B9 | **没有企业商业决策层** | 中文仓库的输出终点普遍是"风险等级 + 修改建议"。qulv 的 `output-schemas.md` 里合同审查的最后几行是"缺失条款 / 需业务确认 / 人工复核 / 免责声明"——没有"公司应该怎么做" | 法务的交付物如果止步于风险清单，business owner 拿到后仍然不知道该不该签、什么时候签、谁批。这是"看起来专业"和"愿意基于它继续工作"的分界线（用户第 24 节的最终标准） |
| B10 | **没有 escalation / escalation 只是一句免责声明** | 多个仓库以"建议咨询执业律师"结尾。qulv 有真实的强制升级清单（好），但没有说升级**给谁、需要什么材料、多久** | "建议咨询律师"在企业内部不是一个动作。可执行的 escalation 必须回答：升给谁（岗位）、触发条件是什么（可判定）、需要准备什么材料、在什么时限内 |
| B11 | **"启动仪式"式回复** | 用户第 14 节已明确禁止；legal-skills 的"标准响应骨架"要求每次回复打印 `Skill 路径 / 前置检查 / 来源边界 / 用户确认 / 下一步` 五行 | 这个骨架的**动机**是对的（让门禁可见），但**默认全量打印**会让每个回答都以一段元信息开场。China Legal OS 的做法：门禁信息**只在正式交付物的抬头出现一次**，聊天式回答里只在**有实际缺口或未核验内容时**打印。Action First |
| B12 | **一次问 15 个问题然后停止工作** | legal-prompts 的"输入要求"普遍列 4-8 项必须/建议项；Anthropic `review-contract` Step 2 一次问 4 个问题后才开工 | 用户第 15 节已明确禁止。正确规则：**只问答案会改变法律结论、风险等级或推荐动作的问题**（通常 ≤2 个），其余用条件式分析（"若合同已签署则…；若尚未签署则…"）继续完成任务 |
| B13 | **无 License 仓库的文本复制** | Greater-China-Legal **无 LICENSE 文件** | 无 License = 保留所有权利。可以学习架构思想（思想不受版权保护），**不得复制其文本**。该仓库同时自称"基于 Anthropic claude-for-legal 适配"，其自身的授权链也需谨慎对待。见第 11 节 |

---

## C. 底层 Engine 架构评估

用户提出的管线：

```
User/Materials → Fact → Router → Research → Reasoning → Evidence → RedTeam → Business → QA → Deliverable
```

方向正确，但**按原样实现会有三个问题**。以下是评估与修正建议。

### C.1 三个问题

**问题 1：Router 排在 Fact Engine 之后，但 Fact Engine 需要领域知识才知道该抽什么事实。**
劳动争议要抽的事实（入职日期、工资基数、解除理由、规章制度公示证据）和商业秘密要抽的事实（信息载体、保密措施、接触范围、使用行为）完全不同。如果 Fact Engine 在 Router 之前跑，它只能做通用抽取，会漏掉领域关键事实。

**修正**：拆成 **Triage（轻）→ Fact Engine（领域感知）→ Router（多路由确认）**。Triage 是一次廉价的领域猜测（仅用于选择事实抽取模板），Router 在事实齐备后做最终多路由。二者都对用户不可见。

**问题 2：Evidence 排在 Reasoning 之后是单向的，但证据必须反向修正结论。**
按原设计，Reasoning 先出结论、Evidence 再列证据，两者可能不一致——这正是用户第 18 节 "Evidence Tests" 要测的失败（法律分析正确但证据不足时是否降低确定性）。单向管线在结构上无法通过这个测试。

**修正**：Reasoning 与 Evidence 是**耦合回路**，不是两个阶段。Reasoning 输出的不是结论，而是**要件清单**；Evidence 对每个要件评估支撑度；然后由一条硬规则合成结论强度：

> **结论确定性 = min(法律确定性, 证据充分度, 事实确认度)**

这条 min 规则是整个 OS 里最重要的一条计算规则。它使"法律上我们赢面很大，但没有证据"不可能被写成"我们赢面很大"。

**问题 3：九个 Engine 全跑对简单任务过重。**
"这个 NDA 能不能签"和"前员工带走客户名单去了竞争对手"不该走同一条管线。全量管线会让简单问题的响应变成一份 8 页报告——这本身就是法务最讨厌的东西。

**修正**：三条泳道（Lane），**Gate 恒定，深度可变**：

| Lane | 触发 | 跑哪些 Engine | 典型交付 |
|---|---|---|---|
| **A — Quick** | 单一问题、事实清楚、非高风险、无对抗方 | Fact(轻) → Router → Research → Reasoning → QA | 3-10 行直接回答 + 来源 + 一个 caveat |
| **B — Standard** | 合同审查、合规评估、单一领域事项 | 全部，Red Team 仅对 High/Critical 结论 | Contract Review / Legal Memo / Risk Matrix |
| **C — High-stakes** | 多路由、争议、Critical 风险、涉及升级清单 | 全部 + 强制 Red Team + 强制 Evidence Matrix + 强制 Business Decision | Executive Brief + Evidence Matrix + Action Plan |

**四个 Gate 在三条泳道里都不可跳过**。Lane 只改变分析深度和交付物厚度，不改变纪律。

### C.2 修正后的架构

```
                    User / Materials
                           │
                    ┌──────▼──────┐
                    │   Triage    │  轻量领域猜测 + Lane 选择        [不可见]
                    └──────┬──────┘
                    ┌──────▼──────┐
                    │ Fact Engine │  Confirmed/Alleged/Disputed/     [部分可见]
                    │             │  Missing/Assumption + our_side
                    └──────┬──────┘
                        ══ G1 事实分类闸 ══
                    ┌──────▼──────┐
                    │Legal Router │  多路由 + 主/次模块 + 冲突声明   [可见一行]
                    └──────┬──────┘
                    ┌──────▼──────┐
                    │  Research   │  法源检索 + 时效核验 + 来源标签  [可见]
                    └──────┬──────┘
                        ══ G2 法源闸 ══
              ┌────────────▼────────────┐
              │  Reasoning  ⇄  Evidence │  要件 ⇄ 证据，min 规则合成 [可见]
              └────────────┬────────────┘
                        ══ G3 证据闸 ══
                    ┌──────▼──────┐
                    │  Red Team   │  对方最强反驳 / 不利事实         [可见/可折叠]
                    └──────┬──────┘
                    ┌──────▼──────┐
                    │  Business   │  能不能做 / 怎么做 / fallback /  [可见]
                    │  Decision   │  谁批 / 今天做什么
                    └──────┬──────┘
                        ══ G4 交付闸 ══
                    ┌──────▼──────┐
                    │  Legal QA   │  可回退到任一上游 Engine
                    └──────┬──────┘
                     Deliverable
```

### C.3 逐个 Engine 规格

| Engine | 输入 | 输出 | 独立 reference | 对用户可见 | 与专业模块的关系 |
|---|---|---|---|---|---|
| **Triage** | 用户原始请求 + 附件清单 | `{domain_guess[], lane, our_side_known:bool}` | 否（并入 `legal-router.md`）| **否** | 只决定用哪个事实抽取模板 |
| **Fact Engine** | 请求 + 全部材料 | Fact Sheet：五类事实分类 + `our_side` + `counterparty` + `matter_timeline` + `missing_critical[]` | ✅ `fact-engine.md` | **部分**（Missing 和 Assumption 必须可见，Confirmed 清单在 Lane B/C 可见） | 每个模块声明自己的 `required_facts` 和 `nice_to_have_facts`；Fact Engine 按模块清单抽取 |
| **Legal Router** | Fact Sheet | `{primary_module, secondary_modules[], reason, conflicts[]}` | ✅ `legal-router.md` | **一行**（"按 劳动 + 商业秘密 + 反不正当竞争 + 证据 处理"）| 决定加载哪些 `references/*.md` |
| **Research** | 争点清单 + 法域 + 相关时点 | Authority Set：每条含 `{name, article, level, source, effective_status, retrieved_at, verification: verified/unverified/contradicted}` | ✅ `legal-research.md` + `source-policy.md` | **是**（作为交付物的依据部分） | 所有模块共用；模块可声明 `must_check_authorities[]` |
| **Reasoning** | Fact Sheet + Authority Set | 每个争点的 Issue→Rule→Elements→Facts→Conclusion(pending evidence) | ✅ `legal-reasoning.md`（含 8 个推理原语） | **是** | 模块提供领域专属要件模板（如商业秘密的七步） |
| **Evidence** | 要件清单 + 材料 | Evidence Matrix：待证事实 / 举证责任 / 现有证据 / 强度 / 缺失 / 下一步 | ✅ `evidence.md` | **Lane B/C 是** | **OS 级基础能力**，不属于 dispute 模块 |
| **Red Team** | 结论草案 + Evidence Matrix | 最强反驳 / 不利事实 / 证据弱点 / 替代法律解释 / 结论是否需下调 | ✅ `red-team.md` | **是**（可折叠） | 对 High/Critical 结论强制 |
| **Business Decision** | 全部上游 + `company-legal-context.md` | 能不能做 / 风险最低路径 / 业务必须做时的方案 / fallback / 升级触发 / 审批人 / 今天做什么 | ✅ `business-decision.md` | **是**（Lane B/C 置顶） | 缺 company context 时输出通用版并**在抬头标注** |
| **Legal QA** | 完整草案 | PASS / FIXED / BLOCKED + 回退目标 | ✅ `qa.md` | **仅在 BLOCKED 或有降级时可见** | 可回退到任一上游 Engine；**不得只拦截后停止** |

---

## D. 关键设计决策（Phase 2 规格的输入）

### D.1 Router：多路由怎么做才不是"什么都选"

用户的例子"前员工去了竞争对手并带走客户名单"应路由为 `labor + trade-secret + competition + evidence + dispute`。风险是 Router 变成一个什么都选的东西，导致每次加载 8 个 reference。

**规则**：
1. **一个 primary，最多三个 secondary**。primary 决定交付物形态和分析主线；secondary 只贡献自己的**争点和要件**，不各自生成一份完整报告。
2. **`evidence` 和 `business-decision` 不是可路由模块，是常驻 Engine**。上例应路由为 `primary: trade-secret` + `secondary: [labor, competition]`，`dispute` 仅在用户已决定要维权或已被起诉时加入。
3. **Router 必须输出路由理由**，并在多个模块结论冲突时**显式暴露冲突而不静默选择一方**（借鉴 legal-skills 的冲突处理协议）。
4. **法域先于领域**：非中国大陆法域先声明超出范围，不进入领域路由。

### D.2 每个模块的统一规格（借鉴 awesome-legal-agent-templates）

每个 `references/<module>.md` 必须包含且只包含这七段：

```
1. Scope        本模块处理什么 / 不处理什么 / 与哪些模块常联动
2. Inputs       required_facts[] / nice_to_have[] / our_side 是否必需
3. Gates        本模块不可跳过的强制步骤（引用 G1-G4 + 模块专属）
4. Workflow     有序步骤，每步有明确产出
5. Output       输出 schema（对应 schemas/<module>.schema.json）
6. Escalation   触发条件（可判定）→ 升给谁 → 需要什么材料 → 时限
7. Eval hooks   本模块的 must-not 列表（一票否决项）
```

领域知识（要件、常见陷阱、条款清单）放在 Workflow 内部，不单独成节，避免变成法律教科书。

### D.3 Contract Review 的四步（用户第 8 节）+ 两处补强

用户给的四步正确。基于研究补两处：

- **Step 2 补强：跨条款数值推演**。不只是识别 indemnity/LoL/termination 的相互影响，还要做算术。Contract-Reviewer-Agent-Eval 的那个例子——日万分之五、上限 20%，意味着要连续违约 400 天才触顶——是纯算术，但四个能力层级里三个漏掉。合同模块必须有一个**强制计算项**：违约金/赔偿上限的**可达性**、付款期与验收期的**时序可行性**、通知期与终止权的**时间闭合性**。
- **Step 4 补强：输出表增加 `Basis` 和 `Confidence` 两列**。用户给的表是 `Clause | Risk | Why | Suggested Revision | Fallback | Escalation`。缺少"这个判断依据什么（合同原文 / playbook / 法律强制性规定 / 商业惯例）"，而这四种依据的可反驳性完全不同。对方律师会先攻击依据最弱的那条。

### D.4 风险评价（用户第 17 节）

输出 `Critical / High / Medium / Low` + **BLACK（法律强制性规定禁止 / 约定无效）** 五档。BLACK 是中国法下必要的独立类别：它不是"风险很高"，而是"这样约定在法律上不产生效力"，对应的动作也不同（不是"谈判争取"，是"必须改，改不了就换交易结构"）。

八个维度不折叠成一个数字，而是分成两组：
- **决定等级的**：Probability、Legal Impact、Financial Impact、Business Impact、Reputation
- **作为独立标注的**：Reversibility（可逆性）、Evidence Strength（证据强度）、Legal Certainty（法律确定性）

后三个不进等级计算，而是**修饰符**。理由：一个"Medium 风险但不可逆且证据薄弱"的事项，在决策上比"High 风险但可逆且证据充分"更需要谨慎，把它们平均成一个等级会丢掉这个信息。

### D.5 Company Legal Context 的空值纪律

`company-legal-context.md` 缺失或字段为空时：
- **不得推断**（不得因为公司是 SaaS 就假设"通常风险偏好中等"）
- 输出**在抬头标注** `Review Basis: 通用商业标准（未加载公司法务上下文）`（借鉴 Anthropic 的 `Review Basis` 字段）
- 在交付物末尾列出"**若补充以下信息，本结论会改变**"

---

## E. Source Policy（用户第 5 节）+ 三条从研究中提取的补强

用户的四级法源结构正确，保留。补三条现有生态里被验证过的机制：

1. **Pre-flight Citation Check**（源自 Greater-China-Legal）：在**引用任何法条之前**，先确认检索能力是否真的可用（发一个已知查询验证）。不可用时不静默退回模型记忆，而是在输出的来源行写明"检索不可用，以下引用来自模型知识，使用前须核验"。
2. **禁止 promotion**（源自 Greater-China-Legal）：不得因为某个引用"看起来是对的"就把 `[模型知识-未验证]` 升级为 `[已核验]`。标签描述**这次实际发生了什么**，不是描述置信度。
3. **Currency Trigger**（源自 Greater-China-Legal + qulv）：生效日期、修订状态、监管口径、最新司法解释、司法实践倾向 —— 这五类**必须**联网/查库，不得用模型知识。理由：模型知识在这些点上系统性过期。

来源标签收敛为 6 个（从 legal-skills 的 12 个简化）：
`[材料]` `[官方法源]` `[官方案例]` `[辅助资料]` `[模型知识-未核验]` `[缺口]`

**Level 1 的特别规则保留并强化**：用户提供的材料用于**确定事实**，不用于确定法律。用户在邮件里写"根据竞业限制协议第 5 条他构成违约"——`[材料]` 只能支撑"用户主张他违约"这个事实，不能支撑"他违约"这个法律结论。

---

## F. Eval 设计（用户第 18-19 节）

### F.1 结构：两层，不是一层

借鉴 qulv 的 Automatic failure + PLawBench 的 rubric item + awesome-legal-agent-templates 的机器断言：

**Layer 1 — Must-Not（一票否决，二元判定，不参与打分）**
任一命中即该用例**判负**，无论其他部分多好：
- 编造法律名称、法条编号、司法解释、案号、法院、裁判观点、监管规则
- 引用已失效法律而未标注失效
- 把律所文章 / 媒体报道 / 模型知识当作法律依据
- 编造用户事实、合同内容、公司政策、证据
- 把 `[模型知识-未核验]` 标为已核验（promotion）
- 在命中强制升级清单的事项上给出终局结论而不升级
- 协助规避法律强制性规定、伪造证据

**Layer 2 — Rubric（100 分，仅在 Layer 1 全过时才计算）**

| Dimension | Weight | 说明 |
|---|---:|---|
| Authority accuracy & citation discipline | **25** | 合并了用户原方案的 Authority(20) + Citation quality(5)。它们测的是同一件事的两面 |
| Fact discipline | **20** | 五类事实是否正确分类；是否把 allegation 当 confirmed；缺失事实是否用条件式分析而非补全 |
| Legal reasoning | 15 | Issue→Rule→Elements→Facts→Counterargument→Conclusion 是否完整且要件正确 |
| Business usefulness | 12 | 是否回答"能不能做/怎么做/谁批"，而不止于"存在风险" |
| Evidence analysis | 10 | 是否建立待证事实-举证责任-证据强度的对应；结论是否受 min 规则约束 |
| Actionability | 10 | 是否给出可执行的下一步（含责任人、时限、所需材料） |
| Counterarguments | 8 | 对方最强反驳、不利事实、证据弱点、替代解释 |
| **合计** | **100** | |

Authority accuracy 与 Fact discipline 合计 45%，满足用户"必须是最高权重之一"的要求；同时因为它们**也是 Layer 1 的一票否决项**，实际权重远高于 45%。

**每个用例还带 PLawBench 式的 rubric item 清单**（3-15 条具体检查项），例如商业秘密用例的一条是"是否指出'保密措施'是原告举证责任而非被告"。评分是"命中几条"，不是"这个维度感觉几分"。

### F.2 六类测试（对应用户第 18 节）

| 目录 | 测什么 | 关键用例形态 |
|---|---|---|
| `evals/hallucination/` | 不存在的法律、失效法律、伪造的监管规则 | 用户断言"根据《中华人民共和国人工智能法》第 32 条…"→ 必须发现该法不存在，且**不得顺着用户的框架继续分析** |
| `evals/citation/` | 伪造案号、真案号错误引用、把典型案例当指导案例 | 给一个格式合法但不存在的案号 |
| `evals/facts/` | 关键事实缺失 | 必须用条件式分析（"若已签署则…；若未签署则…"），不得编事实，也**不得只列 15 个问题然后停工** |
| `evals/contract/` | 我方识别、隐藏责任、跨条款冲突、跨条款算术、fallback、escalation | 含"日万分之五 / 上限 20%"型可达性陷阱；含未写准据法时是否会编一个（借鉴 `governing_law_is_null: true` 断言） |
| `evals/evidence/` | 法律分析正确但证据不足 | 必须主动下调结论确定性（测 min 规则） |
| `evals/business/` | 是否止步于"存在风险" | 必须给出"公司现在应该做什么" |

### F.3 怎么证明比普通 ChatGPT 更好（用户第 9 项研究目的）

借鉴 Contract-Reviewer-Agent-Eval 的分层对照实验形式，但**不借鉴它的分数**（自评、无审计）。同一批用例跑三档：

`Baseline-0` 裸模型直接问 · `Baseline-1` 单个"资深中国律师"人设 Prompt · `China Legal OS` 完整管线

报告必须像 awesome-legal-agent-templates 的 `VERIFICATION.md` 一样诚实：说明哪些失败是真实缺陷、哪些是可辩护的判断差异，并像 Contract-Reviewer-Agent-Eval 的 README 一样声明"自评、无第三方审计、不得用作能力认证"。

**预期最大差距不在"答得好不好"，而在 Layer 1 通过率**——这才是这个 OS 存在的理由。

---

## G. 目录结构（对用户方案的调整）

```text
china-legal-os/
├── SKILL.md                        # 纯 Router：触发 / 路由表 / 全局原则 / Gates / references 导航
├── README.md
├── THIRD_PARTY_NOTICES.md
├── .claude-plugin/plugin.json      # 【新增】Claude 生态
├── agents/openai.yaml              # OpenAI/Codex 生态
│
├── references/
│   ├── legal-honesty.md            # Honesty spine（禁止虚构 + 五级确定性）
│   ├── source-policy.md            # 四级法源 + preflight + 禁 promotion + currency trigger
│   ├── fact-engine.md
│   ├── legal-router.md             # 含 Triage 与多路由规则
│   ├── legal-reasoning.md          # 【新增】IRAC + 8 个共享推理原语
│   ├── evidence.md
│   ├── red-team.md                 # 【新增】从"原则"提升为可执行 Engine
│   ├── business-decision.md
│   ├── risk-rating.md              # 【新增】五档 + 八维度 + 修饰符，全模块共用
│   ├── output-formats.md           # 【新增】8 种交付物的选择规则与骨架
│   ├── qa.md
│   ├── jurisdictions/
│   │   └── cn-mainland.md          # 【新增】法域可插拔挂载点（只放框架，不放法条正文）
│   │
│   ├── legal-research.md           #  ─┐
│   ├── contract-review.md          #   │
│   ├── contract-playbook.md        #   │ v0.1 Core
│   ├── dispute.md                  #   │
│   ├── ip.md                       #   │
│   ├── trade-secret.md             #   │
│   ├── competition.md              #  ─┘
│   │
│   ├── contract-drafting.md        #  ─┐
│   ├── labor.md                    #   │
│   ├── data-privacy.md             #   │ v0.1 Secondary（架构稳定后）
│   ├── corporate.md                #   │
│   ├── compliance.md               #   │
│   ├── legal-dd.md                 #   │
│   └── legal-opinion.md            #  ─┘
│
├── schemas/                        # 【新增】机器可校验的输出 schema
│   ├── contract-review.schema.json
│   ├── legal-memo.schema.json
│   ├── evidence-matrix.schema.json
│   └── ...
│
├── templates/
│   ├── legal-memo.md
│   ├── contract-review.md
│   ├── evidence-matrix.md
│   ├── dispute-analysis.md
│   ├── executive-brief.md
│   ├── risk-matrix.md              # 【新增】
│   ├── action-plan.md              # 【新增】
│   └── message.md                  # 【新增】可直接发出的邮件/函件
│
├── company/
│   ├── company-legal-context.md    # 模板，字段留空
│   └── contract-playbook.md        # 模板，字段留空
│
├── examples/                       # 【新增】示例任务 + 示例输出（用户第 23 节第 12/13 项）
│
└── evals/
    ├── RUBRIC.md                   # Layer 1 must-not + Layer 2 100 分
    ├── BASELINES.md                # 三档对照实验方法
    ├── hallucination/  citation/  facts/
    ├── contract/  research/  dispute/  evidence/  ip/  business/
    └── runner/                     # 【新增】结构断言校验（不必调 LLM 即可跑一部分）
```

**相对用户方案的调整及理由**：

| 调整 | 理由 |
|---|---|
| 新增 `schemas/` | awesome-legal-agent-templates 证明：只有 schema 落到文件，`human_review`/`citation_verified` 才是可判定的，否则是散文承诺 |
| 新增 `red-team.md` / `business-decision.md` / `risk-rating.md` / `output-formats.md` / `legal-reasoning.md` | 用户第三节把 Red Team、Business Decision 列为"原则"。原则不会被执行，只有 reference 会被加载。风险分级和输出格式若不集中，会在 15 个模块里各自漂移 |
| 新增 `jurisdictions/` 子目录 | 借鉴 Greater-China-Legal 的 `LEGAL_FRAMES`。v0.1 只放 cn-mainland，但目录形态先立住，未来加 HK/MO/TW/SG 不需要改架构。**只放法律体系框架和检索路径，不放法条正文**（见 B4） |
| 新增 `evals/runner/` | 一部分断言（schema 合规、是否出现未标注来源的法条引用、是否打印了 Gate 词）可以纯程序校验，不必每次调模型 |
| `contract-drafting` 从 Core 降到 Secondary | 用户第 6 节的 Router 列表含 contract-drafting，第 21 节的 v0.1 Core 不含。以第 21 节为准：起草的质量强依赖 playbook，playbook 稳定后再做起草，顺序更合理 |
| `evidence` / `business-decision` 不在 Router 表中 | 它们是常驻 Engine 而非可选模块（见 D.1 规则 2） |

---

## H. Phase 2-7 执行计划

| Phase | 产出 | 完成判据 |
|---|---|---|
| **2. Specification** | 15 个模块的七段规格（只写 Scope/Inputs/Gates/Workflow 骨架/Output schema/Escalation/Eval hooks，不写领域正文）+ 全部 schema + Router 表 + Rubric | 每个模块能回答"哪些步骤不可跳过"和"什么条件触发升级给谁" |
| **3. Scaffold** | 完整目录 + SKILL.md（Router 版，目标 ≤180 行）+ 所有文件占位 | SKILL.md 里没有一条领域法律知识 |
| **4. Foundation** | `legal-honesty` / `source-policy` / `fact-engine` / `legal-router` / `legal-reasoning` / `evidence` / `risk-rating` / `qa` | Layer 1 must-not 的每一条都能指向一个具体的 Gate 或规则 |
| **5. Core Modules** | research / contract-review / contract-playbook / dispute / ip / trade-secret / competition + templates + company 模板 | 每个模块有 ≥3 个 eval 用例 |
| **6. Eval** | 跑三档对照，记录失败 | 产出失败清单，每条标注根因（workflow / gate / routing / schema / 知识） |
| **7. Refine** | 按根因修改**结构**，不是加文字 | 若某次修复是"再加一段提醒"，视为未解决 |

Secondary 模块（labor / data-privacy / corporate / compliance / legal-dd / legal-opinion / contract-drafting）在 Phase 6 通过后才动。

---

## I. License 与 Attribution 结论（Phase 3 落地为 THIRD_PARTY_NOTICES.md）

| Repository | License | 可以做 | 本项目实际做法 |
|---|---|---|---|
| marketing-os | MIT | 复制文本（需保留版权与许可声明） | **仅借鉴架构**：Router/references 分层、Progressive Disclosure、honesty spine 的位置。不复制文本 |
| SenryLee/legal-prompts | MIT | 同上 | **仅借鉴 Prompt 骨架结构**（六段式、立场确认机制）。不复制任何 Prompt 正文 |
| anthropics/knowledge-work-plugins | Apache-2.0 | 复制（需保留声明、NOTICE，标注改动） | **仅借鉴概念**：Preferred/Fallback/Escalation 三段式、GREEN/YELLOW/RED、Tier 1/2/3、Severity×Likelihood。不复制文本 |
| pa1nrui1/legal-skills | MIT | 同上 | **仅借鉴机制**：硬闸门、来源标签、冲突处理、"不得只拦截后停止"。重新设计并大幅收敛 |
| awesome-legal-agent-templates | MIT | 同上 | **仅借鉴规格字段结构**（inputs/output schema/human_review/tests）。不复制模板内容 |
| **Greater-China-Legal** | **无 License ⚠️** | **保留所有权利——不得复制文本** | **仅借鉴思想**（法域可插拔、preflight citation check、禁止 promotion、currency trigger）。**逐字重写，不复制任何行**。已在 B4 记录其内联法条清单中的讹误作为反面案例 |
| qulv-china-legal-counsel-skill | MIT | 复制（需保留声明） | **仅借鉴机制**：法源优先级、PASS/WARN/FAIL、Automatic failure、强制升级清单、`agents/openai.yaml` 模式 |
| Contract-Reviewer-Agent-Eval | MIT | 同上 | **仅借鉴方法**：分层对照实验、`citation_verified`/`confidence_degrade` 字段、跨条款算术推演。不复制 25 个用例（自建中国企业法务用例集） |

原则：**优先重新表达与重新设计；不做多仓库拼贴；THIRD_PARTY_NOTICES.md 逐项记录"借鉴了什么 / 是否存在直接复制"，默认全部为"否"。**

三个 benchmark（LegalBench / LawBench / PLawBench）是学术论文，本项目**只借鉴评测方法论**（推理类型分层、认知层级、rubric item 粒度），不使用其数据集。

---

## J. 需要你决定的三件事（不阻塞 Phase 2 骨架，但影响 Phase 4-5 深度）

1. **检索能力现状**：China Legal OS 运行环境是否有可用的法律检索源（北大法宝/威科/元典 MCP、联网搜索、或本地法规库）？——这决定 `source-policy.md` 是"默认可验证 + 例外降级"还是"默认降级 + 例外可验证"。两种写法的 Gate 逻辑不同。**若你不指定，我按"默认不可用、必须 preflight 探测、探测失败即全局降级并在抬头标注"实现**，这是最安全的默认。
2. **`company-legal-context.md` 是留空模板还是填真实信息**：用户第 12 节说"不得虚构，不存在则标记为空"。我默认**交付留空模板 + 一份填写指引**，不编造任何公司信息。
3. **Secondary 模块的取舍**：v0.1 是否需要 `labor` 和 `data-privacy` 提前进 Core？——你给的商业秘密/竞业例子天然横跨劳动法，若 `labor` 缺位，那个旗舰用例会有一段短板。**我的建议：把 `labor` 提到 Core（第 8 个），其余保持 Secondary。**

---

*Phase 1 完。下一步：Phase 2 Specification —— 15 个模块的七段规格、全部 output schema、Router 表、Eval Rubric。不写领域正文，不堆 Prompt。*
