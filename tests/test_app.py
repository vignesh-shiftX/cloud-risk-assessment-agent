import pytest
from src.core.app import (
    parse_report_command, 
    VALID_REPORT_CATEGORIES,
    classify_user_intent,
    header_auth_callback,
    token_count,
    messages_token_count,
    trim_messages_to_max_tokens,
    on_message,
    reasoning_prompt,
    get_latest_human_message
)
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import chainlit as cl
import pandas as pd
from io import StringIO
import json

@pytest.fixture
def sample_messages():
    return [
        SystemMessage(content="System test message"),
        HumanMessage(content="Human test message"),
        AIMessage(content="AI test message")
    ]

@pytest.fixture
def sample_dataframe():
    data = {
        'severity': ['HIGH', 'MEDIUM', 'LOW'],
        'message': ['Test issue 1', 'Test issue 2', 'Test issue 3'],
        'resource': ['resource1', 'resource2', 'resource3']
    }
    return pd.DataFrame(data)

class TestReportCommands:
    """Test suite for report command handling"""
    
    @pytest.mark.parametrize("command,expected", [
        ("/report all", "all"),
        ("/report kubernetes", "kubernetes"),
        ("/report aws", "aws"),
        ("/report code", "code"),
        ("/report container", "container"),
        ("/report aws --filter critical", "aws"),
        ("/report all --since 2024-01-01", "all")
    ])
    def test_parse_report_command_valid(self, command, expected):
        """Test parsing various valid report commands"""
        assert parse_report_command(command) == expected

    @pytest.mark.parametrize("invalid_command", [
        "/report invalid",
        "not a report command",
        "/report",
        "",
        "/report aws --invalid-flag",
        "/report all --since invalid-date",
        "/ report aws",  # Space after slash
        "/Report aws"  # Case sensitivity
    ])
    def test_parse_report_command_invalid(self, invalid_command):
        """Test parsing invalid report commands"""
        with pytest.raises(ValueError):
            parse_report_command(invalid_command)

    def test_valid_report_categories(self):
        """Test valid report categories constant"""
        assert isinstance(VALID_REPORT_CATEGORIES, set)
        assert all(isinstance(cat, str) for cat in VALID_REPORT_CATEGORIES)
        assert len(VALID_REPORT_CATEGORIES) >= 5  # all, aws, kubernetes, code, container

@pytest.mark.asyncio
class TestUserIntentClassification:
    """Test suite for user intent classification"""

    @pytest.mark.parametrize("user_input,expected_goto,expected_category", [
        ("/report all", "summary", "all"),
        ("/report aws", "summary", "aws"),
        ("Show me critical issues", "querydb", None),
        ("Why is this vulnerability critical?", "reason", None),
        ("Help me understand this issue", "reason", None),
        ("List all high severity findings", "querydb", None),
        ("What are the top risks?", "querydb", None)
    ])
    async def test_classify_user_intent(self, user_input, expected_goto, expected_category):
        """Test classification of various user inputs"""
        messages = [HumanMessage(content=user_input)]
        state = {"messages": messages}
        result = await classify_user_intent(state)
        assert result.goto == expected_goto
        if expected_category:
            assert result.update.get("category") == expected_category

    async def test_classify_user_intent_with_context(self):
        """Test classification with conversation context"""
        messages = [
            HumanMessage(content="/report aws"),
            AIMessage(content="Here's your AWS report..."),
            HumanMessage(content="Why are these issues critical?")
        ]
        state = {"messages": messages}
        result = await classify_user_intent(state)
        assert result.goto == "reason"

class TestAuthentication:
    """Test suite for authentication functionality"""

    @pytest.mark.parametrize("headers,expected_metadata", [
        ({}, {"role": "admin", "provider": "header"}),
        ({"Authorization": "Bearer test"}, {"role": "admin", "provider": "header"}),
        ({"Custom-Header": "test"}, {"role": "admin", "provider": "header"})
    ])
    def test_header_auth_callback(self, headers, expected_metadata):
        """Test header authentication with various headers"""
        user = header_auth_callback(headers)
        assert user.identifier == "admin"
        assert user.metadata == expected_metadata

class TestTokenManagement:
    """Test suite for token management functionality"""

    @pytest.mark.parametrize("text,min_expected", [
        ("This is a test", 4),
        ("", 0),
        ("A" * 1000, 200),  # Long text
        ("Special chars: !@#$%^&*()", 10),
        ("1234567890", 10),
        ("Multi\nline\ntext", 5)
    ])
    def test_token_count(self, text, min_expected):
        """Test token counting with various inputs"""
        count = token_count(text)
        assert isinstance(count, int)
        assert count >= min_expected

    def test_messages_token_count(self, sample_messages):
        """Test message chain token counting"""
        count = messages_token_count(sample_messages)
        assert isinstance(count, int)
        assert count > 0
        # Test empty message list
        assert messages_token_count([]) == 0

    @pytest.mark.parametrize("max_tokens", [10, 50, 100, 500])
    def test_trim_messages(self, sample_messages, max_tokens):
        """Test message trimming with various token limits"""
        trimmed = trim_messages_to_max_tokens(sample_messages, max_tokens)
        assert len(trimmed) <= len(sample_messages)
        assert messages_token_count(trimmed) <= max_tokens
        # Ensure system message is preserved if present
        if any(isinstance(m, SystemMessage) for m in sample_messages):
            assert any(isinstance(m, SystemMessage) for m in trimmed)

@pytest.mark.asyncio
class TestMessageHandling:
    """Test suite for message handling"""

    async def test_on_message_report_command(self, mocker):
        """Test handling of report commands"""
        msg = cl.Message(content="/report all")
        mocker.patch('chainlit.user_session.get', return_value=[])
        mocker.patch('chainlit.Message.send')
        await on_message(msg)
        # Add assertions based on expected behavior

    async def test_on_message_with_dataframe(self, mocker, sample_dataframe):
        """Test message handling with dataframe generation"""
        msg = cl.Message(content="/report aws")
        mocker.patch('chainlit.user_session.get', return_value=[])
        mocker.patch('pd.read_csv', return_value=sample_dataframe)
        await on_message(msg)
        # Add assertions for dataframe handling

class TestPromptManagement:
    """Test suite for prompt management"""

    def test_reasoning_prompt_generation(self):
        """Test reasoning prompt generation"""
        context = "Test context"
        question = "Why is this important?"
        prompt = reasoning_prompt(context, question)
        assert isinstance(prompt, str)
        assert context in prompt
        assert question in prompt

    def test_get_latest_human_message(self, sample_messages):
        """Test retrieving latest human message"""
        latest = get_latest_human_message(sample_messages)
        assert isinstance(latest, str)
        # Test with no human messages
        no_human = [SystemMessage(content="test"), AIMessage(content="test")]
        assert get_latest_human_message(no_human) == "" 