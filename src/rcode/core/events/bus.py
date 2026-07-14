from __future__ import annotations

from collections.abc import Awaitable, Callable

from pydantic import BaseModel

type EventHandler = Callable[[BaseModel], Awaitable[None]]


class EventBus:
    """事件总线，实现发布-订阅模式。

    职责：
    1. 管理事件订阅者
    2. 发布事件到所有订阅者
    3. 解耦事件生产者和消费者
    """

    def __init__(self) -> None:
        self._subscribers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        """注册事件处理器。"""
        self._subscribers.append(handler)

    async def publish(self, event: BaseModel) -> None:
        """发布事件，按注册顺序调用所有订阅者。"""
        for handler in self._subscribers:
            await handler(event)
