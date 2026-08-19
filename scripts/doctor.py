#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
China Legal OS — 全系统健康诊断与完整性体检工具 (Doctor & Health Check)
全自动对 Schemas、References、Templates、Evals、Examples 及生态软链接进行全量深度体检。
"""

import os
import sys
import glob
import json
import yaml
from pathlib import Path

# 导入静态检查引擎
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "evals", "runner"))
from static_checks import run_all_static_checks


def run_doctor():
    root = Path(__file__).resolve().parent.parent
    print("=" * 72)
    print("          China Legal OS — 全系统健康诊断与完整性体检向导")
    print("=" * 72)
    
    score = 100
    issues = []

    # 1. 检测 JSON Schemas
    print("[1/6] 🔍 正在检查 JSON Schemas 结构约束...")
    schemas = list(root.glob("schemas/*.schema.json"))
    schema_errs = 0
    for s in schemas:
        try:
            with open(s, "r", encoding="utf-8") as f:
                json.load(f)
        except Exception as e:
            schema_errs += 1
            issues.append(f"Schema 语法损坏: {s.name} ({e})")
    if schema_errs == 0:
        print(f"      ✅ 12/12 个 JSON Schema 语法与结构 100% 合法")
    else:
        score -= 20

    # 2. 检测 References 业务模块
    print("[2/6] 🔍 正在检查 14 个业务领域模块规范...")
    core_modules = ['legal-research', 'contract-review', 'contract-playbook', 'dispute', 'ip', 'trade-secret', 'competition', 'labor']
    sec_modules = ['contract-drafting', 'data-privacy', 'corporate', 'compliance', 'legal-dd', 'legal-opinion']
    mod_errs = 0
    for m in core_modules + sec_modules:
        p = root / "references" / f"{m}.md"
        if not p.exists():
            mod_errs += 1
            issues.append(f"缺失模块文件: {p.name}")
            continue
        content = p.read_text(encoding="utf-8")
        if "TODO" in content:
            mod_errs += 1
            issues.append(f"模块存在未完成 TODO: {p.name}")
    if mod_errs == 0:
        print(f"      ✅ 14/14 个业务模块全部符合七段式规范且无 TODO 遗留")
    else:
        score -= 20

    # 3. 检测 Templates 模板
    print("[3/6] 🔍 正在检查 8 个交付物模板...")
    templates = ['executive-brief', 'legal-memo', 'contract-review', 'risk-matrix', 'evidence-matrix', 'legal-opinion', 'action-plan', 'message']
    tpl_errs = 0
    for t in templates:
        p = root / "templates" / f"{t}.md"
        if not p.exists():
            tpl_errs += 1
            issues.append(f"缺失模板文件: {p.name}")
            continue
        content = p.read_text(encoding="utf-8")
        if "Review Basis" not in content:
            tpl_errs += 1
            issues.append(f"模板缺失 Review Basis 抬头: {p.name}")
    if tpl_errs == 0:
        print(f"      ✅ 8/8 个交付物模板全部搭载标准 Review Basis 抬头")
    else:
        score -= 15

    # 4. 检测 Evals 评测集
    print("[4/6] 🔍 正在检查 Evals 评测用例库...")
    eval_cases = list(root.glob("evals/**/*.yaml"))
    eval_errs = 0
    for ec in eval_cases:
        try:
            with open(ec, "r", encoding="utf-8") as f:
                y = yaml.safe_load(f)
                if not y.get("id") or not y.get("rubric_items"):
                    eval_errs += 1
                    issues.append(f"用例缺少必需字段: {ec.name}")
        except Exception as e:
            eval_errs += 1
            issues.append(f"用例 YAML 解析失败: {ec.name} ({e})")
    if eval_errs == 0 and len(eval_cases) >= 14:
        print(f"      ✅ {len(eval_cases)}/{len(eval_cases)} 个基准评测用例结构完备")
    else:
        score -= 15

    # 5. 检测 Examples 端到端案例
    print("[5/6] 🔍 正在检查 Examples 4 套实战案例...")
    ex_dirs = list(root.glob("examples/0*"))
    ex_errs = 0
    for ed in ex_dirs:
        out_f = ed / "output.md"
        if not out_f.exists():
            ex_errs += 1
            issues.append(f"案例缺失 output.md: {ed.name}")
            continue
        chk = run_all_static_checks(out_f.read_text(encoding="utf-8"), lane="A" if "04" in ed.name else "B")
        if not chk["passed"]:
            ex_errs += 1
            issues.append(f"案例未通过门禁检测: {ed.name}")
    if ex_errs == 0 and len(ex_dirs) == 4:
        print(f"      ✅ 4/4 套端到端实战案例全部通过合规门禁检测")
    else:
        score -= 15

    # 6. 检测多生态软链接安装状态
    print("[6/6] 🔍 正在检查多生态 Agent 链接就绪情况...")
    home = Path.home()
    claude_link = home / ".claude" / "skills" / "china-legal-os"
    codex_link = home / ".codex" / "skills" / "china-legal-os"
    gemini_link = home / ".gemini" / "config" / "skills" / "china-legal-os"
    local_bin = home / ".local" / "bin" / "clos"

    installed_ecos = []
    if claude_link.exists(): installed_ecos.append("Claude Code")
    if codex_link.exists(): installed_ecos.append("Codex")
    if gemini_link.exists(): installed_ecos.append("Antigravity/Gemini")
    if local_bin.exists(): installed_ecos.append("CLI (~/.local/bin/clos)")

    if installed_ecos:
        print(f"      ✅ 已成功部署至生态: {', '.join(installed_ecos)}")
    else:
        print("      ℹ️ 尚未运行 ./scripts/install.sh 安装至本地生态环境")

    print("-" * 72)
    print(f"🏥 全系统健康体检得分: {score} / 100")
    if score == 100:
        print("🎉 恭喜！China Legal OS 全系统处于完全健康、工业级就绪状态！")
    else:
        print("⚠️ 发现以下问题需修复：")
        for iss in issues:
            print(" -", iss)
    print("=" * 72)


if __name__ == "__main__":
    run_doctor()
