# 工具接口

## BaseTool

所有工具的抽象基类。

```python
class BaseTool(ABC):
    name: str                    # 工具名称
    description: str             # 工具描述
    input_schema: dict           # 输入参数 schema
    
    @abstractmethod
    async def invoke(self, params: dict) -> ToolResult: ...
```

## ToolResult

工具执行结果。

```python
@dataclass
class ToolResult:
    content: str                 # 结果内容
    is_error: bool = False       # 是否错误
    error_type: str | None = None  # 错误类型
```

### 错误类型

| 类型 | 说明 |
|------|------|
| `runtime_error` | 运行时错误 |
| `timeout` | 执行超时 |
| `schema_error` | 参数错误 |
| `permission_denied` | 权限拒绝 |

## ToolRegistry

工具注册表。

```python
class ToolRegistry:
    def register(self, tool: BaseTool) -> None:
        """注册工具，同名覆盖"""
    
    def get(self, name: str) -> BaseTool | None:
        """按名称查找工具"""
    
    def tool_schemas(self) -> list[dict]:
        """返回所有工具的 Anthropic 格式 schema"""
```

## 内置工具

### BashTool

执行 shell 命令。

```python
class BashTool(BaseTool):
    name = "bash"
    description = "Execute a bash command"
    input_schema = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "命令"}
        },
        "required": ["command"]
    }
```

### ReadFileTool

读取文件内容。

```python
class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read file content"
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"}
        },
        "required": ["path"]
    }
```

### WriteFileTool

写入文件。

```python
class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Write file content"
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
            "content": {"type": "string", "description": "文件内容"}
        },
        "required": ["path", "content"]
    }
```

### EditFileTool

通过替换文本编辑文件。

```python
class EditFileTool(BaseTool):
    name = "edit_file"
    description = "Edit file by replacing text"
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
            "old_text": {"type": "string", "description": "要替换的文本"},
            "new_text": {"type": "string", "description": "替换后的文本"}
        },
        "required": ["path", "old_text", "new_text"]
    }
```

### ListDirTool

列出目录内容。

```python
class ListDirTool(BaseTool):
    name = "list_dir"
    description = "List directory contents"
    input_schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "目录路径", "default": "."},
            "max_depth": {"type": "integer", "description": "最大深度", "default": 2}
        }
    }
```

### GlobTool

查找匹配模式的文件。

```python
class GlobTool(BaseTool):
    name = "glob"
    description = "Find files matching a pattern"
    input_schema = {
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "Glob 模式 (如 **/*.py)"},
            "path": {"type": "string", "description": "基础目录", "default": "."}
        },
        "required": ["pattern"]
    }
```

## 路径安全

```python
def safe_path(path: str, workdir: Path | None = None) -> Path:
    """验证路径在工作目录内，防止路径逃逸。"""
    ...
```

所有文件操作工具都使用 `safe_path()` 校验路径安全。

## 工具调用

```python
async def invoke_tool(
    registry: ToolRegistry,
    tool_call: ToolCall,
    permission_manager: PermissionManager | None = None,
) -> ToolResult:
    """执行工具调用"""
```

## 相关文件

- `src/rcode/core/tools/base.py`
- `src/rcode/core/tools/registry.py`
- `src/rcode/core/tools/invocation.py`
- `src/rcode/core/tools/builtin/`