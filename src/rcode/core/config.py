from __future__ import annotations

import os
import sys
import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LLMConfig(BaseModel):
    """LLM 配置。"""
    model_config = ConfigDict(extra="forbid")

    model: str = "mimo-v2.5"
    timeout: int = 120
    max_retries: int = 2


class SessionConfig(BaseModel):
    """会话配置。"""
    model_config = ConfigDict(extra="forbid")

    dir: str = ".rcode/sessions"
    auto_archive_days: int = 30


class CompactConfig(BaseModel):
    """压缩配置。"""
    model_config = ConfigDict(extra="forbid")

    threshold: float = Field(default=0.0, ge=0.0, le=1.0)
    tool_result_limit: int = 8000
    tool_result_keep: int = 4000


class TraceConfig(BaseModel):
    """Trace 配置。"""
    model_config = ConfigDict(extra="forbid")

    dir: str = ".traces"
    max_files: int = 100


class LoggingConfig(BaseModel):
    """日志配置。"""
    model_config = ConfigDict(extra="forbid")

    level: str = "INFO"
    file: str = "~/.rcode/logs/core.log"


class RcodeConfig(BaseModel):
    """Rcode 配置模型，支持四层优先级。"""
    model_config = ConfigDict(extra="forbid")

    llm: LLMConfig = LLMConfig()
    session: SessionConfig = SessionConfig()
    compact: CompactConfig = CompactConfig()
    trace: TraceConfig = TraceConfig()
    logging: LoggingConfig = LoggingConfig()
    host: str = "127.0.0.1"
    port: int = 7437
    log_level: str = "INFO"
    silent: bool = False


def load_config(
    project_dir: str = ".",
    cli_overrides: dict[str, Any] | None = None,
) -> RcodeConfig:
    """四层优先级配置加载。

    优先级（低 → 高）：
    1. 内置默认值（pydantic 模型默认）
    2. ~/.rcode/config.toml（用户全局）
    3. .rcode/config.toml（项目本地）
    4. 环境变量 RCODE_* / CLI --flag
    """
    merged: dict[str, Any] = {}

    # 2. 用户全局
    global_path = Path.home() / ".rcode" / "config.toml"
    if global_path.exists():
        try:
            with open(global_path, "rb") as f:
                merged.update(tomllib.load(f))
        except tomllib.TOMLDecodeError as e:
            print(f"Config parse error ({global_path}): {e}", file=sys.stderr)
            sys.exit(1)

    # 3. 项目本地
    project_path = Path(project_dir) / ".rcode" / "config.toml"
    if project_path.exists():
        try:
            with open(project_path, "rb") as f:
                merged.update(tomllib.load(f))
        except tomllib.TOMLDecodeError as e:
            print(f"Config parse error ({project_path}): {e}", file=sys.stderr)
            sys.exit(1)

    # 4. 环境变量
    env_overrides = _load_env_vars()
    merged.update(env_overrides)

    # 5. CLI 覆盖
    if cli_overrides:
        merged.update(cli_overrides)

    # pydantic 校验（extra="forbid" 会拒绝未知字段）
    try:
        return RcodeConfig(**merged)
    except Exception as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)


def _load_env_vars() -> dict[str, Any]:
    """从环境变量加载 RCODE_* 配置。"""
    result: dict[str, Any] = {}
    for key, value in os.environ.items():
        if key.startswith("RCODE_"):
            parts = key[6:].lower().split("_")
            # RCODE_LLM_MODEL → {"llm": {"model": value}}
            d = result
            for part in parts[:-1]:
                d = d.setdefault(part, {})
            d[parts[-1]] = _coerce(value)
    return result


def _coerce(value: str) -> Any:
    """自动类型转换。"""
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def get_config() -> RcodeConfig:
    """兼容旧接口。"""
    return load_config()
