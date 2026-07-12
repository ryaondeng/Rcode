import asyncio
import socket
from collections.abc import Generator

import pytest


@pytest.fixture
def free_port() -> Generator[int, None, None]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        port = s.getsockname()[1]
    yield port
