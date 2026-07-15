import pytest

from rcode.core.context import ExecutionContext


# 功能：测试 ExecutionContext.replace_history
# 设计：验证历史消息被替换为摘要
def test_replace_history():
    context = ExecutionContext(goal="test", run_id="123")
    context.messages = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
    ]
    context.replace_history("summary text")
    assert len(context.messages) == 1
    assert context.messages[0]["role"] == "user"
    assert context.messages[0]["content"] == "summary text"


# 功能：测试 replace_history 空摘要
# 设计：验证空摘要也能正常工作
def test_replace_history_empty():
    context = ExecutionContext(goal="test", run_id="123")
    context.messages = [{"role": "user", "content": "hello"}]
    context.replace_history("")
    assert len(context.messages) == 1
    assert context.messages[0]["content"] == ""
