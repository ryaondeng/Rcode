from __future__ import annotations

from pathlib import Path

from rcode.core.tools.base import BaseTool, ToolResult
from rcode.core.tools.builtin.path_utils import safe_path

_MAX_ENTRIES = 200
_MAX_DEPTH = 4


class ListDirTool(BaseTool):
    """列出目录内容。"""
    name = "list_dir"
    description = "List directory contents"
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Directory path", "default": "."},
            "max_depth": {"type": "integer", "description": "Max depth", "default": 2},
        },
    }

    async def invoke(self, params: dict) -> ToolResult:
        path = safe_path(params.get("path", "."))
        if not path.exists():
            return ToolResult(content=f"Not found: {params.get('path', '.')}", is_error=True)
        if not path.is_dir():
            return ToolResult(content=f"Not a directory: {params.get('path', '.')}", is_error=True)

        max_depth = min(params.get("max_depth", 2), _MAX_DEPTH)
        entries: list[str] = []

        def walk(dir_path: Path, depth: int, prefix: str = "") -> None:
            if depth > max_depth:
                return
            try:
                items = sorted(dir_path.iterdir())
            except PermissionError:
                return
            for i, item in enumerate(items):
                if len(entries) >= _MAX_ENTRIES:
                    entries.append(f"{prefix}... (truncated)")
                    return
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                entries.append(f"{prefix}{connector}{item.name}{'/' if item.is_dir() else ''}")
                if item.is_dir():
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    walk(item, depth + 1, new_prefix)

        walk(path, 0)
        return ToolResult(content="\n".join(entries) or "(empty directory)")
