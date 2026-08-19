#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
China Legal OS — 企业级高保真 HTML 法务报表渲染器 (HTML Reporter)
将 Markdown 交付物渲染为单文件自包含、高审美、支持打印为 PDF 的现代化企业法务报告。
无需外部前端依赖，纯 Python 实现。
"""

import os
import re
import sys
import html
import argparse
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — China Legal OS 交付报告</title>
    <style>
        :root {{
            --primary: #1e3a8a;
            --primary-light: #eff6ff;
            --text-main: #1f2937;
            --text-muted: #4b5563;
            --border-color: #e5e7eb;
            --bg-page: #f8fafc;
            --bg-card: #ffffff;
            --badge-black: #111827;
            --badge-critical: #991b1b;
            --badge-red: #dc2626;
            --badge-yellow: #d97706;
            --badge-green: #16a34a;
            --badge-blue: #2563eb;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            line-height: 1.65;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 1080px;
            margin: 0 auto;
            background: var(--bg-card);
            padding: 48px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border-color);
        }}

        /* 抬头卡片 */
        .review-basis-box {{
            background: #0f172a;
            color: #f8fafc;
            padding: 16px 20px;
            border-radius: 8px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 13px;
            line-height: 1.6;
            margin-bottom: 32px;
            border-left: 4px solid #38bdf8;
        }}

        h1 {{
            font-size: 26px;
            font-weight: 700;
            color: var(--primary);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 12px;
            margin-bottom: 24px;
        }}

        h2 {{
            font-size: 20px;
            font-weight: 600;
            color: #0f172a;
            margin-top: 32px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
        }}

        h3 {{
            font-size: 16px;
            font-weight: 600;
            color: #334155;
            margin-top: 20px;
            margin-bottom: 12px;
        }}

        p {{
            margin-bottom: 14px;
            color: var(--text-main);
        }}

        /* 表格样式 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0 28px 0;
            font-size: 14px;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }}

        th {{
            background-color: #f1f5f9;
            color: #334155;
            font-weight: 600;
            text-align: left;
            padding: 12px 16px;
            border-bottom: 2px solid var(--border-color);
            white-space: nowrap;
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            vertical-align: top;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background-color: #f8fafc;
        }}

        /* 风险与状态徽标 */
        .badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .badge-black {{ background: #111827; color: #ffffff; }}
        .badge-critical {{ background: #fef2f2; color: #991b1b; border: 1px solid #f87171; }}
        .badge-red {{ background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; }}
        .badge-yellow {{ background: #fef3c7; color: #b45309; border: 1px solid #fcd34d; }}
        .badge-green {{ background: #dcfce7; color: #15803d; border: 1px solid #86efac; }}
        .badge-blue {{ background: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }}

        /* 引用块 */
        blockquote {{
            background-color: #f8fafc;
            border-left: 4px solid #64748b;
            padding: 14px 18px;
            margin: 16px 0;
            border-radius: 0 8px 8px 0;
            font-size: 14px;
            color: #334155;
        }}

        /* 待核验清单卡片 */
        .verification-box {{
            background-color: #fffbeb;
            border: 1px solid #fde68a;
            border-left: 4px solid #f59e0b;
            padding: 16px;
            border-radius: 6px;
            margin: 20px 0;
        }}

        /* 代码块与条号高亮 */
        code {{
            background: #f1f5f9;
            color: #0f172a;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }}

        pre {{
            background: #0f172a;
            color: #e2e8f0;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 13px;
            margin: 16px 0;
            line-height: 1.5;
        }}
        pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
        }}

        /* 列表 */
        ul, ol {{
            margin-left: 24px;
            margin-bottom: 16px;
        }}
        li {{
            margin-bottom: 6px;
        }}

        hr {{
            border: none;
            border-top: 1px dashed var(--border-color);
            margin: 32px 0;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 16px;
            border-top: 1px solid var(--border-color);
            font-size: 12px;
            color: #94a3b8;
            text-align: center;
        }}

        /* 打印优化样式 */
        @media print {{
            body {{
                background: #ffffff;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                border: none;
                padding: 0;
                max-width: 100%;
            }}
            .review-basis-box {{
                border: 1px solid #000;
                background: #f8fafc;
                color: #000;
            }}
            a {{
                text-decoration: none;
                color: #000;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {body_content}
        <div class="footer">
            China Legal OS · 面向中国大陆企业法务的模块化 AI 工作系统 ｜ 内部工作参考文件
        </div>
    </div>
</body>
</html>
"""


def render_badges(text: str) -> str:
    """自动将文本中的风险级别和确定性关键词替换为色彩 Badge"""
    replacements = [
        (r'`BLACK`', '<span class="badge badge-black">BLACK</span>'),
        (r'`Critical`', '<span class="badge badge-critical">Critical</span>'),
        (r'`RED`', '<span class="badge badge-red">RED</span>'),
        (r'`YELLOW`', '<span class="badge badge-yellow">YELLOW</span>'),
        (r'`GREEN`', '<span class="badge badge-green">GREEN</span>'),
        (r'`High`', '<span class="badge badge-red">High</span>'),
        (r'`Medium`', '<span class="badge badge-yellow">Medium</span>'),
        (r'`Low`', '<span class="badge badge-green">Low</span>'),
        (r'`Confirmed`', '<span class="badge badge-green">Confirmed</span>'),
        (r'`Probable`', '<span class="badge badge-blue">Probable</span>'),
        (r'`Conditional`', '<span class="badge badge-yellow">Conditional</span>'),
        (r'`Unverified`', '<span class="badge badge-red">Unverified</span>'),
    ]
    for pattern, badge_html in replacements:
        text = re.sub(pattern, badge_html, text)
    return text


