# v0.3 工具扩展 — 设计文档

> Spec: `20260712-v03-tool-extension`
> 阶段：设计规划
> 日期：2026-07-12
> 状态：待确认

## 1. 设计目标

扩展内置工具，提升 Agent 的文件操作能力。

**核心原则**：
- 工具原子化：每个工具只做一件事
- 路径安全：safe_path() 防止路径逃逸
- 输出控制：限制输出大小

## 2. 工作目录

```python
import os
from pathlib import Path

# 工作目录：优先从环境变量读取，否则使用当前目录
WORKDIR = Path(os.environ.get("RCODE_WORKDIR", ".")).resolve()
```

## 3. 路径安全

```python
def safe_path(path: str, workdir: Path) -> Path:
    """验证路径在工作目录内，防止路径逃逸。"""
    resolved = (workdir / path).resolve()
    if not resolved.is_relative_to(workdir.resolve()):
        raise ValueError(f"Path escapes workspace: {path}")
    return resolved
```

## 4. 工具设计

### 4.1 工具清单

| 工具 | 功能 | 安全机制 | 输出限制 |
|------|------|----------|----------|
| `bash` | 执行命令 | 超时保护 | 50KB |
| `read_file` | 读取文件 | safe_path | 512KB |
| `write_file` | 写入文件 | safe_path | 1MB |
| `list_dir` | 列出目录 | safe_path + 深度限制 | 200 条目 |
| `edit_file` | 文本替换 | safe_path | - |
| `glob` | 文件匹配 | safe_path + 结果校验 | 100 文件 |

### 4.2 工具设计原则

| 工具 | 选择理由 |
|------|----------|
| `bash` | 执行系统命令，最基础的能力 |
| `read_file` | 读取代码和配置文件，了解项目内容 |
| `write_file` | 创建和修改文件，支持自动创建目录 |
| `list_dir` | 了解项目结构，树状展示 |
| `edit_file` | 精确编辑，比 write_file 更安全 |
| `glob` | 查找文件，支持模式匹配 |

## 5. 目录结构

```
src/rcode/core/tools/builtin/
├── __init__.py
├── bash.py          # 已有
├── path_utils.py    # 新增：路径安全
├── read_file.py     # 新增：文件读取
├── write_file.py    # 新增：文件写入
├── list_dir.py      # 新增：目录列表
├── edit_file.py     # 新增：文件编辑
└── glob.py          # 新增：文件匹配
```