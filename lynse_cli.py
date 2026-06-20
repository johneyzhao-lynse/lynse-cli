#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lynse Unified CLI - 统一命令入口
同时支持 lynse-cli-a 和 lynse-cli-b 功能，以及友好命令别名。

用法：
    python lynse_cli.py <command> [参数...]

示例：
    python lynse_cli.py me
    python lynse_cli.py meetings list --days 7
    python lynse_cli.py getCurrentCustomer
"""

import os
import sys
import json
from pathlib import Path

# 导入核心 API 模块
from lynse import (
    LynseAPI, LynseAPIError,
    _resolve_alias, _parse_global_flags, _format_output, _resolve_exit_code,
    _ALIAS_HANDLERS, _ALIAS_INFO, CLI_VERSION,
    EXIT_SUCCESS, EXIT_INVALID, EXIT_AUTH,
    _handle_auth_command, _print_help,
)


class LynseUnifiedCLI:
    """Lynse 统一 CLI - 路由到合适的处理逻辑"""

    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        self.api: LynseAPI = None

        # CLI 版本检测
        self.cli_a_path = self.script_dir / 'lynse-cli-a' / 'client.sh'
        self.cli_b_path = self.script_dir / 'lynse-cli-b' / 'client.sh'

    def _check_cli_version(self) -> str:
        """检测可用的 CLI 版本"""
        if self.cli_b_path.exists() and os.access(self.cli_b_path, os.X_OK):
            return 'b'
        elif self.cli_a_path.exists() and os.access(self.cli_a_path, os.X_OK):
            return 'a'
        else:
            return 'none'

    def _init_api(self):
        """初始化 API 客户端"""
        if self.api is None:
            self.api = LynseAPI()

    def _run_cli_a(self, command: str, args: list) -> int:
        """运行 CLI A（基础版）"""
        supported_commands = {
            'bind', 'exchangeToken', 'generateApiKey', 'isLogin',
            'login', 'logout', 'refreshToken', 'register', 'render',
            'revokeApiKey', 'terminate', 'updatePhone', 'updatePwd',
            'verifyWechatSignature', 'getPoolStatus', 'smsCode'
        }
        if command not in supported_commands:
            print(f"Error: command '{command}' not available in CLI A, please upgrade to CLI B", file=sys.stderr)
            return EXIT_INVALID
        import subprocess
        cmd_args = [str(self.cli_a_path), command] + args
        try:
            result = subprocess.run(cmd_args, cwd=str(self.script_dir))
            return result.returncode
        except Exception as e:
            print(f"Error: failed to execute CLI A - {e}", file=sys.stderr)
            return EXIT_INVALID

    def _run_cli_b(self, command: str, args: list) -> int:
        """运行 CLI B（完整版）"""
        import subprocess
        cmd_args = [str(self.cli_b_path), command] + args
        try:
            result = subprocess.run(cmd_args, cwd=str(self.script_dir))
            return result.returncode
        except Exception as e:
            print(f"Error: failed to execute CLI B - {e}", file=sys.stderr)
            return EXIT_INVALID

    def _handle_python_command(self, command: str, args: list, flags: dict) -> int:
        """使用 Python API 处理命令，支持别名和输出格式。"""
        try:
            self._init_api()
            display_command = _ALIAS_INFO.get(command, command)

            # 尝试使用别名处理器
            if command in _ALIAS_HANDLERS:
                result = _ALIAS_HANDLERS[command](self.api, args)
                _format_output(result, display_command, flags)
                return EXIT_SUCCESS

            # 原有命令
            if command == 'getCurrentCustomer':
                result = self.api.get_current_customer()
            elif command == 'getUserInfo':
                if not args:
                    print("Error: getUserInfo requires a user ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.get_user_info(args[0])
            elif command == 'getUserPoints':
                result = self.api.get_user_points()
            elif command == 'getUserPhone':
                result = {'phone': self.api.get_user_phone()}
            elif command == 'refreshMembership':
                result = self.api.refresh_membership()
            elif command == 'listFiles':
                result = self.api.list_files()
            elif command == 'listFilesPaged':
                page_size = int(args[0]) if args else 100
                result = self.api.list_files_paged(page_size)
            elif command == 'searchFiles':
                if not args:
                    print("Error: searchFiles requires a keyword", file=sys.stderr); return EXIT_INVALID
                page = int(args[1]) if len(args) > 1 else 1
                page_size = int(args[2]) if len(args) > 2 else 20
                result = self.api.search_files(args[0], page=page, page_size=page_size)
            elif command == 'listTodos':
                if len(args) < 3:
                    print("Error: listTodos requires: <all|open|done> <pageNum> <pageSize>", file=sys.stderr)
                    return EXIT_INVALID
                result = self.api.list_todos(status=args[0].lower(), page_num=int(args[1]), page_size=int(args[2]))
            elif command == 'listAllTodos':
                result = self.api.list_all_todos()
            elif command == 'deleteTodos':
                if not args:
                    print("Error: deleteTodos requires todo IDs", file=sys.stderr); return EXIT_INVALID
                raw_ids = " ".join(args).strip()
                try:
                    parsed = json.loads(raw_ids)
                    todo_ids = parsed if isinstance(parsed, list) else [parsed]
                except json.JSONDecodeError:
                    todo_ids = [item.strip() for item in raw_ids.split(',') if item.strip()]
                result = self.api.delete_todos([str(item) for item in todo_ids])
            elif command == 'clearCompletedTodos':
                result = self.api.clear_completed_todos()
            elif command == 'getFileInfo':
                if not args:
                    print("Error: getFileInfo requires a file ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.get_file_info(args[0])
            elif command in ('getConclusion', 'getConclusionList'):
                if not args:
                    print("Error: getConclusion requires a file ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.get_conclusion(args[0])
            elif command == 'getOutline':
                if not args:
                    print("Error: getOutline requires a file ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.get_outline(args[0])
            elif command == 'exportOutline':
                if not args:
                    print("Error: exportOutline requires a file ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.export_outline(args[0])
            elif command == 'listFilesByTimeRange':
                days = int(args[0]) if args else 7
                result = self.api.list_files_by_time_range(days)
            elif command == 'listFolders':
                result = self.api.list_folders()
            elif command == 'createFolder':
                if not args:
                    print("Error: createFolder requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.create_folder(json.loads(args[0]))
            elif command == 'changeFolder':
                if not args:
                    print("Error: changeFolder requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.change_folder(json.loads(args[0]))
            elif command == 'getTranscriptionRecord':
                if not args:
                    print("Error: getTranscriptionRecord requires a file ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.get_transcription_record(args[0])
            elif command == 'renameSpeaker':
                if not args:
                    print("Error: renameSpeaker requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.rename_speaker(json.loads(args[0]))
            elif command == 'editSpeakerInfo':
                if not args:
                    print("Error: editSpeakerInfo requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.edit_speaker_info(json.loads(args[0]))
            elif command == 'getAiModels':
                result = self.api.get_ai_models()
            elif command == 'addModel':
                if not args:
                    print("Error: addModel requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.add_model(json.loads(args[0]))
            elif command == 'deleteModel':
                if not args:
                    print("Error: deleteModel requires a model ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.delete_model(args[0])
            elif command == 'editModel':
                if not args:
                    print("Error: editModel requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.edit_model(json.loads(args[0]))
            elif command == 'enableModel':
                if len(args) < 2:
                    print("Error: enableModel requires model ID and true/false", file=sys.stderr); return EXIT_INVALID
                result = self.api.enable_model(args[0], args[1].lower() in ('true', '1', 'yes'))
            elif command == 'getDevicePage':
                page = int(args[0]) if args else 1
                result = self.api.get_device_page(page)
            elif command == 'getMyDevices':
                result = self.api.get_my_devices()
            elif command == 'getDeviceInfo':
                if not args:
                    print("Error: getDeviceInfo requires a device ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.get_device_info(args[0])
            elif command == 'unbindDevice':
                if not args:
                    print("Error: unbindDevice requires a device ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.unbind_device(args[0])
            elif command == 'getCurrentUser':
                result = self.api.get_current_user()
            elif command == 'addUser':
                if not args:
                    print("Error: addUser requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.add_user(json.loads(args[0]))
            elif command == 'editUser':
                if not args:
                    print("Error: editUser requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.edit_user(json.loads(args[0]))
            elif command == 'removeUser':
                if not args:
                    print("Error: removeUser requires a user ID", file=sys.stderr); return EXIT_INVALID
                result = self.api.remove_user(args[0])
            elif command == 'login':
                if len(args) < 2:
                    print("Error: login requires username and password", file=sys.stderr); return EXIT_INVALID
                result = self.api.login(args[0], args[1])
            elif command == 'loginWithPhone':
                if len(args) < 2:
                    print("Error: loginWithPhone requires phone and captcha", file=sys.stderr); return EXIT_INVALID
                result = self.api.login_with_phone(args[0], args[1])
            elif command == 'logout':
                result = self.api.logout()
            elif command == 'sendSms':
                if not args:
                    print("Error: sendSms requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.send_sms(json.loads(args[0]))
            elif command == 'sendEmail':
                if not args:
                    print("Error: sendEmail requires JSON data", file=sys.stderr); return EXIT_INVALID
                result = self.api.send_email(json.loads(args[0]))
            elif command == 'getRoleList':
                result = self.api.get_role_list()
            elif command == 'getMenuTree':
                result = self.api.get_menu_tree()
            else:
                print(f"Error: unknown command '{command}'", file=sys.stderr)
                return EXIT_INVALID

            _format_output(result, display_command, flags)
            return EXIT_SUCCESS

        except LynseAPIError as e:
            print(f"Error: {e.message}", file=sys.stderr)
            return _resolve_exit_code(e)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON - {e}", file=sys.stderr)
            return EXIT_INVALID
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return EXIT_INVALID

    def run(self, args: list) -> int:
        """运行 CLI。"""
        if not args:
            _print_help()
            return EXIT_SUCCESS

        # 剥离全局标志
        flags, cli_args = _parse_global_flags(args)
        if not cli_args:
            _print_help()
            return EXIT_SUCCESS

        # 解析别名
        command, cmd_args, is_alias = _resolve_alias(cli_args[0], cli_args[1:])

        # 本地命令直接委托给 lynse.main
        if command in ('__version__', '__update__', '__doctor__'):
            from lynse import main as lynse_main
            sys.argv = ['lynse', cli_args[0]] + cli_args[1:]
            try:
                lynse_main()
            except SystemExit as e:
                return e.code or EXIT_SUCCESS
            return EXIT_SUCCESS

        if command.startswith('__auth_'):
            try:
                _handle_auth_command(command, cmd_args, flags)
            except SystemExit as e:
                return e.code or EXIT_SUCCESS
            return EXIT_SUCCESS

        # 检测 shell CLI 版本
        version = self._check_cli_version()

        # Python 命令集合（含别名解析后的命令）
        python_commands = {
            'getCurrentCustomer', 'getUserInfo', 'getUserPoints', 'getUserPhone', 'refreshMembership',
            'listFiles', 'listFilesPaged', 'searchFiles', 'listFilesByTimeRange',
            'listTodos', 'listAllTodos', 'deleteTodos', 'clearCompletedTodos',
            'getFileInfo', 'getConclusion', 'getOutline', 'exportOutline',
            'getTranscriptionRecord', 'renameSpeaker', 'editSpeakerInfo',
            'listFolders', 'createFolder', 'changeFolder',
            'getAiModels', 'addModel', 'deleteModel', 'editModel', 'enableModel',
            'getMyDevices', 'getDevicePage', 'getDeviceInfo', 'unbindDevice',
            'getCurrentUser', 'addUser', 'editUser', 'removeUser',
            'login', 'loginWithPhone', 'logout', 'sendSms', 'sendEmail',
            'getRoleList', 'getMenuTree',
        }

        # 别名解析后的命令始终走 Python 路径
        if is_alias or command in python_commands:
            return self._handle_python_command(command, cmd_args, flags)

        # 其他命令路由到 shell CLI
        if version == 'none':
            return self._handle_python_command(command, cmd_args, flags)
        elif version == 'b':
            return self._run_cli_b(command, cmd_args)
        else:
            return self._run_cli_a(command, cmd_args)


def main():
    """CLI 入口"""
    cli = LynseUnifiedCLI()
    sys.exit(cli.run(sys.argv[1:]))


if __name__ == '__main__':
    main()
