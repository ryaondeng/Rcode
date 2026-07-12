from __future__ import annotations

import asyncio
import sys

import click

from rcode import __version__


@click.group()
@click.version_option(__version__, prog_name="rcode")
def cli() -> None:
    pass


@cli.command()
@click.option("--host", default="127.0.0.1", help="Core host")
@click.option("--port", default=7437, help="Core port")
def ping(host: str, port: int) -> None:
    from rcode.core.transport.socket_client import SocketClient

    async def _ping() -> None:
        client = SocketClient(host, port)
        result = await client.send("core.ping", {"client": "cli"})
        click.echo(f"Pong: {result}")

    asyncio.run(_ping())


@cli.command()
def core() -> None:
    from rcode.core.app import main

    main()


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
