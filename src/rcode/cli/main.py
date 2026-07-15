from __future__ import annotations

import argparse
import asyncio
import sys
import time

from rcode.cli.commands.ping import cmd_ping
from rcode.cli.commands.core import cmd_core
from rcode.cli.commands.run import cmd_run
from rcode.core.config import get_config
from rcode.core.logging_setup import setup_logging


def cmd_core_start(config):
    """启动 Core 进程。"""
    from rcode.core.transport.socket_server import SocketServer
    from rcode.core.runner import AgentRunner

    server = SocketServer(host="127.0.0.1", port=7437)
    runner = AgentRunner(config)

    async def handle_run(params):
        session_id = params.get("session_id", "default")
        user_input = params.get("user_input", "")
        outcome = await runner.run(session_id, user_input)
        return {"run_id": f"run_{int(time.time())}", "status": outcome.status, "result": outcome.result}

    async def handle_ping(params):
        return {"status": "pong"}

    server.register("core.run", handle_run)
    server.register("core.ping", handle_ping)

    print("Starting core daemon...")
    asyncio.run(server.start())


def main() -> None:
    parser = argparse.ArgumentParser(prog="rcode", description="Rcode CLI")
    parser.add_argument("--version", action="store_true", help="Print version and exit")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("ping", help="Ping the core daemon")

    run_parser = subparsers.add_parser("run", help="Run an agent task")
    run_parser.add_argument("--goal", required=True, help="Goal for the agent to accomplish")
    run_parser.add_argument("--local", action="store_true", help="Run in local mode (no IPC)")

    core_parser = subparsers.add_parser("core", help="Manage the core daemon")
    core_sub = core_parser.add_subparsers(dest="core_command")
    core_sub.add_parser("start", help="Start the daemon")
    core_sub.add_parser("stop", help="Stop the running daemon")
    core_sub.add_parser("status", help="Show daemon status")

    args = parser.parse_args()

    if args.version:
        from rcode import __version__
        print(f"rcode {__version__}")
        return

    config = get_config()
    setup_logging(config)

    if args.command == "ping":
        cmd_ping(config)
    elif args.command == "run":
        cmd_run(args.goal, config, local=args.local)
    elif args.command == "core":
        if args.core_command == "start":
            cmd_core(config)
        elif args.core_command == "stop":
            print("TODO: stop daemon")
        elif args.core_command == "status":
            print("TODO: show status")
        else:
            core_parser.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
