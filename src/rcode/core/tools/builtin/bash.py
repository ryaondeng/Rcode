from __future__ import annotations

import subprocess

from rcode.core.tools.base import BaseTool, ToolResult

_MAX_OUTPUT = 50000  # 输出最大字符数


class BashTool(BaseTool):
    """Bash 命令执行工具。

    功能：
    - 执行 bash 命令
    - 捕获 stdout 和 stderr
    - 超时保护（30s）
    - 输出截断（50KB）
    """
    name = "bash"
    description = "Execute a bash command"
    input_schema = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The bash command to execute",
            }
        },
        "required": ["command"],
    }

    async def invoke(self, params: dict) -> ToolResult:
        """执行 bash 命令。"""
        command = params.get("command", "")
        if not command:
            return ToolResult(content="No command provided", is_error=True)

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout + result.stderr
            if len(output) > _MAX_OUTPUT:
                output = output[:_MAX_OUTPUT] + "\n... (output truncated)"
            return ToolResult(content=output or "(no output)")
        except subprocess.TimeoutExpired:
            return ToolResult(
                content="Command timed out after 30s",
                is_error=True,
                error_type="timeout",
            )
