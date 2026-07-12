from __future__ import annotations

import logging
import sys

from rcode.core.config import RcodeConfig


def setup_logging(config: RcodeConfig) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]

    if config.log_file is not None:
        handlers.append(logging.FileHandler(config.log_file))

    logging.basicConfig(
        level=getattr(logging, config.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=handlers,
    )
