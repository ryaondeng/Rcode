from __future__ import annotations

from rcode.core.app import CoreApp
from rcode.core.config import RcodeConfig


def cmd_core(config: RcodeConfig) -> None:
    app = CoreApp()
    app.run_sync()
