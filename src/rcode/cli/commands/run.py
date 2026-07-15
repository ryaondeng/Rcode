from __future__ import annotations

import asyncio
import sys

from rcode.core.config import RcodeConfig


def cmd_run(goal: str, config: RcodeConfig, local: bool = False) -> None:
    try:
        asyncio.run(_run(goal, config, local))
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(1)


async def _run(goal: str, config: RcodeConfig, local: bool) -> str:
    if local:
        # 同进程模式
        from rcode.core.runner import AgentRunner
        runner = AgentRunner(config)
        outcome = await runner.run(goal)
    else:
        # IPC 模式
        from rcode.ipc.client import IpcClient
        client = IpcClient()
        try:
            await client.connect()
            result = await client.call("core.run", session_id="default", user_input=goal)
            run_id = result.get("result", {}).get("run_id")
            if run_id:
                outcome_data = await client.wait_for_result(run_id)
                return outcome_data.get("result", "")
            else:
                print("Error: Failed to get run_id", file=sys.stderr)
                sys.exit(1)
        finally:
            await client.close()

    if outcome.status == "success":
        return outcome.result
    else:
        print(f"Error: {outcome.result}", file=sys.stderr)
        sys.exit(1)
