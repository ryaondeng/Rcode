# 工具系统设计

## 核心概念

工具系统采用**注册表模式**，所有工具继承 `BaseTool` 基类，通过 `ToolRegistry` 统一管理。

## 工具基类

```python
class BaseTool(ABC):
    name: str
    description: str
    input_schema: dict
    
    @abstractmethod
    async def invoke(self, params: dict) -> ToolResult: ...
```

## 工具注册表

```python
class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)
    
    def tool_schemas(self) -> list[dict]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self._tools.values()
        ]
```

## 工具调用流程

```
1. LLM 返回 tool_use
2. invoke_tool() 查找工具
3. 参数校验
4. 权限检查（可选）
5. 执行工具
6. 返回 ToolResult
```

## 内置工具

| 工具 | 说明 |
|------|------|
| `bash` | 执行 shell 命令 |
| `read_file` | 读取文件内容 |
| `write_file` | 写入文件 |
| `list_dir` | 列出目录内容 |
| `task_create` | 创建任务 |
| `task_list` | 列出任务 |
| `task_update` | 更新任务状态 |

## 路径安全

所有文件操作都通过 `safe_path()` 验证，防止路径逃逸：

```python
def safe_path(path: str, workdir: Path) -> Path:
    resolved = (workdir / path).resolve()
    if not resolved.is_relative_to(workdir.resolve()):
        raise ValueError(f"Path escapes workspace: {path}")
    return resolved
```

## 相关文件

- `src/rcode/core/tools/base.py`：工具基类
- `src/rcode/core/tools/registry.py`：工具注册表
- `src/rcode/core/tools/invocation.py`：工具调用逻辑
- `src/rcode/core/tools/builtin/`：内置工具实现