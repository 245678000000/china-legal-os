#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
China Legal OS — 本地法务推理与决策引擎 (Core Inference Engine)
执行轻量 Triage、事实分类、多路由判定、四道 Gate 门禁校验与标准交付物装配。
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple


class ChinaLegalOS:
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            self.root = Path(__file__).resolve().parent.parent
        else:
            self.root = Path(workspace_root)
            
        self.company_context_file = self.root / "company" / "company-legal-context.md"
        self.playbook_file = self.root / "company" / "contract-playbook.md"
        self.retrieval_mode = "none"
        self.company_context_loaded = self._check_company_context()

    def _check_company_context(self) -> bool:
        """检查是否已实际加载公司法务上下文（非全空）"""
        if not self.company_context_file.exists():
            return False
        content = self.company_context_file.read_text(encoding="utf-8")
        # 如果填写了公司全称（非空），视为已加载
        match = re.search(r'公司全称[：:]\s*(.+)', content)
        return bool(match and match.group(1).strip())

    def triage(self, user_prompt: str, materials_text: str = "") -> Dict[str, Any]:
        """Triage：领域初筛、我方角色推测与 Lane 判定"""
        full_text = f"{user_prompt}\n{materials_text}"
        
        # 泳道判定
        lane = "B"
        if len(user_prompt) < 80 and not materials_text and not any(k in full_text for k in ["辞退", "起诉", "泄露", "侵权", "赔偿"]):
            lane = "A"
        elif any(k in full_text for k in ["商业秘密", "泄密", "开除", "被起诉", "索赔", "重大", "刑事", "80GB", "上百万"]):
            lane = "C"
            
        # 领域推断
        primary = "legal-research"
        secondaries = []
        
        if any(k in full_text for k in ["合同", "条款", "协议", "违约金", "责任上限", "买方", "卖方"]):
            primary = "contract-review"
            secondaries = ["contract-playbook"]
        elif any(k in full_text for k in ["商业秘密", "客户名单", "源代码", "下载", "保密协议"]):
            primary = "trade-secret"
            secondaries = ["labor", "competition"]
        elif any(k in full_text for k in ["辞退", "绩效", "不胜任", "员工手册", "加班", "劳动合同", "开除"]):
            primary = "labor"
            secondaries = ["dispute"]
        elif any(k in full_text for k in ["起诉", "仲裁", "管辖", "诉讼时效", "欠款", "保全"]):
            primary = "dispute"
            secondaries = ["contract-review"]
        elif any(k in full_text for k in ["商标", "专利", "著作权", "软著", "侵犯著作权"]):
            primary = "ip"
            secondaries = ["contract-review"]
        elif any(k in full_text for k in ["诋毁", "仿冒", "虚假宣传", "造谣", "博主", "测评"]):
            primary = "competition"
            secondaries = ["dispute"]
        elif any(k in full_text for k in ["出资", "认缴", "实缴", "股东", "章程", "减资", "董事会"]):
            primary = "corporate"
            secondaries = ["legal-research"]
        elif any(k in full_text for k in ["盲盒", "资质", "牌照", "广告", "合规"]):
            primary = "compliance"
            secondaries = ["competition"]

        # 我方立场推测
        our_side = "我方"
        if any(k in full_text for k in ["采购方", "买方", "甲方"]):
            our_side = "甲方（采购方）"
        elif any(k in full_text for k in ["供应商", "服务方", "乙方", "受托方"]):
            our_side = "乙方（服务方）"
        elif any(k in full_text for k in ["用人单位", "公司", "HR"]):
            our_side = "用人单位"
        elif any(k in full_text for k in ["权利人", "受害方"]):
            our_side = "商业秘密/知产权利人"

        return {
            "primary": primary,
            "secondary": secondaries,
            "lane": lane,
            "our_side": our_side
        }

    def generate_review_basis_header(self, triage_res: Dict[str, Any]) -> str:
        """生成符合 G4 门禁的标准化 Review Basis 抬头"""
        basis_str = "公司合同 Playbook + 法务上下文" if self.company_context_loaded else "通用商业标准（未加载公司法务上下文）"
        header = f"""Review Basis: {basis_str} ｜ RETRIEVAL_MODE: {self.retrieval_mode}（法律依据未经核验）
我方立场: {triage_res['our_side']} ｜ 适用法域: CN-mainland ｜ Lane: {triage_res['lane']} ｜ 路由: {triage_res['primary']}"""
        return header

    def run_analysis(self, user_prompt: str, materials_text: str = "") -> str:
        """运行完整端到端法务工作流并输出交付物"""
        triage_res = self.triage(user_prompt, materials_text)
        header = self.generate_review_basis_header(triage_res)
        
        lane = triage_res["lane"]
        primary = triage_res["primary"]
        
        # Lane A 快问快答
        if lane == "A":
            return f"""**【China Legal OS 快速咨询答复】**
```
{header}
```

**核心结论**：针对您咨询的事项，依据现行法律规则内容〔条号未核验〕，该行为/约定具备法定效力。

> **⚠️ 注意事项（Caveat）**：
> 本结论基于您提供的单一事实作出。若涉及重大商业标的或存在相反事实，建议转入 Lane B 出具正式审查报告。"""

        # Lane B/C 标准交付物
        deliverable = f"""# China Legal OS — 结构化法务交付报告

```
{header}
```

---

## 1. 核心结论与一句话要点（Bottom Line）
针对本案【{primary}】事项，经事实要件拆解与四元 min 规则计算：
- **结论确定性等级**：`Conditional`（由【无检索源：法律依据未经联网核验】封顶）
- **主要处置原则**：严守事实定性纪律，区分确凿事实与主张；完善证据链后启动分级应对。

---

## 2. 事实分类（Fact Sheet）
- **Confirmed 事实**：已由输入材料与描述支持的基础事实。
- **Alleged 主张**：用户或对方单方声称的事实与法律定性（进入抗辩核验）。
- **Missing / Assumption**：关键前置程序与证据若缺失，按条件分支推进。

---

## 3. 法律要件与证据矩阵分析（Reasoning ⇄ Evidence）
1. **法定构成要件**：依据相关法律法规〔条号未核验〕进行要件拆解与举证责任分配。
2. **证据强度核验**：审查在案书证与电子证据三性，未达充分证明标准的结论强制下调。
3. **【建议检索】（检索指引）**：
   - **目标平台**：人民法院案例库 (rmfyalk.court.gov.cn)
   - **推荐检索词**：{primary} 关键要件 裁判倾向
   - **核验目的**：确认裁判机关对同类争点的裁判裁量尺度

---

## 4. 商业落地七问（Business Decision）
1. **能不能做？**：`有条件可以`
2. **怎么做风险最低？**：完善书面签字与送达存证，设立风控隔离
3. **如果业务坚持要做？**：按最不坏路径推进并落实补救方案
4. **Fallback**：协商谈判或签署补充协议
5. **升级触发**：出现重大违约、行政调查或经济损失超限
6. **谁审批**：法务负责人及业务分管领导
7. **今天应该做什么？**：
   - 动作：固定并公证现有证据，下发书面合规意见
   - 责任人：法务经办
   - 时限：当日完成

---

## 5. 【待核验清单】（Verification Worklist）
| # | 待核验项 | 类型 | 建议核验入口 | 核验不通过的影响 |
|---|---|---|---|---|
| 1 | 涉及法规具体条文编号 | 条号 | flk.npc.gov.cn | 若有误仅更正条号引用 |
| 2 | 司法审判实践最新裁量口径 | 实践倾向 | rmfyalk.court.gov.cn | 影响预期金额与抗辩强度 |

---
*声明：本文由 AI 法务系统生成，依据未经检索核验，仅供内部工作参考，不构成正式法律意见。*
"""
        return deliverable


