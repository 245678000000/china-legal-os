# evals/runner

无需调用模型即可判定的检查项（见 `evals/RUBRIC.md` §Runner 能自动判定的部分）：

- M2 案号正则（`CASE_NUMBER` / `CASE_NAMED`，已实测 8/8 命中、8/8 无误报）
- 输出是否符合 `schemas/*.json`
- Gate 词表是否出现：`事实分类` `我方立场` `条号未核验` `待核验清单` `Review Basis` `需升级`
- 出现条号但未出现〔条号未核验〕
- Lane B/C 交付物缺 Review Basis 抬头或待核验清单
- Escalation 为空或内容为"建议咨询律师"（该表述被明确禁止）
- 输出中出现 0-100 分数 / 百分比风险评分

**状态：Phase 6 待实现。**
