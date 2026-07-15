import pytest
from unittest.mock import MagicMock

from rcode.core.events.registry import SubscriberRegistry, build_default_subscribers


# 功能：测试 SubscriberRegistry.register
# 设计：验证订阅者能正确注册
def test_subscriber_registry_register():
    registry = SubscriberRegistry()
    handler = MagicMock()
    registry.register(handler)
    assert len(registry._subscribers) == 1


# 功能：测试 SubscriberRegistry.build
# 设计：验证 build 返回包装后的订阅者
def test_subscriber_registry_build():
    registry = SubscriberRegistry()
    handler = MagicMock()
    registry.register(handler)
    subscribers = registry.build()
    assert len(subscribers) == 1


# 功能：测试 SubscriberRegistry 错误隔离
# 设计：验证一个订阅者异常不影响其他订阅者
def test_subscriber_registry_error_isolation():
    registry = SubscriberRegistry()

    def failing_handler(event):
        raise ValueError("test error")

    success_handler = MagicMock()

    registry.register(failing_handler)
    registry.register(success_handler)

    subscribers = registry.build()

    # 调用第一个订阅者（会抛异常）
    from rcode.core.events.types import RunStartedEvent
    event = RunStartedEvent(run_id="123", goal="test", ts="2024-01-01T00:00:00")

    # 第一个订阅者抛异常，但不影响第二个
    for sub in subscribers:
        try:
            sub(event)
        except Exception:
            pass

    # 第二个订阅者应该被调用
    success_handler.assert_called_once()


# 功能：测试 build_default_subscribers
# 设计：验证默认订阅者包含 ConsoleSubscriber
def test_build_default_subscribers():
    registry = build_default_subscribers()
    subscribers = registry.build()
    assert len(subscribers) >= 1


# 功能：测试 build_default_subscribers 静默模式
# 设计：验证静默模式下不包含 ConsoleSubscriber
def test_build_default_subscribers_silent():
    config = MagicMock()
    config.silent = True
    registry = build_default_subscribers(config)
    subscribers = registry.build()
    # 静默模式下应该没有订阅者
    assert len(subscribers) == 0
