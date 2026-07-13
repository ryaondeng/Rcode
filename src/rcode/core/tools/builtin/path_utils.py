from __future__ import annotations

import os
from pathlib import Path


def get_workdir() -> Path:
    """获取工作目录，每次调用时读取环境变量。"""
    return Path(os.environ.get("RCODE_WORKDIR", ".")).resolve()


def safe_path(path: str, workdir: Path | None = None) -> Path:
    """验证路径在工作目录内，防止路径逃逸。

    Args:
        path: 相对路径
        workdir: 工作目录，默认从环境变量获取

    Returns:
        Path: 解析后的绝对路径

    Raises:
        ValueError: 如果路径逃逸到工作目录之外
    """
    if workdir is None:
        workdir = get_workdir()
    resolved = (workdir / path).resolve()
    if not resolved.is_relative_to(workdir.resolve()):
        raise ValueError(f"Path escapes workspace: {path}")
    return resolved
