# 案例 02：商业秘密维权 — 路由分流与门禁触发记录

## 1. Triage 与事实分类
- `our_side`: 原用人单位 / 商业秘密权利人 — `Confirmed`
- `counterparty`: 离职员工李某及新竞争对手公司 — `Confirmed`
- `matter_type`: 商业秘密侵害、劳动合同违约、不正当竞争
- `confirmed_facts`:
  - 存在李某签署的《保密协议》与《离职承诺书》
  - IT 日志证实其在离职前非正常时间下载 80GB 核心代码包
- `alleged_facts`:
  - 新竞争对手公司是否已实际使用该算法（目前无直接证据，属 Alleged）
- `missing_critical`:
  - 核心算法是否具有独创性/秘密性的技术鉴定意见（待出具）

---

## 2. 路由判定（Router）
```
primary   : trade-secret
secondary : [labor, competition]
lane      : C (重大事项 / 高风险 / 强制 Evidence Matrix / 强制 Red Team)
reason    : 核心算法资产外流，涉及离职员工违约与新雇主不正当竞争，面临证据灭失风险，需启动紧急取证与刑事/民事多元维权。
```

---

## 3. 四道 Gate 门禁通过判定

| Gate | 触发时机 | 检查项与判定结果 | 动作 |
|---|---|---|---|
| **G1 事实分类闸** | 分析前 | 区分下载行为（已证实）与实际使用行为（未证实），未直接推定新雇主已侵权 | ✅ PASS |
| **G2 法源闸** | 结论前 | 引用反法第9条、第17条，刑法第219条〔条号未核验〕；输出人民法院案例库检索指引，无自产案号 | ✅ PASS |
| **G3 证据闸** | 定稿前 | 对三要件分配举证责任，明确保密措施证据充分，但新雇主使用证据薄弱，结论分层定性 | ✅ PASS |
| **G4 交付闸** | 交付前 | 交付 Executive Brief、Evidence Matrix、Action Plan（含 24h 紧急取证）与待核验清单 | ✅ PASS |
