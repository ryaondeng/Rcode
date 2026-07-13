from __future__ import annotations

from rcode.core.tools.base import BaseTool, ToolResult
from rcode.core.tools.builtin.path_utils import safe_path

_MAX_CONTENT = 1048576  # 1MB


class WriteFileTool(BaseTool):
    """写入文件内容。"""
    name = "write_file"
    description = "Write file content"
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path"},
            "content": {"type": "string", "description": "File content"},
        },
        "required": ["path", "content"],
    }

    async def invoke(self, params: dict) -> ToolResult:
        path = safe_path(params["path"])
        content = params["content"]

        if len(content) > _MAX_CONTENT:
            return ToolResult(content="Content too large (max 1MB)", is_error=True)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return ToolResult(content=f"Written {len(content)} bytes to {params['path']}")
        except Exception as e:
            return ToolResult(content=f"Failed to write: {e}", is_error=True)
