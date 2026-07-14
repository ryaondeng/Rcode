from __future__ import annotations

import asyncio
import sys

from rcode.core.config import RcodeConfig
from rcode.core.runner import AgentRunner


def cmd_run(goal: str, config: RcodeConfig) -> None:
    try:
        asyncio.run(_run(goal, config))
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)


async def _run(goal: str, config: RcodeConfig) -> str:
    runner = AgentRunner(config)
    outcome = await runner.run(goal)

    if outcome.status == "success":
        return outcome.result
    else:
        print(f"Error: {outcome.result}", file=sys.stderr)
        sys.exit(1)
