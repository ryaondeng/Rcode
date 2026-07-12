from __future__ import annotations

import argparse
import sys

from rcode.cli.commands.ping import cmd_ping
from rcode.cli.commands.core import cmd_core
from rcode.core.config import get_config
from rcode.core.logging_setup import setup_logging


def main() -> None:
    parser = argparse.ArgumentParser(prog="rcode", description="Rcode CLI")
    parser.add_argument("--version", action="store_true", help="Print version and exit")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("ping", help="Ping the core daemon")

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
