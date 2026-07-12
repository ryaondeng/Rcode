import asyncio
import signal
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from rcode.core.app import CoreApp
from rcode.core.bus.commands import PongResult


def test_core_app_init():
    app = CoreApp()
    assert app._start_time > 0


@pytest.mark.asyncio
async def test_ping_handler():
    app = CoreApp()
    result = await app._ping_handler({"client": "test"})
    assert isinstance(result, PongResult)
    assert result.server_version == "0.1.0"
    assert result.uptime_ms >= 0
    assert result.received_at is not None


@pytest.mark.asyncio
async def test_ping_handler_default_client():
    app = CoreApp()
    result = await app._ping_handler({})
    assert isinstance(result, PongResult)
    assert result.uptime_ms >= 0


@pytest.mark.asyncio
async def test_ping_handler_uptime_increases():
    app = CoreApp()
    result1 = await app._ping_handler({})
    await asyncio.sleep(0.01)
    result2 = await app._ping_handler({})
    assert result2.uptime_ms >= result1.uptime_ms


def test_run_sync():
    app = CoreApp()
    assert hasattr(app, 'run_sync')
