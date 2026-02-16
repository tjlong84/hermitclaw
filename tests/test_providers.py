"""Tests for multi-provider translation in providers.py."""

from hermitclaw.providers import _translate_tools_for_completions


def test_translate_tools_filters_web_search():
    """web_search_preview should be dropped for Chat Completions providers."""
    tools = [
        {"type": "function", "name": "shell", "description": "Run a command",
         "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
        {"type": "web_search_preview"},
        {"type": "function", "name": "respond", "description": "Talk",
         "parameters": {"type": "object", "properties": {"message": {"type": "string"}}, "required": ["message"]}},
    ]
    result = _translate_tools_for_completions(tools)
    assert len(result) == 2
    assert all(t["type"] == "function" for t in result)
    assert result[0]["function"]["name"] == "shell"
    assert result[1]["function"]["name"] == "respond"


def test_translate_tools_converts_format():
    """Function tools should be converted to Chat Completions format."""
    tools = [
        {"type": "function", "name": "shell", "description": "Run a command",
         "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}},
    ]
    result = _translate_tools_for_completions(tools)
    assert result[0] == {
        "type": "function",
        "function": {
            "name": "shell",
            "description": "Run a command",
            "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]},
        },
    }
