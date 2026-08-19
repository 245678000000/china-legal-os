#!/usr/bin/env bash
# ==============================================================================
# China Legal OS — 多生态一键安装与适配部署脚本
# 支持 Claude Code、Codex、Antigravity (Gemini)、Cursor 等 Agent 环境
# ==============================================================================

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "======================================================================"
echo "          China Legal OS — 一键安装与多生态配置向导"
echo "======================================================================"
echo "[*] 项目根目录: $REPO_DIR"

# 1. 配置 Claude Code 生态 (~/.claude/skills/china-legal-os)
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
if [ -d "$HOME/.claude" ] || [ -d "$CLAUDE_SKILLS_DIR" ]; then
    mkdir -p "$CLAUDE_SKILLS_DIR"
    rm -rf "$CLAUDE_SKILLS_DIR/china-legal-os"
    ln -sf "$REPO_DIR" "$CLAUDE_SKILLS_DIR/china-legal-os"
    echo "[+] ✅ 成功安装至 Claude Code 生态: $CLAUDE_SKILLS_DIR/china-legal-os"
else
    mkdir -p "$CLAUDE_SKILLS_DIR"
    ln -sf "$REPO_DIR" "$CLAUDE_SKILLS_DIR/china-legal-os"
    echo "[+] ✅ 已创建 Claude Skills 目录并建立链接: $CLAUDE_SKILLS_DIR/china-legal-os"
fi

# 2. 配置 Codex / OpenAI 生态 (~/.codex/skills/china-legal-os)
CODEX_SKILLS_DIR="$HOME/.codex/skills"
mkdir -p "$CODEX_SKILLS_DIR"
rm -rf "$CODEX_SKILLS_DIR/china-legal-os"
ln -sf "$REPO_DIR" "$CODEX_SKILLS_DIR/china-legal-os"
echo "[+] ✅ 成功安装至 Codex 生态: $CODEX_SKILLS_DIR/china-legal-os"

# 3. 配置 Antigravity / Gemini 生态 (~/.gemini/config/skills/china-legal-os)
GEMINI_SKILLS_DIR="$HOME/.gemini/config/skills"
mkdir -p "$GEMINI_SKILLS_DIR"
rm -rf "$GEMINI_SKILLS_DIR/china-legal-os"
ln -sf "$REPO_DIR" "$GEMINI_SKILLS_DIR/china-legal-os"
echo "[+] ✅ 成功安装至 Antigravity/Gemini 生态: $GEMINI_SKILLS_DIR/china-legal-os"

# 4. 配置本地 CLI 命令 (~/.local/bin/clos)
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"
ln -sf "$REPO_DIR/bin/clos" "$LOCAL_BIN/clos"
echo "[+] ✅ 成功将 clos 命令行工具链接至: $LOCAL_BIN/clos"

# 赋予执行权限
chmod +x "$REPO_DIR/bin/clos" "$REPO_DIR/scripts/clos_engine.py" "$REPO_DIR/evals/runner/run.py"

echo "======================================================================"
echo "🎉 安装完成！您现在可以通过以下方式使用 China Legal OS："
echo " 1. 命令行交互: $REPO_DIR/bin/clos"
echo " 2. 运行自动化评测: $REPO_DIR/bin/clos eval"
echo " 3. Claude Code 中直接给法务任务（自动路由识别）"
echo "======================================================================"
