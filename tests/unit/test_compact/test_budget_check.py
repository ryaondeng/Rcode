import pytest

from rcode.core.compact.budget import TokenBudget


# 功能：测试 TokenBudget.check 未超水位
# 设计：消息数量少时不触发压缩
@pytest.mark.asyncio
async def test_token_budget_check_below_threshold():
    budget = TokenBudget(threshold=0.7)
    messages = [{"role": "user", "content": "hello"}]
    result = await budget.check(messages, max_tokens=100000)
    assert result is False


# 功能：测试 TokenBudget.check 超水位
# 设计：消息数量多时触发压缩
@pytest.mark.asyncio
async def test_token_budget_check_above_threshold():
    budget = TokenBudget(threshold=0.7)
    # 创建超长消息
    long_content = "x" * 400000  # ~100000 tokens
    messages = [{"role": "user", "content": long_content}]
    result = await budget.check(messages, max_tokens=100000)
    assert result is True


# 功能：测试 TokenBudget.check 边界情况
# 设计：刚好等于阈值时不触发
@pytest.mark.asyncio
async def test_token_budget_check_at_threshold():
    budget = TokenBudget(threshold=0.7)
    # 70000 tokens * 4 = 280000 chars
    content = "x" * 280000
    messages = [{"role": "user", "content": content}]
    result = await budget.check(messages, max_tokens=100000)
    assert result is False
