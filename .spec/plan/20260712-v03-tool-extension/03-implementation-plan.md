# v0.3 工具扩展 — 实现计划

> Spec: `20260712-v03-tool-extension`
> 阶段：设计规划
> 日期：2026-07-12
> 状态：待确认

## 任务拆解

### 阶段一：基础设施

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T1 | 创建 `core/tools/builtin/path_utils.py`（safe_path） | 10min | [ ] |
| T2 | 更新 `core/tools/builtin/__init__.py` | 5min | [ ] |

### 阶段二：文件操作工具

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T3 | 实现 `core/tools/builtin/read_file.py` | 20min | [ ] |
| T4 | 实现 `core/tools/builtin/write_file.py` | 20min | [ ] |
| T5 | 实现 `core/tools/builtin/edit_file.py` | 25min | [ ] |

### 阶段三：目录操作工具

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T6 | 实现 `core/tools/builtin/list_dir.py` | 25min | [ ] |
| T7 | 实现 `core/tools/builtin/glob.py` | 20min | [ ] |

### 阶段四：集成

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T8 | 更新 `runner.py` 注册新工具 | 10min | [ ] |
| T9 | 更新 `core/tools/builtin/__init__.py` 导出 | 5min | [ ] |

### 阶段五：测试

| 任务 | 描述 | 预计时间 | 状态 |
|------|------|----------|------|
| T10 | 编写 `test_path_utils.py` | 15min | [ ] |
| T11 | 编写 `test_read_file.py` | 20min | [ ] |
| T12 | 编写 `test_write_file.py` | 20min | [ ] |
| T13 | 编写 `test_edit_file.py` | 20min | [ ] |
| T14 | 编写 `test_list_dir.py` | 20min | [ ] |
| T15 | 编写 `test_glob.py` | 20min | [ ] |
| T16 | 运行所有测试 | 10min | [ ] |

## 预计总时间

| 阶段 | 时间 |
|------|------|
| 阶段一：基础设施 | 15min |
| 阶段二：文件操作工具 | 65min |
| 阶段三：目录操作工具 | 45min |
| 阶段四：集成 | 15min |
| 阶段五：测试 | 115min |
| **总计** | **255min（4.25小时）** |