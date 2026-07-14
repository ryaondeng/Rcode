import pytest
from pydantic import BaseModel

from rcode.core.events.bus import EventBus


class MockEvent(BaseModel):
    type: str = "mock"
    data: str = ""


@pytest.mark.asyncio
async def test_event_bus_subscribe_and_publish():
    bus = EventBus()
    received = []

    async def handler(event: BaseModel):
        received.append(event)

    bus.subscribe(handler)
    event = MockEvent(data="test")
    await bus.publish(event)

    assert len(received) == 1
    assert received[0].data == "test"


@pytest.mark.asyncio
async def test_event_bus_multiple_subscribers():
    bus = EventBus()
    received1 = []
    received2 = []

    async def handler1(event: BaseModel):
        received1.append(event)

    async def handler2(event: BaseModel):
        received2.append(event)

    bus.subscribe(handler1)
    bus.subscribe(handler2)

    event = MockEvent(data="test")
    await bus.publish(event)

    assert len(received1) == 1
    assert len(received2) == 1


@pytest.mark.asyncio
async def test_event_bus_order():
    bus = EventBus()
    order = []

    async def handler1(event: BaseModel):
        order.append(1)

    async def handler2(event: BaseModel):
        order.append(2)

    bus.subscribe(handler1)
    bus.subscribe(handler2)

    await bus.publish(MockEvent())

    assert order == [1, 2]
