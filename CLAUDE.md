# CLAUDE.md

## 设计理念

```
Agent = Model (LLM) + Harness (运行环境)
```

Rcode 实现的是 **Harness**：工具、权限、上下文管理、会话续航。模型是驱动者，Harness 是载体。

## 架构

```
rcode-core (daemon)  ←→  JSON-RPC 2.0 NDJSON  ←→  rcode (CLI/TUI/Web)
```

- **双进程**：故障隔离、多客户端、状态持久化
- **JSON-RPC 2.0 + NDJSON**：成熟标准、便于流式读取、类型安全

## 开发目标

参考 Claude Code 核心架构，实现完整的 Agent Harness：
- Agent Loop（Think → Act → Observe）
- 工具系统、权限审批、事件流
- 会话管理、上下文压缩、记忆系统
- 子 Agent、技能加载、MCP 集成

**不要偏离**：我们做的是 Harness，不是 Model。不要花时间在模型训练或 prompt engineering 上。

## 开发命令

```bash
uv run rcode-core              # 启动 Core
uv run rcode ping              # 测试连接
uv run rcode run --goal "xxx"  # 执行 Agent 任务
uv run python -m pytest tests/ -v  # 运行测试
```

## 提交规范

- 日常：`feat:`、`fix:`、`docs:`、`test:`、`refactor:`
- 版本：用户手动打 tag，不在提交信息中写版本号

## 注释规范

- **复杂类**：类定义上方加一句话说明职责
- **复杂函数**：函数定义上方加一句话说明功能
- **公共 API**：添加 Args/Returns 说明参数和返回值
- **不要**：简单函数、getter/setter、明显逻辑不加注释

原则：一句话能说清楚的，不写两句话；复杂逻辑加注释，简单逻辑不加。

## 版本规划

v0.1 骨架与协议 → v0.2 Agent 闭环 → v0.3 工具扩展 → ... → v0.14 MCP 集成

详见 `docs/versions/` 目录。

## Spec 驱动开发

本项目使用 spec-dev-workflow 进行规格驱动开发。

### 调用方式

| 触发词 | 命令 |
|--------|------|
| 做一个功能、帮我规划、写个设计、spec开发 | `/spec-dev-workflow` |
| 检查spec、验证spec | `/spec-check` |

### Spec 文档路径

- 文档存放：`.spec/plan/YYYYMMDD-英文功能名/`
- 总索引：`.spec/plan/YYYYMMDD-英文功能名/00-index.md`

### 八阶段工作流

1. 需求阐述 → 01-requirements.md
2. 设计规划 → 02-design.md + 03-implementation-plan.md
3. 实现 → 源代码 + 测试（TDD）
4. 单元测试 → 04-unit-test-plan.md（覆盖率 ≥ 80%）
5. 集成测试 → 05-integration-test-plan.md
6. Code Review → 06-code-review-report.md
7. 文档更新 → 07-docs-update-plan.md
8. 完成记录 → 08-commit.md

### 重要原则

- **开发以 spec 文档为准**
- 每完成一个任务，更新对应的 spec 文档
- 代码实现必须与 spec 文档保持一致
