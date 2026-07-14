from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CompactionConfig:
    """压缩配置。"""
    auto_threshold: float = 0.0    # 自动压缩阈值（0 = 禁用）
    tool_result_limit: int = 8000  # 截断触发字符数
    tool_result_keep: int = 4000   # 截断后保留的前缀字符数


def truncate_tool_results(
    messages: list[dict],
    limit: int = 8000,
    keep: int = 4000,
) -> list[dict]:
    """截断超长的 tool_result。

    Args:
        messages: 消息列表
        limit: 截断触发字符数
        keep: 截断后保留的前缀字符数

    Returns:
        截断后的消息列表
    """
    result = []
    for msg in messages:
        if msg.get("role") != "user" or not isinstance(msg.get("content"), list):
            result.append(msg)
            continue

        new_content = []
        for block in msg["content"]:
            if block.get("type") != "tool_result":
                new_content.append(block)
                continue

            content = block.get("content", "")
            if len(content) > limit:
                truncated = content[:keep]
                omitted = len(content) - keep
                truncated += f"\n[... {omitted} chars omitted]"
                new_content.append({**block, "content": truncated})
            else:
                new_content.append(block)

        result.append({**msg, "content": new_content})

    return result
