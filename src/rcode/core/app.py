from __future__ import annotations

import asyncio
import logging
import signal
import time
from datetime import UTC, datetime
from typing import Any

from rcode import __version__
from rcode.core.bus.commands import PongResult
from rcode.core.config import RcodeConfig, load_config
from rcode.core.logging_setup import setup_logging
from rcode.core.transport.socket_server import SocketServer

logger = logging.getLogger(__name__)


class CoreApp:
    def __init__(self) -> None:
        self._start_time = time.monotonic()

    async def _ping_handler(self, params: dict[str, Any]) -> PongResult:
        client = params.get("client", "unknown")
        logger.debug("ping from %s", client)
        return PongResult(
            server_version=__version__,
            uptime_ms=int((time.monotonic() - self._start_time) * 1000),
            received_at=datetime.now(UTC).isoformat(),
        )

    async def run(self) -> None:
        config = load_config()
        setup_logging(config)

        server = SocketServer(config.host, config.port)
        server.register("core.ping", self._ping_handler)

        addr = await server.start()
        logger.info("rcode-core %s listening at %s", __version__, addr)

        shutdown = asyncio.Event()
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, shutdown.set)
        loop.add_signal_handler(signal.SIGTERM, shutdown.set)
        await shutdown.wait()

        logger.info("shutting down")
        await server.stop()


def main() -> None:
    asyncio.run(CoreApp().run())


if __name__ == "__main__":
    main()