def simple_markdown_to_html(md_text: str) -> Tuple[str, str]:
    """简单稳健的轻量级 Markdown 到 HTML 转换器"""
    lines = md_text.splitlines()
    html_lines = []
    in_table = False
    table_headers = []
    in_code_block = False
    in_review_basis = False
    review_basis_lines = []
    doc_title = "法务交付报告"

    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检查是否为文档标题
        if line.startswith("# ") and not html_lines:
            doc_title = line[2:].strip()
            html_lines.append(f"<h1>{html.escape(doc_title)}</h1>")
            i += 1
            continue

        # 检查 Review Basis 抬头代码块
        if line.startswith("```") and not in_code_block and not in_review_basis:
            # 查看下一行是否是 Review Basis
            if i + 1 < len(lines) and "Review Basis" in lines[i+1]:
                in_review_basis = True
                review_basis_lines = []
                i += 1
                continue
            else:
                in_code_block = True
                html_lines.append("<pre><code>")
                i += 1
                continue

        if in_review_basis:
            if line.startswith("```"):
                in_review_basis = False
                header_text = "<br>".join([html.escape(l) for l in review_basis_lines if l.strip()])
                html_lines.append(f'<div class="review-basis-box">{header_text}</div>')
            else:
                review_basis_lines.append(line)
            i += 1
            continue

        if in_code_block:
            if line.startswith("```"):
                in_code_block = False
                html_lines.append("</code></pre>")
            else:
                html_lines.append(html.escape(line))
            i += 1
            continue

        # 表格处理
        if "|" in line:
            parts = [p.strip() for p in line.strip().split("|")[1:-1]]
            if not in_table:
                in_table = True
                table_headers = parts
                html_lines.append("<table>")
                html_lines.append("<thead><tr>")
                for th in table_headers:
                    html_lines.append(f"<th>{render_badges(html.escape(th))}</th>")
                html_lines.append("</tr></thead><tbody>")
                i += 1
                # 跳过分隔行 |---|---|
                if i < len(lines) and re.match(r'\|?\s*[-:]+\s*\|', lines[i]):
                    i += 1
                continue
            else:
                # 表格数据行
                if re.match(r'\|?\s*[-:]+\s*\|', line):
                    i += 1
                    continue
                html_lines.append("<tr>")
                for td in parts:
                    # 处理粗体与内联代码
                    formatted_td = html.escape(td)
                    formatted_td = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', formatted_td)
                    formatted_td = re.sub(r'`(.+?)`', r'<code>\1</code>', formatted_td)
                    formatted_td = formatted_td.replace('&lt;br&gt;', '<br>').replace('<br>', '<br>')
                    formatted_td = render_badges(formatted_td)
                    html_lines.append(f"<td>{formatted_td}</td>")
                html_lines.append("</tr>")
                i += 1
                continue
        else:
            if in_table:
                in_table = False
                html_lines.append("</tbody></table>")

        # 标题处理
        if line.startswith("### "):
            html_lines.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("> "):
            quote_content = html.escape(line[2:])
            quote_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', quote_content)
            quote_content = render_badges(quote_content)
            html_lines.append(f"<blockquote>{quote_content}</blockquote>")
        elif line.startswith("- [ ] ") or line.startswith("- [x] "):
            is_checked = line.startswith("- [x] ")
            box_sym = "☑" if is_checked else "☐"
            item_text = html.escape(line[6:])
            item_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_text)
            html_lines.append(f"<p>{box_sym} {item_text}</p>")
        elif line.startswith("- ") or line.startswith("* "):
            item_text = html.escape(line[2:])
            item_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_text)
            item_text = re.sub(r'`(.+?)`', r'<code>\1</code>', item_text)
            item_text = render_badges(item_text)
            html_lines.append(f"<li>{item_text}</li>")
        elif line.startswith("---"):
            html_lines.append("<hr>")
        elif line.strip():
            para_text = html.escape(line)
            para_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para_text)
            para_text = re.sub(r'`(.+?)`', r'<code>\1</code>', para_text)
            para_text = render_badges(para_text)
            html_lines.append(f"<p>{para_text}</p>")

        i += 1

    if in_table:
        html_lines.append("</tbody></table>")

    body_html = "\n".join(html_lines)
    return doc_title, body_html


def convert_markdown_file_to_html(md_path: str, output_html_path: str = None) -> str:
    """读取 Markdown 文件并输出自包含 HTML 报告"""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    title, body_html = simple_markdown_to_html(md_content)
    full_html = HTML_TEMPLATE.format(title=title, body_content=body_html)

    if output_html_path:
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(full_html)

    return full_html


def main():
    parser = argparse.ArgumentParser(description="China Legal OS — 高保真 HTML 法务报表渲染器")
    parser.add_argument("input_md", help="输入 Markdown 交付物文件路径")
    parser.add_argument("-o", "--output", help="输出 HTML 文件路径 (默认保存为 [输入名].html)")

    args = parser.parse_args()
    out_path = args.output or os.path.splitext(args.input_md)[0] + ".html"

    convert_markdown_file_to_html(args.input_md, out_path)
    print(f"[+] ✅ 成功生成企业级 HTML 报表: {out_path}")


if __name__ == "__main__":
    main()
