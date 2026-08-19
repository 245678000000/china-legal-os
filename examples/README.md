# China Legal OS — 真实任务与端到端交付物范例

本目录包含 4 套不同业务场景、不同泳道（Lane）的端到端真实输入与高保真交付样例。每个案例均完整记录了**输入材料、不可见路由分流与门禁判定记录、以及标准化交付物组合**。

---

## 案例索引表

| 案例编号与目录 | 业务场景 | 泳道 | 交付物组合 | 核心考察亮点 |
|---|---|:---:|---|---|
| [`01-contract-review/`](01-contract-review/) | 150万元技术采购协议审查 | **Lane B** | `Contract Review` + `Executive Brief` | 400 天违约金触顶推演、知识产权归属让渡驳回、责任上限穿透、可直接复制的替换条款 |
| [`02-trade-secret/`](02-trade-secret/) | 算法负责人离职下载代码维权 | **Lane C** | `Executive Brief` + `Evidence Matrix` + `Action Plan` | 多路由分流、商业秘密三要件举证责任、**24h 紧急取证倒计时**、刑民交叉策略 |
| [`03-labor/`](03-labor/) | 员工考核 D 拟单方辞退合规 | **Lane B** | `Legal Memo` + `Message` + `Action Plan` | 规章制度效力核验、法定培训调岗前置程序、**2N 赔偿精准量化**、协商离职面谈话术 |
| [`04-quick/`](04-quick/) | 合同未写日期仅盖公章效力 | **Lane A** | 直接对话回答（3-10 行） | **不写厚重文件、不套格式**，极速响应 + 法源依据 + 1 个关键 Caveat |

---

## 案例结构说明

每个案例目录包含三个标准文件：
1. `input.md`：用户原始提问与提供的附件合同/证据材料片段。
2. `routing.md`：Triage 事实抽取、主次模块路由（Primary / Secondary / Lane）与 G1~G4 四道门禁通过记录。
3. `output.md`：系统严格按照 JSON Schema 与 Templates 规范生成的交付物（对内法务、对外业务或呈报管理层）。
