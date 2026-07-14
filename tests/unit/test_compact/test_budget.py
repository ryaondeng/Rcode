from rcode.core.compact.budget import truncate_tool_results


def test_truncate_tool_results_no_truncation():
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "tool_result", "content": "short output"}
            ]
        }
    ]
    result = truncate_tool_results(messages)
    assert result[0]["content"][0]["content"] == "short output"


def test_truncate_tool_results_with_truncation():
    long_content = "x" * 10000
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "tool_result", "content": long_content}
            ]
        }
    ]
    result = truncate_tool_results(messages, limit=8000, keep=4000)
    content = result[0]["content"][0]["content"]
    assert len(content) < len(long_content)
    assert "chars omitted" in content


def test_truncate_tool_results_preserves_other_blocks():
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "content": "keep this"},
                {"type": "tool_result", "content": "x" * 10000}
            ]
        }
    ]
    result = truncate_tool_results(messages, limit=8000, keep=4000)
    assert result[0]["content"][0]["content"] == "keep this"
    assert "chars omitted" in result[0]["content"][1]["content"]
