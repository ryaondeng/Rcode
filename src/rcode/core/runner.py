from __future__ import annotations

import time
import uuid
from dataclasses import dataclass

from rcode.core.config import RcodeConfig
from rcode.core.context import ExecutionContext
from rcode.core.llm.provider import AnthropicProvider
from rcode.core.loop import AgentLoop
from rcode.core.tools.builtin.bash import BashTool
from rcode.core.tools.registry import ToolRegistry


@dataclass
class RunOutcome:
    status: str
    result: str


class AgentRunner:
    def __init__(self, config: RcodeConfig) -> None:
        self._config = config
        self._provider = AnthropicProvider()
        self._registry = ToolRegistry()
        self._register_builtin_tools()

    def _register_builtin_tools(self) -> None:
        self._registry.register(BashTool())

    async def run(self, goal: str) -> RunOutcome:
        run_id = f"run_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        context = ExecutionContext(goal=goal, run_id=run_id)
        loop = AgentLoop(self._provider, self._registry)

        try:
            await loop.run(context)
            return RunOutcome(
                status=context.status,
                result=context.result or "",
            )
        except Exception as e:
            return RunOutcome(status="failed", result=str(e))
