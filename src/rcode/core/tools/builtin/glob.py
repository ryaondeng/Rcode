from __future__ import annotations

from rcode.core.tools.base import BaseTool, ToolResult
from rcode.core.tools.builtin.path_utils import get_workdir, safe_path

_MAX_MATCHES = 100


class GlobTool(BaseTool):
    """查找匹配模式的文件。"""
    name = "glob"
    description = "Find files matching a pattern"
    input_schema = {
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "Glob pattern (e.g., **/*.py)"},
            "path": {"type": "string", "description": "Base directory", "default": "."},
        },
        "required": ["pattern"],
    }

    async def invoke(self, params: dict) -> ToolResult:
        workdir = get_workdir()
        base_path = safe_path(params.get("path", "."))
        pattern = params["pattern"]

        if not base_path.exists():
            return ToolResult(content=f"Not found: {params.get('path', '.')}", is_error=True)

        matches: list[str] = []
        try:
            for match in base_path.glob(pattern):
                # 校验每个匹配结果
                if match.resolve().is_relative_to(workdir.resolve()):
                    matches.append(str(match.relative_to(workdir)))
                    if len(matches) >= _MAX_MATCHES:
                        break
        except Exception as e:
            return ToolResult(content=f"Glob error: {e}", is_error=True)

        if not matches:
            return ToolResult(content="No files found")

        return ToolResult(content="\n".join(matches))
