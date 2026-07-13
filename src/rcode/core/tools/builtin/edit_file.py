from __future__ import annotations

from rcode.core.tools.base import BaseTool, ToolResult
from rcode.core.tools.builtin.path_utils import safe_path


class EditFileTool(BaseTool):
    """通过替换文本编辑文件。"""
    name = "edit_file"
    description = "Edit file by replacing text"
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path"},
            "old_text": {"type": "string", "description": "Text to replace"},
            "new_text": {"type": "string", "description": "Replacement text"},
        },
        "required": ["path", "old_text", "new_text"],
    }

    async def invoke(self, params: dict) -> ToolResult:
        path = safe_path(params["path"])
        if not path.exists():
            return ToolResult(content=f"File not found: {params['path']}", is_error=True)

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return ToolResult(content=f"Cannot read binary file: {params['path']}", is_error=True)

        old_text = params["old_text"]
        new_text = params["new_text"]

        if old_text not in content:
            return ToolResult(content="Text not found in file", is_error=True)

        new_content = content.replace(old_text, new_text, 1)  # 只替换第一次出现
        path.write_text(new_content, encoding="utf-8")
        return ToolResult(content=f"Replaced text in {params['path']}")
