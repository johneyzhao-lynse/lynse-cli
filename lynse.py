#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lynse CLI - 核心 API 封装模块
跨平台支持：Windows / macOS / Linux

用法：
    python lynse.py <command> [参数...]

示例：
    python lynse.py getCurrentCustomer
    python lynse.py getFileInfo 12345
"""

import os
import sys
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

try:
    import requests
except ImportError:
    print("错误：缺少 requests 库，请运行 'pip install requests' 安装", file=sys.stderr)
    sys.exit(1)


class LynseAPIError(Exception):
    """API 调用异常"""
    def __init__(self, message: str, http_code: int = None, code: int = None):
        self.message = message
        self.http_code = http_code
        self.code = code
        super().__init__(self.message)


class LynseAPI:
    """Lynse API 客户端 - 处理认证和 API 调用"""

    # HTTP 错误码处理映射
    HTTP_ERROR_MESSAGES = {
        401: "Token 已过期，正在自动刷新...",
        403: "您的账户权限不足，请联系管理员升级权限",
        404: "请求的资源不存在",
        429: "请求过于频繁，请等待 60 秒后重试",
        500: "服务器暂时不可用，请稍后重试",
        502: "服务器暂时不可用，请稍后重试",
        503: "服务器暂时不可用，请稍后重试",
    }

    def __init__(self, api_host: str = None, api_key: str = None, config_file: str = None):
        """
        初始化 API 客户端

        Args:
            api_host: API 服务器地址
            api_key: API Key
            config_file: 配置文件路径（默认当前目录 .env）
        """
        # 1. 加载配置
        self._load_config(config_file)

        # 2. 使用传入参数或环境变量
        self.api_host = api_host or os.environ.get('LYNSE_API_HOST')
        self.api_key = api_key or os.environ.get('LYNSE_API_KEY')
        self.owner_id = os.environ.get('LYNSE_OWNER_ID')

        # 3. 验证配置
        if not self.api_host:
            raise LynseAPIError(
                "未设置 LYNSE_API_HOST 环境变量。\n"
                "请在 .env 文件中配置 API 服务器地址，或运行:\n"
                '  export LYNSE_API_HOST="http://your-api-host/api"'
            )
        if not self.api_key:
            raise LynseAPIError(
                "未设置 LYNSE_API_KEY 环境变量。\n"
                "请在 .env 文件中配置 API Key，或运行:\n"
                '  export LYNSE_API_KEY="dk_your_api_key"'
            )

        # 4. Token 缓存
        script_dir = Path(__file__).parent.resolve()
        self.token_file = Path(os.environ.get('LYNSE_TOKEN_FILE', script_dir / '.token_cache'))
        self._access_token: Optional[str] = None

    def _load_config(self, config_file: str = None):
        """从 .env 文件加载配置"""
        if config_file is None:
            script_dir = Path(__file__).parent.resolve()
            config_file = str(script_dir / '.env')

        config_path = Path(config_file)
        if not config_path.exists():
            return

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in ('LYNSE_API_HOST', 'LYNSE_API_KEY', 'LYNSE_OWNER_ID'):
                            os.environ[key] = value
        except Exception as e:
            print(f"警告：读取配置文件失败：{e}", file=sys.stderr)

    def _validate_token(self, token: str) -> bool:
        """验证 Token 格式（JWT 基本格式）"""
        if not token:
            return False
        # JWT 格式：三段 base64 由.连接
        pattern = r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$'
        return bool(re.match(pattern, token))

    def _get_cached_token(self) -> Optional[str]:
        """从缓存获取 Token"""
        if not self.token_file.exists():
            return None

        try:
            # 检查文件权限（Unix 系统）
            if os.name != 'nt':
                mode = self.token_file.stat().st_mode & 0o777
                if mode != 0o600:
                    self.token_file.chmod(0o600)

            token = self.token_file.read_text(encoding='utf-8').strip()
            if self._validate_token(token):
                return token
        except Exception:
            pass

        return None

    def _save_token(self, token: str):
        """保存 Token 到缓存文件"""
        try:
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            self.token_file.write_text(token, encoding='utf-8')

            # 设置文件权限为 600（仅所有者可读写）
            if os.name != 'nt':
                self.token_file.chmod(0o600)
        except Exception as e:
            print(f"警告：保存 Token 失败：{e}", file=sys.stderr)

    def _refresh_token(self) -> str:
        """使用 API Key 刷新 Token"""
        url = f"{self.api_host}/api/auth/apikey/token"
        headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, timeout=30)

            if response.status_code != 200:
                raise LynseAPIError(
                    "API Key 认证失败，请检查 LYNSE_API_KEY 是否正确",
                    http_code=response.status_code
                )

            data = response.json()
            access_token = data.get('data', {}).get('accessToken') or data.get('accessToken')

            if not access_token or access_token == 'null':
                raise LynseAPIError("API Key 认证失败：返回的 Token 为空")

            if not self._validate_token(access_token):
                raise LynseAPIError("API Key 认证失败：返回的 Token 格式无效")

            self._save_token(access_token)
            return access_token

        except requests.RequestException as e:
            raise LynseAPIError(f"网络错误：无法连接到 API 服务器 - {e}")
        except json.JSONDecodeError:
            raise LynseAPIError("API Key 认证失败：服务器返回格式错误")

    def _get_token(self, refresh: bool = False) -> str:
        """获取有效 Token，支持自动刷新"""
        if not refresh:
            cached = self._get_cached_token()
            if cached:
                # 验证 Token 是否有效
                try:
                    test_url = f"{self.api_host}/api/business/customer/current"
                    test_headers = {
                        'Authorization': cached,
                        'X-API-Key': self.api_key
                    }
                    test_response = requests.get(test_url, headers=test_headers, timeout=10)
                    if test_response.status_code == 200:
                        self._access_token = cached
                        return cached
                except Exception:
                    pass  # Token 无效，刷新

        # 刷新 Token
        self._access_token = self._refresh_token()
        return self._access_token

    def _check_http_error(self, http_code: int, response_text: str):
        """检查 HTTP 错误并抛出异常"""
        if http_code == 200:
            return

        message = self.HTTP_ERROR_MESSAGES.get(http_code)
        if message:
            raise LynseAPIError(message, http_code=http_code)

        # 未知错误
        error_msg = f"API 请求失败 (HTTP {http_code})"
        if response_text:
            error_msg += f" - {response_text}"
        raise LynseAPIError(error_msg, http_code=http_code)

    def _check_owner_id(self, token: str):
        """验证 Owner ID"""
        if not self.owner_id:
            return

        try:
            url = f"{self.api_host}/api/business/customer/current"
            headers = {
                'Authorization': token,
                'X-API-Key': self.api_key
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current_id = data.get('data', {}).get('id') or data.get('id')
                if current_id and current_id != self.owner_id:
                    raise LynseAPIError("抱歉，这是私密账户，我无法操作")
        except LynseAPIError:
            raise
        except Exception:
            pass  # 忽略验证错误，继续执行

    def _sanitize_param(self, param: str, allow_type: str = 'safe') -> str:
        """清理参数，防止注入"""
        if allow_type == 'digit':
            return re.sub(r'[^0-9]', '', str(param))
        elif allow_type == 'safe':
            # 移除危险字符
            return re.sub(r'[;$`]', '', str(param)).replace('..', '')
        return str(param)

    def _request(self, method: str, path: str,
                 headers: Dict[str, str] = None,
                 params: Dict[str, Any] = None,
                 json_data: Dict[str, Any] = None,
                 retry_count: int = 0) -> Dict[str, Any]:
        """
        发送 API 请求

        Args:
            method: HTTP 方法 (GET/POST/DELETE 等)
            path: API 路径（不含 api_host）
            headers: 额外请求头
            params: URL 参数
            json_data: JSON Body 数据
            retry_count: 重试次数

        Returns:
            解析后的 JSON 响应
        """
        url = f"{self.api_host}{path}"

        # 获取 Token
        token = self._get_token()

        # 构建请求头
        request_headers = {
            'Authorization': token,
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        if headers:
            request_headers.update(headers)

        try:
            response = requests.request(
                method,
                url,
                headers=request_headers,
                params=params,
                json=json_data,
                timeout=30
            )

            # 检查 HTTP 错误
            self._check_http_error(response.status_code, response.text)

            # 解析响应
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = {'raw': response.text}

            # 检查业务错误码
            code = data.get('code')
            if code and code != 200:
                message = data.get('message', '未知错误')
                raise LynseAPIError(f"API 错误：{message}", code=code)

            return data

        except LynseAPIError:
            raise
        except requests.RequestException as e:
            if retry_count < 2:
                # 网络错误，重试
                return self._request(method, path, headers, params, json_data, retry_count + 1)
            raise LynseAPIError(f"网络错误：{e}")

    # ==================== 业务方法 ====================

    def get_current_customer(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        return self._request('GET', '/api/business/customer/current')

    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """获取指定用户信息"""
        safe_id = self._sanitize_param(user_id, 'safe')
        return self._request('GET', '/api/business/sysUser/info',
                            headers={'id': safe_id})

    def get_user_points(self) -> Dict[str, Any]:
        """获取用户积分"""
        data = self.get_current_customer()
        points_data = data.get('data', {})
        return {
            'pointsAmount': points_data.get('pointsAmount', 0),
            'usedPointsAmount': points_data.get('usedPointsAmount', 0)
        }

    def get_user_phone(self) -> str:
        """获取用户手机号"""
        data = self.get_current_customer()
        phone = data.get('data', {}).get('phone', '')
        # 脱敏处理
        if len(phone) >= 11:
            return f"{phone[:3]}****{phone[7:]}"
        return phone

    # 文件管理
    def list_files(self) -> Dict[str, Any]:
        """获取文件列表"""
        return self._request('GET', '/api/business/file/list')

    def get_file_info(self, file_id: str) -> Dict[str, Any]:
        """获取文件详情"""
        safe_id = self._sanitize_param(file_id, 'digit')
        return self._request('GET', '/api/business/file/info',
                            params={'fileId': safe_id})

    def get_conclusion(self, file_id: str) -> Dict[str, Any]:
        """获取文件总结"""
        safe_id = self._sanitize_param(file_id, 'digit')
        return self._request('GET', '/api/business/file/conclusion/list',
                            params={'fileId': safe_id})

    def get_outline(self, file_id: str) -> Dict[str, Any]:
        """获取文件大纲"""
        safe_id = self._sanitize_param(file_id, 'digit')
        return self._request('GET', '/api/business/file/outline/get',
                            params={'fileId': safe_id})

    def export_outline(self, file_id: str) -> Dict[str, Any]:
        """导出大纲"""
        safe_id = self._sanitize_param(file_id, 'digit')
        return self._request('GET', '/api/business/file/outline/export',
                            params={'fileId': safe_id})

    def list_files_by_time_range(self, days: int = 7) -> Dict[str, Any]:
        """按时间范围查询文件"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        params = {
            'startTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'endTime': end_time.strftime('%Y-%m-%dT%H:%M:%S')
        }
        return self._request('GET', '/api/business/file/timeRange/list', params=params)

    def get_transcription_record(self, file_id: str) -> Dict[str, Any]:
        """获取转写记录"""
        safe_id = self._sanitize_param(file_id, 'digit')
        return self._request('GET', '/api/business/file/trans/get',
                            params={'fileId': safe_id})

    # AI 模型管理
    def get_ai_models(self) -> Dict[str, Any]:
        """获取 AI 模型列表"""
        return self._request('GET', '/api/business/ai/getAllAIModelList')

    def add_model(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """添加 AI 模型"""
        return self._request('POST', '/api/business/ai/addModel', json_data=model_data)

    def delete_model(self, model_id: str) -> Dict[str, Any]:
        """删除 AI 模型"""
        safe_id = self._sanitize_param(model_id, 'safe')
        return self._request('DELETE', '/api/business/ai/deleteModel',
                            headers={'id': safe_id})

    def edit_model(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """编辑 AI 模型"""
        return self._request('POST', '/api/business/ai/editModel', json_data=model_data)

    def enable_model(self, model_id: str, enabled: bool) -> Dict[str, Any]:
        """启用/禁用 AI 模型"""
        safe_id = self._sanitize_param(model_id, 'safe')
        enabled_str = 'true' if enabled else 'false'
        return self._request('POST', '/api/business/ai/enableModel',
                            headers={'id': safe_id, 'enabled': enabled_str})

    # 设备管理
    def get_device_page(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """分页获取设备列表"""
        safe_page = self._sanitize_param(str(page), 'digit')
        return self._request('GET', '/api/business/deviceMgt/page9',
                            headers={'pageNum': safe_page, 'pageSize': str(page_size)})

    def get_device_info(self, device_id: str) -> Dict[str, Any]:
        """获取设备详情"""
        safe_id = self._sanitize_param(device_id, 'safe')
        return self._request('GET', '/api/business/deviceMgt/info5',
                            headers={'id': safe_id})

    def unbind_device(self, device_id: str) -> Dict[str, Any]:
        """解绑设备"""
        safe_id = self._sanitize_param(device_id, 'safe')
        return self._request('POST', '/api/business/deviceMgt/unbind',
                            headers={'id': safe_id})

    # 用户管理
    def get_current_user(self) -> Dict[str, Any]:
        """获取当前系统用户"""
        return self._request('GET', '/api/business/sysUser/current')

    def add_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """添加用户"""
        return self._request('POST', '/api/business/sysUser/add2', json_data=user_data)

    def edit_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """编辑用户"""
        return self._request('POST', '/api/business/sysUser/edit1', json_data=user_data)

    def remove_user(self, user_id: str) -> Dict[str, Any]:
        """删除用户"""
        safe_id = self._sanitize_param(user_id, 'safe')
        return self._request('POST', '/api/business/sysUser/remove',
                            headers={'id': safe_id})

    # 登录相关
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """用户名密码登录"""
        return self._request('POST', '/api/business/sysLogin/login',
                            json_data={'username': username, 'password': password})

    def login_with_phone(self, phone: str, captcha: str) -> Dict[str, Any]:
        """手机号验证码登录"""
        return self._request('POST', '/api/business/sysLogin/login',
                            json_data={'phone': phone, 'captcha': captcha})

    def logout(self) -> Dict[str, Any]:
        """登出"""
        return self._request('POST', '/api/business/sysLogin/logout')

    # 消息管理
    def send_sms(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """发送短信"""
        return self._request('POST', '/api/business/message/sendSmsMessage',
                            json_data=message_data)

    def send_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """发送邮件"""
        return self._request('POST', '/api/business/message/sendEmailMessage',
                            json_data=email_data)

    # 系统管理
    def get_role_list(self) -> Dict[str, Any]:
        """获取角色列表"""
        return self._request('GET', '/api/business/sysRole/list1')

    def get_menu_tree(self) -> Dict[str, Any]:
        """获取菜单树"""
        return self._request('GET', '/api/business/sysMenu/tree')


def main():
    """CLI 入口函数"""
    if len(sys.argv) < 2:
        print("Lynse CLI v1.3.0 - 跨平台 Python 版")
        print("用法：python lynse.py <command> [参数...]")
        print("\n常用命令:")
        print("  getCurrentCustomer          - 当前用户信息")
        print("  getUserPoints               - 当前用户积分")
        print("  getUserPhone                - 当前用户手机号")
        print("  listFiles                   - 文件列表")
        print("  getFileInfo <id>            - 文件详情")
        print("  getConclusion <id>          - 文件总结")
        print("  getAiModels                 - AI 模型列表")
        print("  getDevicePage [页码]        - 设备列表")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    try:
        api = LynseAPI()

        # 命令路由
        if command == 'getCurrentCustomer':
            result = api.get_current_customer()
        elif command == 'getUserInfo':
            if len(args) < 1:
                print("错误：getUserInfo 需要用户 ID 参数", file=sys.stderr)
                sys.exit(1)
            result = api.get_user_info(args[0])
        elif command == 'getUserPoints':
            result = api.get_user_points()
        elif command == 'getUserPhone':
            result = {'phone': api.get_user_phone()}
        elif command == 'listFiles':
            result = api.list_files()
        elif command == 'getFileInfo':
            if len(args) < 1:
                print("错误：getFileInfo 需要文件 ID 参数", file=sys.stderr)
                sys.exit(1)
            result = api.get_file_info(args[0])
        elif command == 'getConclusion' or command == 'getConclusionList':
            if len(args) < 1:
                print("错误：getConclusion 需要文件 ID 参数", file=sys.stderr)
                sys.exit(1)
            result = api.get_conclusion(args[0])
        elif command == 'getOutline':
            if len(args) < 1:
                print("错误：getOutline 需要文件 ID 参数", file=sys.stderr)
                sys.exit(1)
            result = api.get_outline(args[0])
        elif command == 'exportOutline':
            if len(args) < 1:
                print("错误：exportOutline 需要文件 ID 参数", file=sys.stderr)
                sys.exit(1)
            result = api.export_outline(args[0])
        elif command == 'listFilesByTimeRange':
            days = int(args[0]) if args else 7
            result = api.list_files_by_time_range(days)
        elif command == 'getTranscriptionRecord':
            if len(args) < 1:
                print("错误：getTranscriptionRecord 需要文件 ID 参数", file=sys.stderr)
                sys.exit(1)
            result = api.get_transcription_record(args[0])
        elif command == 'getAiModels':
            result = api.get_ai_models()
        elif command == 'getDevicePage':
            page = int(args[0]) if args else 1
            result = api.get_device_page(page)
        elif command == 'getDeviceInfo':
            if len(args) < 1:
                print("错误：getDeviceInfo 需要设备 ID 参数", file=sys.stderr)
                sys.exit(1)
            result = api.get_device_info(args[0])
        elif command == 'getCurrentUser':
            result = api.get_current_user()
        elif command == 'getRoleList':
            result = api.get_role_list()
        elif command == 'getMenuTree':
            result = api.get_menu_tree()
        elif command == 'login':
            if len(args) < 2:
                print("错误：login 需要用户名和密码参数", file=sys.stderr)
                sys.exit(1)
            result = api.login(args[0], args[1])
        elif command == 'logout':
            result = api.logout()
        else:
            print(f"错误：不支持的命令 '{command}'", file=sys.stderr)
            print("\n支持的命令:")
            print("  getCurrentCustomer, getUserInfo, getUserPoints, getUserPhone,")
            print("  listFiles, getFileInfo, getConclusion, getOutline, exportOutline,")
            print("  getAiModels, getDevicePage, getDeviceInfo, getCurrentUser,")
            print("  getRoleList, getMenuTree, login, logout")
            sys.exit(1)

        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except LynseAPIError as e:
        print(f"错误：{e.message}", file=sys.stderr)
        sys.exit(e.http_code or e.code or 1)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
