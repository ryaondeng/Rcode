from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SubscriberRegistry:
    """事件订阅者注册中心。"""

    def __init__(self) -> None:
        self._subscribers: list[Callable[[BaseModel], Any]] = []

    def register(self, subscriber: Callable[[BaseModel], Any]) -> None:
        """注册订阅者。"""
        self._subscribers.append(subscriber)

    def build(self) -> list[Callable[[BaseModel], Any]]:
        """返回所有已注册的订阅者（含错误隔离包装）。"""
        return [self._wrap(s) for s in self._subscribers]

    def _wrap(self, subscriber: Callable[[BaseModel], Any]) -> Callable[[BaseModel], Any]:
        """包装订阅者，捕获异常不影响其他订阅者。"""
        def safe_handler(event: BaseModel) -> None:
            try:
                subscriber(event)
            except Exception as e:
                logger.warning("Subscriber %s failed: %s", subscriber.__name__, e)
        return safe_handler


def build_default_subscribers(config: Any = None) -> SubscriberRegistry:
    """按配置装配默认订阅者。"""
    registry = SubscriberRegistry()

    # Console 订阅者（非静默模式）
    silent = getattr(config, 'silent', False) if config else False
    if not silent:
        from rcode.cli.printer import ConsoleSubscriber
        registry.register(ConsoleSubscriber())

    return registry
