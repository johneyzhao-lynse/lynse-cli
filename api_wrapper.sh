#!/bin/bash

# 获取当前脚本所在的绝对目录，保证能在任何地方被 OpenClaw 准确调用
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# ============================================================
# 安全措施说明：
# 1. API Key 从 .env 文件读取（跨平台通用）
# 2. .env 文件自动设置 600 权限（仅所有者可读写）
# 3. Token 缓存文件设置 600 权限
# 4. 不在日志/输出中暴露 API Key 和 Token
# 5. 使用 -s 静默 curl，避免凭证泄露到终端
# 6. 移除硬编码的备用 JWT Token
# ============================================================

# 1. 基础配置
API_HOST="http://119.97.160.133:10060"  # 所有API请求的基础地址
# API_HOST="http://10.246.52.153:10060" # 本地服

# 2. 安全读取 API Key（优先级：环境变量 > .env 文件）
ENV_FILE="$DIR/.env"

read_api_key() {
    # 优先级 1: 环境变量
    if [ -n "${LYNSE_API_KEY:-}" ]; then
        echo "$LYNSE_API_KEY"
        return 0
    fi

    # 优先级 2: .env 文件（自动确保权限安全）
    if [ -f "$ENV_FILE" ]; then
        # 自动修复权限：仅所有者可读写
        chmod 600 "$ENV_FILE" 2>/dev/null
        local key
        key=$(grep -E '^LYNSE_API_KEY=' "$ENV_FILE" | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'")
        if [ -n "$key" ]; then
            echo "$key"
            return 0
        fi
    fi

    return 1
}

API_KEY=$(read_api_key)

# 3. 凭证预检
if [ -z "$API_KEY" ]; then
    echo "LYNSE API KEY 未配置！"
    echo ""
    echo "请在 $(dirname "$0")/.env 文件中配置 API Key："
    echo '  echo "LYNSE_API_KEY=你的API_Key" > ~/.claude/skills/lynse/.env && chmod 600 ~/.claude/skills/lynse/.env'
    echo ""
    echo "或通过环境变量（会话级别）："
    echo '  export LYNSE_API_KEY="你的API_Key"'
    echo ""
    echo "获取 API Key：联系管理员或从系统控制台获取（dk_xxx 格式）"
    exit 1
fi

# 4. Token 缓存文件（安全权限）
TOKEN_FILE="/tmp/.lynse_token_cache_$USER"
ensure_token_file_perms() {
    if [ -f "$TOKEN_FILE" ]; then
        chmod 600 "$TOKEN_FILE" 2>/dev/null
    fi
}

# 5. 静默获取 Token（不输出凭证信息）
get_token_via_apikey() {
    local response
    response=$(curl -s -X POST "$API_HOST/api/auth/apikey/token" \
        --header @- <<EOF_HEADER 2>/dev/null
X-API-Key: $API_KEY
EOF_HEADER
    )
    echo "$response" | grep -o '"accessToken":"[^"]*"' | cut -d'"' -f4
}

ensure_valid_token() {
    ensure_token_file_perms

    if [ -f "$TOKEN_FILE" ]; then
        local cached_token
        cached_token=$(cat "$TOKEN_FILE")
        # 静默验证 Token
        local http_code
        http_code=$(curl -s -o /dev/null -w "%{http_code}" \
            -X GET "$API_HOST/api/business/customer/current" \
            -H "Authorization: $cached_token" \
            -H "X-API-Key: $API_KEY" 2>/dev/null)
        if [ "$http_code" -eq 200 ]; then
            TOKEN="$cached_token"
            return 0
        fi
    fi

    # 缓存无效，重新获取
    local new_token
    new_token=$(get_token_via_apikey)
    if [ -n "$new_token" ] && [ "$new_token" != "null" ]; then
        echo "$new_token" > "$TOKEN_FILE"
        chmod 600 "$TOKEN_FILE"
        TOKEN="$new_token"
        return 0
    fi

    # API Key 获取失败
    echo "API Key 认证失败，请检查 Key 是否有效"
    return 1
}

# 获取有效 Token
ensure_valid_token || exit 1

# 6. 自动路由到统一 CLI
"$DIR/lynse_unified.sh" --host "$API_HOST" "$@"

# 7. 语义化路由（复用已获取的 Token）
ACTION=$1
shift
PARAMS="$*"

case $ACTION in
    # 用户信息
    "getCurrentCustomer")
        curl -s -X GET "$API_HOST/api/business/customer/current" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "getUserInfo")
        curl -s -X GET "$API_HOST/sysUser/info" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "id:$1"
        ;;
    "getUserPoints")
        RESPONSE=$(curl -s -X GET "$API_HOST/api/business/customer/current" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY")
        POINTS=$(echo "$RESPONSE" | grep -o '"pointsAmount":[0-9]*' | cut -d: -f2)
        USED_POINTS=$(echo "$RESPONSE" | grep -o '"usedPointsAmount":[0-9]*' | cut -d: -f2)
        echo "当前积分: ${POINTS:-0}"
        echo "已使用积分: ${USED_POINTS:-0}"
        ;;
    "getUserPhone")
        RESPONSE=$(curl -s -X GET "$API_HOST/api/business/customer/current" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY")
        echo "$RESPONSE" | grep -o '"phone":"[0-9*]*"' | cut -d: -f2 | tr -d '"'
        ;;

    # 文件管理
    "listFiles")
        curl -s -X GET "$API_HOST/api/business/file/list" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "getFileInfo")
        curl -s -X GET "$API_HOST/api/business/file/info?fileId=$1" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "getConclusion")
        curl -s -X GET "$API_HOST/api/business/file/conclusion/list?fileId=$1" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "getConclusionList")
        curl -s -X GET "$API_HOST/api/business/file/conclusion/list?fileId=$1" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "getOutline")
        curl -s -X GET "$API_HOST/api/business/file/outline/get?fileId=$1" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "exportOutline")
        curl -s -X GET "$API_HOST/api/business/file/outline/export?fileId=$1" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "getTranscriptionRecord")
        curl -s -X GET "$API_HOST/api/business/file/trans/get?fileId=$1" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "listFilesByTimeRange")
        if [ -n "$1" ]; then
            startTime=$(date -d "$1 ago" +'%Y-%m-%dT%H:%M:%S' 2>/dev/null || date -v-"${1}"d +'%Y-%m-%dT%H:%M:%S')
        else
            startTime=$(date -d '7 days ago' +'%Y-%m-%dT%H:%M:%S' 2>/dev/null || date -v-7d +'%Y-%m-%dT%H:%M:%S')
        fi
        endTime=$(date +'%Y-%m-%dT%H:%M:%S')
        curl -s -X GET "$API_HOST/api/business/file/timeRange/list?startTime=$startTime&endTime=$endTime" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;

    # AI 模型管理
    "getAiModels")
        curl -s -X GET "$API_HOST/ai/getAllAIModelList" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "addModel")
        curl -s -X POST "$API_HOST/ai/addModel" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d "$PARAMS"
        ;;
    "deleteModel")
        curl -s -X DELETE "$API_HOST/ai/deleteModel" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "id:$1"
        ;;
    "editModel")
        curl -s -X POST "$API_HOST/ai/editModel" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d "$PARAMS"
        ;;
    "enableModel")
        curl -s -X POST "$API_HOST/ai/enableModel" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "id:$1" -H "enabled:$2"
        ;;

    # 设备管理
    "getDevicePage")
        curl -s -X GET "$API_HOST/deviceMgt/page9" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "pageNum:$1" -H "pageSize:10"
        ;;
    "getDeviceInfo")
        curl -s -X GET "$API_HOST/deviceMgt/info5" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "id:$1"
        ;;
    "unbindDevice")
        curl -s -X POST "$API_HOST/deviceMgt/unbind" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "id:$1"
        ;;

    # 系统用户管理
    "getCurrentUser")
        curl -s -X GET "$API_HOST/sysUser/current" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "addUser")
        curl -s -X POST "$API_HOST/sysUser/add2" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d "$PARAMS"
        ;;
    "editUser")
        curl -s -X POST "$API_HOST/sysUser/edit1" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d "$PARAMS"
        ;;
    "removeUser")
        curl -s -X POST "$API_HOST/sysUser/remove" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "id:$1"
        ;;

    # 登录
    "login")
        curl -s -X POST "$API_HOST/sysLogin/login" -H "Content-Type: application/json" -d "{\"username\":\"$1\",\"password\":\"$2\"}"
        ;;
    "loginWithPhone")
        curl -s -X POST "$API_HOST/sysLogin/login" -H "Content-Type: application/json" -d "{\"phone\":\"$1\",\"captcha\":\"$2\"}"
        ;;
    "logout")
        curl -s -X POST "$API_HOST/sysLogin/logout" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;

    # 消息
    "sendSms")
        curl -s -X POST "$API_HOST/message/sendSmsMessage" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d "$PARAMS"
        ;;
    "sendEmail")
        curl -s -X POST "$API_HOST/message/sendEmailMessage" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d "$PARAMS"
        ;;

    # 系统管理
    "getRoleList")
        curl -s -X GET "$API_HOST/sysRole/list1" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;
    "getMenuTree")
        curl -s -X GET "$API_HOST/sysMenu/tree" -H "Authorization: $TOKEN" -H "X-API-Key: $API_KEY"
        ;;

    *)
        echo "Error: 不支持的 Action $ACTION。"
        echo "支持的操作: getCurrentCustomer, getUserInfo, getUserPoints, getUserPhone, listFiles, getFileInfo, getConclusion, getOutline, exportOutline, getTranscriptionRecord, listFilesByTimeRange, getAiModels, addModel, deleteModel, editModel, enableModel, getDevicePage, getDeviceInfo, unbindDevice, getCurrentUser, addUser, editUser, removeUser, login, loginWithPhone, logout, sendSms, sendEmail, getRoleList, getMenuTree"
        exit 1
        ;;
esac
