from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class RcodeConfig:
    host: str = "127.0.0.1"
    port: int = 7437
    log_level: str = "INFO"
    log_file: str | None = None


_CONFIG_FILE = Path("~/.rcode/config.toml").expanduser()


def load_config() -> RcodeConfig:
    load_dotenv(override=False)

    config = RcodeConfig()

    env_host = os.getenv("RCODE_HOST")
    if env_host is not None:
        config.host = env_host

    env_port = os.getenv("RCODE_PORT")
    if env_port is not None:
        config.port = int(env_port)

    env_log_level = os.getenv("RCODE_LOG_LEVEL")
    if env_log_level is not None:
        config.log_level = env_log_level

    env_log_file = os.getenv("RCODE_LOG_FILE")
    if env_log_file is not None and env_log_file.strip():
        config.log_file = env_log_file

    return config
