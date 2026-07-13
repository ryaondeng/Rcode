from __future__ import annotations

from rcode.core.tools.base import BaseTool, ToolResult
from rcode.core.tools.builtin.path_utils import safe_path

_MAX_OUTPUT = 512000  # 512KB


class ReadFileTool(BaseTool):
    """读取文件内容。"""
    name = "read_file"
    description = "Read file content"
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path"},
            "limit": {"type": "integer", "description": "Max lines to read", "default": 0},
        },
        "required": ["path"],
    }

    async def invoke(self, params: dict) -> ToolResult:
        path = safe_path(params["path"])
        if not path.exists():
            return ToolResult(content=f"File not found: {params['path']}", is_error=True)
        if path.is_dir():
            return ToolResult(content=f"Is a directory: {params['path']}", is_error=True)

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return ToolResult(content=f"Cannot read binary file: {params['path']}", is_error=True)

        limit = params.get("limit", 0)
        if limit > 0:
            lines = content.split("\n")
            content = "\n".join(lines[:limit])
            if len(lines) > limit:
                content += f"\n... ({len(lines) - limit} more lines)"

        return ToolResult(content=content[:_MAX_OUTPUT])
