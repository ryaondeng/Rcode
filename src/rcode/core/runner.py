from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

from rcode.core.config import RcodeConfig
from rcode.core.context import ExecutionContext
from rcode.core.events.bus import EventBus
from rcode.core.llm.provider import AnthropicProvider
from rcode.core.loop import AgentLoop
from rcode.core.tools.builtin.bash import BashTool
from rcode.core.tools.builtin.read_file import ReadFileTool
from rcode.core.tools.builtin.write_file import WriteFileTool
from rcode.core.tools.builtin.edit_file import EditFileTool
from rcode.core.tools.builtin.list_dir import ListDirTool
from rcode.core.tools.builtin.glob import GlobTool
from rcode.core.tools.registry import ToolRegistry


@dataclass
class RunOutcome:
    """Agent 运行结果。"""
    status: str  # "success" | "failed"
    result: str  # 结果内容


class AgentRunner:
    """Agent 运行器，组装所有依赖并执行任务。

    职责：
    1. 初始化 LLM Provider
    2. 注册内置工具
    3. 创建 ExecutionContext 和 AgentLoop
    4. 执行任务并返回结果
    """

    def __init__(self, config: RcodeConfig) -> None:
        self._config = config
        self._provider = AnthropicProvider()
        self._registry = ToolRegistry()
        self._bus = EventBus()
        self._register_builtin_tools()

    def _register_builtin_tools(self) -> None:
        """注册内置工具。"""
        self._registry.register(BashTool())
        self._registry.register(ReadFileTool())
        self._registry.register(WriteFileTool())
        self._registry.register(EditFileTool())
        self._registry.register(ListDirTool())
        self._registry.register(GlobTool())

    async def run(self, goal: str) -> RunOutcome:
        """执行 Agent 任务。

        Args:
            goal: 用户目标描述

        Returns:
            RunOutcome: 包含状态和结果
        """
        run_id = f"run_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        context = ExecutionContext(goal=goal, run_id=run_id)
        loop = AgentLoop(self._provider, self._registry, self._bus)

        try:
            await loop.run(context)
            return RunOutcome(
                status=context.status,
                result=context.result or "",
            )
        except Exception as e:
            return RunOutcome(status="failed", result=str(e))
