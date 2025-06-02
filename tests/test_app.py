import pytest
from src.core.app import parse_report_command, VALID_REPORT_CATEGORIES
from langchain_core.messages import HumanMessage, SystemMessage
import chainlit as cl

def test_parse_report_command_valid():
    """Test parsing valid report commands"""
    assert parse_report_command("/report all") == "all"
    assert parse_report_command("/report kubernetes") == "kubernetes"
    assert parse_report_command("/report aws") == "aws"
    assert parse_report_command("/report code") == "code"
    assert parse_report_command("/report container") == "container"

def test_parse_report_command_invalid():
    """Test parsing invalid report commands"""
    with pytest.raises(ValueError):
        parse_report_command("/report invalid")
    with pytest.raises(ValueError):
        parse_report_command("not a report command")
    with pytest.raises(ValueError):
        parse_report_command("/report")
    with pytest.raises(ValueError):
        parse_report_command("")

@pytest.mark.asyncio
async def test_classify_user_intent_report():
    """Test classification of report commands"""
    messages = [HumanMessage(content="/report all")]
    state = {"messages": messages}
    result = await classify_user_intent(state)
    assert result.goto == "summary"
    assert result.update["category"] == "all"

@pytest.mark.asyncio
async def test_classify_user_intent_query():
    """Test classification of regular queries"""
    messages = [HumanMessage(content="Show me high severity vulnerabilities")]
    state = {"messages": messages}
    result = await classify_user_intent(state)
    assert result.goto in ["querydb", "reason"]

@pytest.mark.asyncio
async def test_header_auth_callback():
    """Test header authentication callback"""
    headers = {}
    user = header_auth_callback(headers)
    assert user.identifier == "admin"
    assert user.metadata["role"] == "admin"
    assert user.metadata["provider"] == "header"

@pytest.mark.asyncio
async def test_token_count():
    """Test token counting functionality"""
    text = "This is a test message"
    count = token_count(text)
    assert isinstance(count, int)
    assert count > 0

@pytest.mark.asyncio
async def test_messages_token_count():
    """Test message chain token counting"""
    messages = [
        SystemMessage(content="System message"),
        HumanMessage(content="Human message")
    ]
    count = messages_token_count(messages)
    assert isinstance(count, int)
    assert count > 0

@pytest.mark.asyncio
async def test_trim_messages():
    """Test message trimming functionality"""
    messages = [
        SystemMessage(content="System message"),
        HumanMessage(content="Human message"),
        SystemMessage(content="Another system message")
    ]
    max_tokens = 50
    trimmed = trim_messages_to_max_tokens(messages, max_tokens)
    assert len(trimmed) <= len(messages)
    assert messages_token_count(trimmed) <= max_tokens 