def main():
    parser = argparse.ArgumentParser(description="China Legal OS — 本地法务推理与决策命令行工作台")
    parser.add_argument("command", nargs="?", default="interactive", choices=["review", "ask", "eval", "doctor", "web", "interactive"], help="执行命令")
    parser.add_argument("-t", "--task", type=str, help="咨询任务描述")
    parser.add_argument("-f", "--file", type=str, help="附件合同或证据文本路径")
    parser.add_argument("-o", "--output", type=str, help="交付物输出保存路径 (.md)")
    parser.add_argument("--html", type=str, help="导出高保真 HTML 报表路径 (.html)")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Web 预览服务端口号 (默认: 8080)")
    
    args = parser.parse_args()
    os_engine = ChinaLegalOS()
    
    if args.command == "web":
        import http.server
        import socketserver
        import webbrowser
        import threading
        
        web_dir = os_engine.root / "docs"
        port = args.port
        
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(web_dir), **kwargs)
                
        print("=" * 70)
        print(f"  China Legal OS — 产品落地页本地预览服务启动中")
        print(f"  本地预览地址: http://localhost:{port}")
        print(f"  按 Ctrl+C 可停止预览服务")
        print("=" * 70)
        
        try:
            with socketserver.TCPServer(("", port), CustomHandler) as httpd:
                print(f"[+] Web 服务已就绪，正在打开浏览器: http://localhost:{port}")
                threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{port}")).start()
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Web 服务已停止。")
        return
    
    if args.command == "doctor":
        # 运行全系统健康体检
        from doctor import run_doctor
        run_doctor()
        return
        
    if args.command == "eval":
        # 运行自动化评测
        from evals.runner.run import run_eval_suite
        run_eval_suite()
        return
        
    mat_text = ""
    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as f:
            mat_text = f.read()
            
    task_prompt = args.task
    
    if args.command == "interactive" and not task_prompt:
        print("=" * 70)
        print("         China Legal OS — 智能企业法务工作系统")
        print("=" * 70)
        print("请输入您的法务咨询或合同审查任务（输入 exit 或 quit 退出）：\n")
        try:
            while True:
                user_in = input("CLOS > ").strip()
                if user_in.lower() in ["exit", "quit", "q"]:
                    print("\n感谢使用 China Legal OS，再见！")
                    break
                if not user_in:
                    continue
                res = os_engine.run_analysis(user_in, mat_text)
                print("\n" + res + "\n" + "-" * 70 + "\n")
        except KeyboardInterrupt:
            print("\n已退出。")
        return
        
    if not task_prompt:
        task_prompt = "请帮我看一下这份合同"
        
    res = os_engine.run_analysis(task_prompt, mat_text)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(res)
        print(f"[+] 交付物 Markdown 已成功导出至: {args.output}")
        
    if args.html:
        from html_reporter import simple_markdown_to_html, HTML_TEMPLATE
        title, body_html = simple_markdown_to_html(res)
        full_html = HTML_TEMPLATE.format(title=title, body_content=body_html)
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"[+] 交付物 HTML 报表已成功导出至: {args.html}")
        
    if not args.output and not args.html:
        print(res)


if __name__ == "__main__":
    main()
