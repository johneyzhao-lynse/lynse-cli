#!/bin/bash

# Lynse CLI Auto-Install Script
# 自动检测环境并安装到正确的 skills 目录

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
SKILL_NAME="lynse-cli"

# 检查是否从命令行传入了 API 服务器地址
API_HOST_ARG=""
for arg in "$@"; do
    case "$arg" in
        --api-host=*)
            API_HOST_ARG="${arg#*=}"
            ;;
    esac
done

# 如果没有命令行参数，尝试从环境变量读取
if [ -z "$API_HOST_ARG" ]; then
    API_HOST_ARG="${LYNSE_API_HOST_FROM_PROMPT:-}"
fi

# 如果还没有，尝试从标准输入读取（支持管道传入）
if [ -z "$API_HOST_ARG" ] && [ ! -t 0 ]; then
    # 读取所有输入到变量
    INPUT_CONTENT=$(cat)
    # 匹配包含 API 服务器地址的行（支持中英文多种格式）
    # 支持："API 服务器地址"、"API Server"、"服务器地址"、"api server"等
    API_LINE=$(echo "$INPUT_CONTENT" | grep -iE "(API 服务器地址|API Server|服务器地址|api server)" || true)
    if [ -n "$API_LINE" ]; then
        # 从该行提取 URL（支持 http/https，支持路径）
        API_HOST_ARG=$(echo "$API_LINE" | grep -oE "https?://[^[:space:]\"']+" | head -1 || true)
        if [ -n "$API_HOST_ARG" ]; then
            echo -e "${BLUE}[INFO]${NC} 从输入中提取 API 服务器地址：$API_HOST_ARG" >&2
        fi
    fi
fi

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" >&2
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# 检测可用的 Python 3.11+ 解释器（python3 优先，回退 python）
# 检测结果写入全局变量 PYTHON_BIN，供安装提示使用
detect_python() {
    PYTHON_BIN=""
    for candidate in python3 python; do
        if command -v "$candidate" &> /dev/null && \
            "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
            PYTHON_BIN="$candidate"
            break
        fi
    done

    if [ -z "$PYTHON_BIN" ]; then
        log_error "未检测到 Python 3.11+。请安装 Python 3.11 或更高版本：https://www.python.org/downloads/"
        return 1
    fi

    local py_ver
    py_ver=$($PYTHON_BIN -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")' 2>/dev/null || echo "unknown")
    log_info "检测到 Python：$PYTHON_BIN (v$py_ver)"
}

# 检测环境函数
detect_environment() {
    local target_dir=""
    local env_name=""

    # 检测 OpenClaw
    if [ -d "$HOME/.openclaw/workspace" ]; then
        target_dir="$HOME/.openclaw/workspace/skills/$SKILL_NAME"
        env_name="OpenClaw"
        log_info "检测到 OpenClaw 环境"
    fi

    # 检测 Claude Code
    if [ -d "$HOME/.claude" ]; then
        if [ -z "$target_dir" ]; then
            target_dir="$HOME/.claude/skills/$SKILL_NAME"
            env_name="Claude Code"
            log_info "检测到 Claude Code 环境"
        fi
    fi

    # 检测 Cursor
    if [ -d "$HOME/.cursor" ]; then
        if [ -z "$target_dir" ]; then
            target_dir="$HOME/.cursor/skills/$SKILL_NAME"
            env_name="Cursor"
            log_info "检测到 Cursor 环境"
        fi
    fi

    # 检测 Hermes (常见路径)
    if [ -d "$HOME/.hermes" ]; then
        if [ -z "$target_dir" ]; then
            target_dir="$HOME/.hermes/skills/$SKILL_NAME"
            env_name="Hermes"
            log_info "检测到 Hermes 环境"
        fi
    fi

    # 如果没有检测到任何环境，提示用户手动指定
    if [ -z "$target_dir" ]; then
        log_error "未检测到支持的 AI 助手环境"
        echo ""
        echo "支持的环境："
        echo "  - OpenClaw: ~/.openclaw/workspace/skills/"
        echo "  - Claude Code: ~/.claude/skills/"
        echo "  - Cursor: ~/.cursor/skills/"
        echo "  - Hermes: ~/.hermes/skills/"
        echo ""
        read -p "请输入目标 skills 目录路径：" target_dir
        if [ -z "$target_dir" ]; then
            log_error "未提供路径，安装取消"
            exit 1
        fi
        env_name="Manual"
    fi

    echo "$target_dir"
}

# 安装函数
install_skill() {
    local target_dir="$1"

    log_info "开始安装到：$target_dir"

    # 创建目录
    mkdir -p "$target_dir"

    # 复制技能文件
    log_info "复制技能文件..."
    cp -r "$SCRIPT_DIR"/* "$target_dir/" 2>/dev/null || true

    # 创建 .env 配置文件（如果不存在）
    if [ ! -f "$target_dir/.env" ]; then
        log_info "创建 .env 配置文件..."
        if [ -f "$target_dir/.env.example" ]; then
            cp "$target_dir/.env.example" "$target_dir/.env"
            # 如果传入了 API 服务器地址，写入 .env
            if [ -n "$API_HOST_ARG" ]; then
                echo "LYNSE_API_HOST=$API_HOST_ARG" >> "$target_dir/.env"
                log_info "已设置 API 服务器地址：$API_HOST_ARG"
            fi
        else
            # 使用传入的 API 服务器地址，否则使用占位符
            local api_host_value="${API_HOST_ARG:-https://your-api-host/api}"
            cat > "$target_dir/.env" << EOF
# Lynse CLI Configuration

# API 服务器地址
LYNSE_API_HOST=$api_host_value

# API Key — 不要在这里填真实密钥。推荐用交互方式登录（密钥仅保存在本机）：
#   ${PYTHON_BIN:-python3} lynse.py auth login
LYNSE_API_KEY=

# [可选] 限定只有此用户 ID 可操作
# LYNSE_OWNER_ID=
EOF
        fi
        log_warn "运行 auth login 录入你的 LYNSE_API_KEY（不要把密钥写死在 .env）"
    fi

    # 设置执行权限
    log_info "设置执行权限..."
    chmod +x "$target_dir"/*.sh 2>/dev/null || true
    chmod 600 "$target_dir/.env" 2>/dev/null || true

    log_success "安装完成！"
    echo ""
    echo "==================================="
    echo "  Lynse CLI 安装成功"
    echo "==================================="
    echo ""
    echo "下一步："
    echo "  1. 录入你的 API Key（交互式，密钥仅保存在本机 ~/.lynse/config.json）："
    echo "       ${PYTHON_BIN:-python3} lynse.py auth login"
    echo "  2. 验证：${PYTHON_BIN:-python3} lynse.py auth status"
    echo "  3. 在 AI 助手中使用 lynse-cli 技能"
    echo ""
    echo "使用方法（本机检测到的 Python：${PYTHON_BIN:-未检测到}）："
    echo "  ${PYTHON_BIN:-python3} lynse.py me                       # 查询当前用户信息"
    echo "  ${PYTHON_BIN:-python3} lynse.py meetings list            # 最近会议列表"
    echo "  ${PYTHON_BIN:-python3} lynse.py meetings summary <id>    # 会议 AI 总结"
    echo ""
    echo "文档：$target_dir/README.md"
    echo "==================================="
}

# 主程序
main() {
    echo "==================================="
    echo "  Lynse CLI 自动安装脚本"
    echo "==================================="
    echo ""

    # 先检测 Python（安装提示里要用到）
    detect_python || exit 1

    local target_dir=$(detect_environment)
    install_skill "$target_dir"
}

main "$@"
