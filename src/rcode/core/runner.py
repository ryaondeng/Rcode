from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from rcode.core.config import RcodeConfig
from rcode.core.context import ExecutionContext
from rcode.core.events.bus import EventBus
from rcode.core.events.writer import TraceEventSubscriber
from rcode.core.llm.provider import AnthropicProvider
from rcode.core.loop import AgentLoop
from rcode.core.tools.builtin.bash import BashTool
from rcode.core.tools.builtin.read_file import ReadFileTool
from rcode.core.tools.builtin.write_file import WriteFileTool
from rcode.core.tools.builtin.edit_file import EditFileTool
from rcode.core.tools.builtin.list_dir import ListDirTool
from rcode.core.tools.builtin.glob import GlobTool
from rcode.core.tools.registry import ToolRegistry
from rcode.core.trace.provider import TracingProvider
from rcode.core.trace.writer import TraceWriter


class _EventPrinter:
    """将关键事件打印到终端。"""

    def __init__(self):
        self._run_start = 0
        self._step = 0

    def __call__(self, event):
        import time
        from datetime import datetime
        from rcode.core.events.types import (
            RunStartedEvent, RunFinishedEvent,
            StepStartedEvent,
            ToolCallStartedEvent, ToolCallFinishedEvent,
            LlmCallStartedEvent,
        )

        now = datetime.now().strftime("%H:%M:%S")

        if isinstance(event, RunStartedEvent):
            self._run_start = time.monotonic()
            print(f"Task: {event.goal}\n")

        elif isinstance(event, StepStartedEvent):
            self._step = event.step

        elif isinstance(event, LlmCallStartedEvent):
            print(f"{now} | Step {event.step} | [LLM] chat | ...")

        elif isinstance(event, ToolCallStartedEvent):
            args_str = str(event.params)[:50] if event.params else ""
            print(f"{now} | [Tool] {event.tool_name} | ... | Args: {args_str}")

        elif isinstance(event, ToolCallFinishedEvent):
            if event.tool_result:
                # 截断显示
                display = event.tool_result[:150]
                if len(event.tool_result) > 150:
                    display += "..."
                print(f"{now} | Output: {display}")

        elif isinstance(event, RunFinishedEvent):
            elapsed = time.monotonic() - self._run_start
            print(f"\nDone ({elapsed:.2f}s)")


@dataclass
class RunOutcome:
    """Agent 运行结果。"""
    status: str  # "success" | "failed"
    result: str  # 结果内容


class AgentRunner:
    """Agent 运行器，组装所有依赖并执行任务。"""

    def __init__(self, config: RcodeConfig) -> None:
        self._config = config
        self._provider = AnthropicProvider()
        self._registry = ToolRegistry()
        self._bus = EventBus()
        self._trace: TraceWriter | None = None
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
        """执行 Agent 任务。"""
        run_id = f"run_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        context = ExecutionContext(goal=goal, run_id=run_id)

        # 初始化 Trace
        trace_path = Path(".traces") / f"{run_id}.jsonl"
        self._trace = TraceWriter(trace_path)
        await self._trace.start()

        # 用 TracingProvider 包裹真实 provider
        traced_provider = TracingProvider(self._provider, self._trace)

        # 订阅事件打印
        self._bus.subscribe(_EventPrinter())

        # 订阅事件写入 Trace
        self._bus.subscribe(TraceEventSubscriber(self._trace))

        loop = AgentLoop(traced_provider, self._registry, self._bus)

        try:
            await loop.run(context)
            return RunOutcome(
                status=context.status,
                result=context.result or "",
            )
        except Exception as e:
            return RunOutcome(status="failed", result=str(e))
        finally:
            await self._trace.stop()
