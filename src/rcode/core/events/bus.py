from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Union

from pydantic import BaseModel

type EventHandler = Union[Callable[[BaseModel], Awaitable[None]], Callable[[BaseModel], None]]


class EventBus:
    """事件总线，实现发布-订阅模式。"""

    def __init__(self) -> None:
        self._subscribers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        """注册事件处理器。"""
        self._subscribers.append(handler)

    async def publish(self, event: BaseModel) -> None:
        """发布事件，按注册顺序调用所有订阅者。"""
        for handler in self._subscribers:
            result = handler(event)
            if asyncio.iscoroutine(result):
                await result
