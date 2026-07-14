from __future__ import annotations

import logging
import sys
from pathlib import Path

from rcode.core.config import RcodeConfig


def setup_logging(config: RcodeConfig) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]

    log_file = config.logging.file
    if log_file:
        log_path = Path(log_file).expanduser()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_path))

    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=handlers,
    )

    # 禁用 httpx/httpcore 的详细日志
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpcore.http11").setLevel(logging.WARNING)
