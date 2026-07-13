# v0.3 工具扩展 — 单元测试报告

> Spec: `20260712-v03-tool-extension`
> 阶段：单元测试
> 日期：2026-07-12

## 1. 测试概览

| 指标 | 数值 |
|------|------|
| 总用例数 | 60 |
| 通过 | 60 |
| 失败 | 0 |
| 跳过 | 0 |
| 整体覆盖率 | 84% |

## 2. 测试用例清单

### 2.1 路径安全（5 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_safe_path_within_workdir | 正常路径 | 返回绝对路径 | [x] |
| test_safe_path_with_subdirectory | 子目录路径 | 返回绝对路径 | [x] |
| test_safe_path_escape_raises | 路径逃逸 | 抛出 ValueError | [x] |
| test_safe_path_absolute_escape_raises | 绝对路径逃逸 | 抛出 ValueError | [x] |
| test_get_workdir_default | 默认工作目录 | 返回绝对路径 | [x] |

### 2.2 文件读取（4 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_read_file_success | 读取文件 | 返回内容 | [x] |
| test_read_file_with_limit | 限制行数 | 返回指定行数 | [x] |
| test_read_file_not_found | 文件不存在 | 返回错误 | [x] |
| test_read_file_directory | 读取目录 | 返回错误 | [x] |

### 2.3 文件写入（3 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_write_file_success | 写入文件 | 文件创建成功 | [x] |
| test_write_file_creates_parent_dir | 创建父目录 | 目录自动创建 | [x] |
| test_write_file_overwrites | 覆盖文件 | 文件内容更新 | [x] |

### 2.4 文件编辑（4 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_edit_file_success | 替换文本 | 文本替换成功 | [x] |
| test_edit_file_only_first_occurrence | 只替换第一次 | 只替换首次出现 | [x] |
| test_edit_file_not_found | 文件不存在 | 返回错误 | [x] |
| test_edit_file_text_not_found | 文本不存在 | 返回错误 | [x] |

### 2.5 目录列表（4 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_list_dir_success | 列出目录 | 返回文件列表 | [x] |
| test_list_dir_with_depth | 限制深度 | 不显示子目录内容 | [x] |
| test_list_dir_not_found | 目录不存在 | 返回错误 | [x] |
| test_list_dir_empty | 空目录 | 返回 empty | [x] |

### 2.6 文件匹配（4 个）

| 用例名 | 测试场景 | 期望结果 | 状态 |
|--------|----------|----------|------|
| test_glob_py_files | 匹配 .py 文件 | 返回 py 文件 | [x] |
| test_glob_recursive | 递归匹配 | 返回嵌套文件 | [x] |
| test_glob_no_match | 无匹配 | 返回 no files found | [x] |
| test_glob_with_path | 指定路径 | 在指定路径匹配 | [x] |

## 3. 覆盖率详情

| 模块 | 文件 | 覆盖率 |
|------|------|--------|
| path_utils | core/tools/builtin/path_utils.py | 100% |
| read_file | core/tools/builtin/read_file.py | 92% |
| write_file | core/tools/builtin/write_file.py | 84% |
| edit_file | core/tools/builtin/edit_file.py | 91% |
| list_dir | core/tools/builtin/list_dir.py | 86% |
| glob | core/tools/builtin/glob.py | 85% |

## 4. 失败用例

无

## 5. 测试执行命令

```bash
# 运行所有单元测试
uv run python -m pytest tests/unit/ -v

# 运行工具测试
uv run python -m pytest tests/unit/test_tools/ -v
```