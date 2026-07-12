# LLM 接口

## LLMProvider

LLM 提供商抽象基类。

```python
class LLMProvider(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        tool_schemas: list[dict],
        system: str,
    ) -> ChatResponse:
        """发送聊天请求"""
```

## ChatResponse

LLM 响应。

```python
@dataclass
class ChatResponse:
    text: str | None             # 文本回复
    tool_calls: list[ToolCall]   # 工具调用列表
    stop_reason: str             # 停止原因
    thinking_blocks: list[dict]  # 思考块（extended thinking）
```

### stop_reason

| 值 | 说明 |
|------|------|
| `tool_use` | 需要调用工具 |
| `end_turn` | 对话结束 |
| `max_tokens` | 达到 token 限制 |

## ToolCall

工具调用信息。

```python
@dataclass
class ToolCall:
    id: str                      # 调用 ID
    name: str                    # 工具名称
    input: dict                  # 输入参数
```

## AnthropicProvider

Anthropic Claude 实现。

```python
class AnthropicProvider(LLMProvider):
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.client = Anthropic()
        self.model = model
    
    async def chat(
        self,
        messages: list[dict],
        tool_schemas: list[dict],
        system: str,
    ) -> ChatResponse:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8096,
            system=system,
            messages=messages,
            tools=tool_schemas,
        )
        return self._parse_response(response)
```

## 配置

在 `.env` 文件中配置：

```bash
ANTHROPIC_API_KEY=your_api_key
MODEL_ID=claude-sonnet-4-20250514
```

## 相关文件

- `src/rcode/core/llm/base.py`
- `src/rcode/core/llm/provider.py`
- `src/rcode/core/llm/types.py`