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
- **AgentLoop**：Think → Act → Observe 循环，事件驱动，不含 UI 代码

## 开发命令

```bash
uv run rcode run --goal "xxx"  # 执行 Agent 任务
uv run rcode ping              # 测试连接
```

## 测试

```bash
uv run python -m pytest tests/unit/ -v  # 单元测试
uv run python -m pytest tests/ -v       # 全部测试
```

原则：先增量测试相关模块，通过后再跑全部测试。

## 提交规范

- 格式：`feat:`、`fix:`、`docs:`、`test:`、`refactor:`
- 版本：用户手动打 tag，不在提交信息中写版本号

## 注释规范

- 复杂类/函数：上方加一句话说明
- 公共 API：添加 Args/Returns
- 简单逻辑：不加注释

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

完成9阶段开发后，添加本版本的changelog文档，在Rcode/docs/changelog下，参考之前的文档格式

### ⚠️ 强制规则

**每完成一个阶段，必须更新对应的 spec 文档！**

| 阶段 | 必须更新的文档 |
|------|----------------|
| 实现阶段完成后 | 08-commit.md（任务打勾） |
| 单元测试完成后 | 04-unit-test-plan.md |
| 集成测试完成后 | 05-integration-test-plan.md |
| Code Review 完成后 | 06-code-review-report.md |
| 文档更新完成后 | 07-docs-update-plan.md |
| 最后 | 00-index.md（更新状态） |

**不要跳过 spec 文档更新！**

### ⚠️ 开发检查清单

每次开发新功能时，必须按顺序完成：

1. **需求阶段**：更新 01-requirements.md
2. **设计阶段**：更新 02-design.md + 03-implementation-plan.md
3. **实现阶段**：
   - TDD：先写测试再写代码
   - 每完成一个任务，在 08-commit.md 中打勾
   - 运行增量测试，确保通过
4. **测试阶段**：
   - 运行全部单元测试
   - 检查增量覆盖率 ≥ 80%
   - 更新 04-unit-test-plan.md（含覆盖率数据）
5. **文档阶段**：
   - 更新 07-docs-update-plan.md
   - 生成 `docs/changelog/v{版本号}.md`
6. **提交阶段**：
   - 提交代码（版本号只在核心实现提交中加）
   - 更新 00-index.md

### 重要原则

- **开发以 spec 文档为准**
- 每完成一个任务，更新对应的 spec 文档
- 代码实现必须与 spec 文档保持一致
- **增量覆盖率 ≥ 80%，否则不进入下一阶段，除非得到用户确认跳过**
- **changelog 文档必须在提交前生成**
