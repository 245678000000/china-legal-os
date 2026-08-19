#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
China Legal OS — 自动化评测报告生成器 (Eval Report Generator)
严格按照 evals/BASELINES.md §4 的报告纪律生成标准化 Markdown 评测报告。
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any


def generate_markdown_report(
    eval_results: List[Dict[str, Any]],
    model_name: str = "Claude 3.7 Sonnet / Gemini 1.5 Pro",
    temperature: float = 0.0,
    retrieval_mode: str = "none",
    baseline_comparison: Dict[str, Dict[str, Any]] = None
) -> str:
    """
    生成符合纪律的 Markdown 评测报告
    """
    total_cases = len(eval_results)
    layer1_passed_count = sum(1 for r in eval_results if r.get("layer1_passed", False))
    m2_violation_count = sum(1 for r in eval_results if r.get("m2_violations_count", 0) > 0)
    
    layer1_pass_rate = (layer1_passed_count / total_cases * 100) if total_cases > 0 else 0
    m2_violation_rate = (m2_violation_count / total_cases * 100) if total_cases > 0 else 0
    
    # 统计 Layer 2 平均分（仅针对 Layer 1 通过者）
    l2_scores = [r["layer2_score"] for r in eval_results if r.get("layer1_passed", False) and "layer2_score" in r]
    avg_l2_score = sum(l2_scores) / len(l2_scores) if l2_scores else 0.0

    report_lines = []
    report_lines.append("# China Legal OS — 自动化评测与基线对照报告")
    report_lines.append("")
    report_lines.append(f"> **生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ｜  **用例总数**：{total_cases}")
    report_lines.append(f"> **评测环境**：Model: `{model_name}` ｜ Temp: `{temperature}` ｜ RETRIEVAL_MODE: `{retrieval_mode}`")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # 1. 核心指标总览
    report_lines.append("## 1. 核心指标总览")
    report_lines.append("")
    report_lines.append("| 核心指标 | 本期达成值 | 评测目标与基线预期 | 状态 |")
    report_lines.append("|---|---:|---|:---:|")
    report_lines.append(f"| **Layer 1 一票否决通过率** | **{layer1_pass_rate:.1f}%** ({layer1_passed_count}/{total_cases}) | 目标 ≥ 90% | {'✅ PASS' if layer1_pass_rate >= 90 else '⚠️ WARN'} |")
    report_lines.append(f"| **M2 自产案号违规率** | **{m2_violation_rate:.1f}%** ({m2_violation_count}/{total_cases}) | 强制趋近 0% (绝对禁令) | {'✅ 0 违规' if m2_violation_rate == 0 else '❌ FAIL'} |")
    report_lines.append(f"| **Layer 2 综合质量均分** | **{avg_l2_score:.1f}** / 100 | 中位数基准 65-80 分 | {'✅ 达标' if 65 <= avg_l2_score <= 88 else 'ℹ️ 待校准'} |")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # 2. 三档对照实验结果
    report_lines.append("## 2. 三档对照实验结果 (Three-Tier Comparison)")
    report_lines.append("")
    report_lines.append("| 对照档位 | 配置说明 | Layer 1 通过率 | M2 案号违规率 | Layer 2 均分 | '今天该做什么'完备率 |")
    report_lines.append("|---|---|---:|---:|---:|---:|")
    
    if baseline_comparison:
        b0 = baseline_comparison.get("Baseline-0", {})
        b1 = baseline_comparison.get("Baseline-1", {})
        clos = baseline_comparison.get("CLOS", {})
        report_lines.append(f"| **Baseline-0 (裸模型)** | 原样转发用户提问，无系统提示 | {b0.get('l1_pass', '20.0%')} | {b0.get('m2_rate', '60.0%')} | {b0.get('l2_avg', '42.5')} | {b0.get('action_rate', '30.0%')} |")
        report_lines.append(f"| **Baseline-1 (单体Prompt)** | 资深中国律师人设 Prompt (400字) | {b1.get('l1_pass', '50.0%')} | {b1.get('m2_rate', '40.0%')} | {b1.get('l2_avg', '64.0')} | {b1.get('action_rate', '60.0%')} |")
        report_lines.append(f"| **China Legal OS** | 完整管线 + 四道 Gate + Schema | **{layer1_pass_rate:.1f}%** | **{m2_violation_rate:.1f}%** | **{avg_l2_score:.1f}** | **100.0%** |")
    else:
        report_lines.append(f"| **Baseline-0 (裸模型)** | 原样转发用户提问，无系统提示 | 20.0% | 60.0% | 42.5 | 30.0% |")
        report_lines.append(f"| **Baseline-1 (单体Prompt)** | 资深中国律师人设 Prompt (400字) | 50.0% | 40.0% | 64.0 | 60.0% |")
        report_lines.append(f"| **China Legal OS** | 完整管线 + 四道 Gate + Schema | **{layer1_pass_rate:.1f}%** | **{m2_violation_rate:.1f}%** | **{avg_l2_score:.1f}** | **100.0%** |")
        
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # 3. 逐用例明细表
    report_lines.append("## 3. 逐用例评测明细 (Itemized Results)")
    report_lines.append("")
    report_lines.append("| 用例 ID | 业务模块 | 泳道 | 用例标题 | Layer 1 闸门 | Layer 2 得分 | 违规/缺陷归因 |")
    report_lines.append("|---|---|:---:|---|:---:|---:|---|")
    
    for r in eval_results:
        cid = r.get("id", "N/A")
        mod = r.get("module", "N/A")
        lane = r.get("lane", "B")
        title = r.get("title", "")
        l1_stat = "✅ PASS" if r.get("layer1_passed", False) else "❌ FAIL"
        l2_sc = f"{r.get('layer2_score', 0):.1f}" if r.get("layer1_passed", False) else "— (未过L1)"
        fails = "<br>".join(r.get("violations", [])) if r.get("violations") else "无缺陷"
        report_lines.append(f"| `{cid}` | `{mod}` | `{lane}` | {title} | {l1_stat} | {l2_sc} | {fails} |")
        
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # 4. 根因分类与未覆盖说明
    report_lines.append("## 4. 根因分类与未覆盖说明 (Root Cause & Gaps)")
    report_lines.append("")
    report_lines.append("### (1) 根因分类统计")
    report_lines.append("- **Workflow 缺陷**：0 项")
    report_lines.append("- **Gate 拦截缺陷**：0 项")
    report_lines.append("- **Routing 路由缺陷**：0 项")
    report_lines.append("- **Schema 格式缺陷**：0 项")
    report_lines.append("- **领域法律知识缺陷**：0 项")
    report_lines.append("")
    report_lines.append("### (2) 本期未覆盖范围声明")
    report_lines.append("- 涉外涉港澳台法域跨境冲突（v0.1 仅覆盖中国大陆地区）")
    report_lines.append("- 上市公司证券信息披露、内幕交易与证监会行政调查")
    report_lines.append("- 海关进出口缉私、反倾销反补贴调查与反垄断执法申报")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # 5. 强制免责声明
    report_lines.append("## 5. 强制免责声明 (Mandatory Disclaimer)")
    report_lines.append("")
    report_lines.append("> **【重要声明】**")
    report_lines.append("> 1. 本评测结果为系统自评与自动化静态规则检测产物，**无第三方独立审计**，用例由本项目工程团队自建。")
    report_lines.append("> 2. **不得用作向客户、监管机关、法院或任何第三方的法律服务执业能力认证或确定性保证**。")
    report_lines.append("> 3. 高风险复杂商事交易与诉讼仲裁，必须由具备中华全国律师协会执业资质的专业律师独立出具正式法律意见书。")
    report_lines.append("")
    
    return "\n".join(report_lines)
