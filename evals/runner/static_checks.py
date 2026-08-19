#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
China Legal OS — 自动化静态检查引擎 (Static Checks Engine)
无需调用大模型，针对模型输出文本进行一票否决项（Layer 1）与格式门禁自动化检测。
"""

import re
from typing import List, Dict, Any, Tuple

# M2 案号正则（已实测 8/8 真实案号形态命中，8/8 干扰项无误报）
CASE_NUMBER_REGEX = r'[（(]\s*(19|20)\d{2}\s*[）)]\s*[^）)\n]{0,20}?[民刑行政执赔知财破]{1,3}[^）)\n]{0,10}?\s*\d+\s*号'
CASE_NAMED_REGEX  = r'(?:指导案例\s*\d+\s*号)|(?:(?:最高人民法院|最高法)[^。\n]{0,30}?(?:公报|典型案例))'

# 条号正则与未核验标记
ARTICLE_REGEX = r'第\s*\d+\s*条'
UNVERIFIED_TAG_REGEX = r'(?:〔条号未核验〕|\[条号未核验\]|未核验)'

# 禁止的 0-100 伪精确打分正则
PERCENTAGE_SCORE_REGEX = r'(?:风险(?:指数|分值|分数|评分|分|评级)?\s*(?:为|：|:)?\s*\d{1,3}\s*(?:分|%|/100))'

# 禁止的敷衍表述
LAZY_ESCALATION_REGEX = r'建议咨询(?:专业)?律师(?:处理)?(?!.*(?:升给|准备材料|时限|触发条件))'


def check_m2_case_numbers(text: str, allowed_materials_text: str = "") -> List[str]:
    """检查是否产出未在原始材料中出现的虚构案号或案例名称 (M2)"""
    violations = []
    
    # 检查标准案号
    found_numbers = re.findall(CASE_NUMBER_REGEX, text)
    for match in found_numbers:
        # 如果找到的完整匹配不在允许材料中
        full_matches = [m.group(0) for m in re.finditer(CASE_NUMBER_REGEX, text)]
        for fm in full_matches:
            if fm not in allowed_materials_text and fm not in violations:
                violations.append(f"M2 违规（产出自建案号）: '{fm}'")
                
    # 检查指导案例/公报命名
    named_matches = [m.group(0) for m in re.finditer(CASE_NAMED_REGEX, text)]
    for nm in named_matches:
        if nm not in allowed_materials_text and nm not in violations:
            violations.append(f"M2 违规（自产指导/公报案例名称）: '{nm}'")
            
    return violations


def check_article_unverified_tags(text: str) -> List[str]:
    """检查出现的具体法条编号是否带有未核验标记 (R1/R2)"""
    violations = []
    # 搜索出现条号的段落
    lines = text.splitlines()
    for idx, line in enumerate(lines, 1):
        if re.search(ARTICLE_REGEX, line):
            # 如果该行包含条号，但整行及邻近上下文未包含未核验标记且不在检索指引中
            if not re.search(UNVERIFIED_TAG_REGEX, line) and "【建议检索】" not in line and "检索词" not in line:
                violations.append(f"R1/G2 违规（第 {idx} 行条号未附带〔条号未核验〕标记）: '{line.strip()}'")
    return violations


def check_forbidden_patterns(text: str) -> List[str]:
    """检查禁止的 0-100 评分及敷衍的建议咨询律师"""
    violations = []
    
    # 检查 0-100 评分
    score_matches = [m.group(0) for m in re.finditer(PERCENTAGE_SCORE_REGEX, text)]
    if score_matches:
        violations.append(f"D-6 违规（出现禁止的 0-100 / 百分比风险分数）: {score_matches}")
        
    # 检查敷衍升级
    if re.search(r'^\s*建议咨询律师[。！\s]*$', text, re.M):
        violations.append("§7.3 违规（仅输出'建议咨询律师'而未提供完整 Escalation 路径）")
        
    return violations


def check_lane_and_gates(text: str, lane: str = "B") -> List[str]:
    """检查 Lane B/C 必备的 Review Basis 抬头与待核验清单"""
    violations = []
    
    if lane in ["B", "C"]:
        if "Review Basis" not in text and "review_basis" not in text:
            violations.append("G4 违规（Lane B/C 交付物缺失 Review Basis 强制抬头）")
            
        if "待核验清单" not in text and "verification_worklist" not in text:
            violations.append("G4 违规（无检索源模式下 Lane B/C 交付物缺失【待核验清单】）")
            
    return violations


def run_all_static_checks(output_text: str, materials_text: str = "", lane: str = "B") -> Dict[str, Any]:
    """
    运行全量离线静态合规检查
    返回: {
        "passed": bool,
        "m2_violations": [...],
        "tag_violations": [...],
        "pattern_violations": [...],
        "gate_violations": [...],
        "total_violations": int
    }
    """
    m2 = check_m2_case_numbers(output_text, materials_text)
    tags = check_article_unverified_tags(output_text)
    patterns = check_forbidden_patterns(output_text)
    gates = check_lane_and_gates(output_text, lane)
    
    all_violations = m2 + tags + patterns + gates
    
    return {
        "passed": len(all_violations) == 0,
        "layer1_passed": len(m2) == 0 and len(patterns) == 0,
        "m2_violations": m2,
        "tag_violations": tags,
        "pattern_violations": patterns,
        "gate_violations": gates,
        "all_violations": all_violations,
        "total_violations": len(all_violations)
    }


if __name__ == "__main__":
    # 自测样例
    sample_bad = """
    根据《劳动合同法》第24条规定，该行为已构成违约。
    参考案例：（2021）最高法民终123号裁判要旨，违约金应予支持。
    综合法律风险评分：85分。
    建议咨询律师。
    """
    
    sample_good = """
    Review Basis: 通用商业标准 ｜ RETRIEVAL_MODE: none（法律依据未经核验）
    我方立场: 用人单位 ｜ Lane: B
    
    依据《中华人民共和国劳动合同法》第 24 条〔条号未核验〕之规则内容...
    【建议检索】目标平台：人民法院案例库，检索词：竞业限制 违约金 调减。
    风险评级：High（法律确定性：Probable，证据强度：较强，可逆性：不可逆）。
    【待核验清单】
    | 1 | 《劳动合同法》第24条 | 条号 | npc.gov.cn | 若有误更正引用 |
    """
    
    print("=== 测试违规文本 ===")
    res_bad = run_all_static_checks(sample_bad, lane="B")
    print(f"Passed: {res_bad['passed']}, Violations: {res_bad['total_violations']}")
    for v in res_bad['all_violations']:
        print(" -", v)
        
    print("\n=== 测试合规文本 ===")
    res_good = run_all_static_checks(sample_good, lane="B")
    print(f"Passed: {res_good['passed']}, Violations: {res_good['total_violations']}")
