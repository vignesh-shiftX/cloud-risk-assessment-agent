import pytest
from playwright.sync_api import Page, expect
import os

CHAINLIT_URL = "http://localhost:8000"  # Change if your Chainlit app runs on a different port

# --- Core Chat Command Coverage ---
@pytest.mark.ui
@pytest.mark.parametrize("user_input,expected_keyword", [
    ("/report all", "summary"),
    ("/report aws --filter critical", "aws"),
    ("Show me high severity vulnerabilities", "high"),
    ("Show me issues", "issue"),
    ("asdf1234!!", "error"),
    ("/report kubernetes", "kubernetes"),
    ("/report container", "container"),
    ("/report code", "code"),
    ("What are the top critical issues?", "critical"),
    ("Give me a summary of container issues", "container"),
])
def test_chainlit_chat_commands(page: Page, user_input, expected_keyword):
    page.goto(CHAINLIT_URL)
    input_selector = "textarea, input[type='text']"
    page.wait_for_selector(input_selector)
    page.fill(input_selector, user_input)
    page.keyboard.press("Enter")
    # Wait for a response
    expect(page.locator(".cl-message, .message, .chat-message")).to_have_count(2, timeout=10000)
    # Check that the response contains the expected keyword (case-insensitive)
    response_text = page.locator(".cl-message, .message, .chat-message").nth(1).inner_text()
    assert expected_keyword.lower() in response_text.lower()

# --- UI Button Interactions ---
def test_generate_executive_summary_button(page: Page):
    page.goto(CHAINLIT_URL)
    button_selector = "button:has-text('Generate Executive Summary')"
    page.wait_for_selector(button_selector)
    page.click(button_selector)
    expect(page.locator(".summary, .executive-summary")).to_be_visible(timeout=10000)

@pytest.mark.parametrize("button_text", ["Copy", "Download CSV"])
def test_report_action_buttons(page: Page, button_text):
    page.goto(CHAINLIT_URL)
    input_selector = "textarea, input[type='text']"
    page.wait_for_selector(input_selector)
    page.fill(input_selector, "/report all")
    page.keyboard.press("Enter")
    expect(page.locator(".cl-message, .message, .chat-message")).to_have_count(2, timeout=10000)
    button_selector = f"button:has-text('{button_text}')"
    page.wait_for_selector(button_selector)
    page.click(button_selector)

# --- Theme and Settings ---
def test_theme_switching(page: Page):
    page.goto(CHAINLIT_URL)
    # Open settings
    settings_button = "button:has-text('Settings')"
    page.wait_for_selector(settings_button)
    page.click(settings_button)
    # Test theme switches
    theme_options = ["Light Theme", "Dark Theme", "Follow System"]
    for theme in theme_options:
        theme_button = f"button:has-text('{theme}')"
        page.click(theme_button)
        # Verify theme change (you might need to adjust selectors based on your theme implementation)
        if "Light" in theme:
            expect(page.locator("body")).to_have_class(/.*light.*/)
        elif "Dark" in theme:
            expect(page.locator("body")).to_have_class(/.*dark.*/)

# --- Message Feedback ---
def test_message_feedback(page: Page):
    page.goto(CHAINLIT_URL)
    # Send a message first
    page.fill("textarea, input[type='text']", "/report all")
    page.keyboard.press("Enter")
    page.wait_for_selector(".cl-message, .message, .chat-message")
    
    # Test feedback buttons
    feedback_buttons = ["Helpful", "Not helpful"]
    for button in feedback_buttons:
        button_selector = f"button:has-text('{button}')"
        page.wait_for_selector(button_selector)
        page.click(button_selector)
        
        # If it's negative feedback, test adding a comment
        if button == "Not helpful":
            dialog_selector = "[role='dialog']"
            page.wait_for_selector(dialog_selector)
            page.fill("textarea", "Test feedback comment")
            page.click("button:has-text('Submit feedback')")
            expect(page.locator(".feedback-status, .status-message")).to_be_visible()

# --- File Upload ---
def test_file_upload(page: Page):
    page.goto(CHAINLIT_URL)
    # Create a temporary test file
    test_file_path = "test_upload.txt"
    with open(test_file_path, "w") as f:
        f.write("Test content for upload")
    
    try:
        # Test file upload
        page.set_input_files("input[type='file']", test_file_path)
        # Verify upload success
        expect(page.locator(".file-upload-success, .upload-complete")).to_be_visible()
    finally:
        # Cleanup
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

# --- Error Handling & Robustness ---
@pytest.mark.parametrize("invalid_input", [
    "",  # Empty input
    " ",  # Whitespace only
    "/invalid_command",  # Invalid command
    "?" * 1000,  # Very long input
])
def test_input_validation(page: Page, invalid_input):
    page.goto(CHAINLIT_URL)
    input_selector = "textarea, input[type='text']"
    page.wait_for_selector(input_selector)
    page.fill(input_selector, invalid_input)
    page.keyboard.press("Enter")
    if not invalid_input.strip():
        # Empty input should not create a new message
        expect(page.locator(".cl-message, .message, .chat-message")).to_have_count(1, timeout=5000)
    else:
        # Invalid inputs should show error message
        expect(page.locator(".error-message, .alert-error")).to_be_visible()

# --- Accessibility & Usability ---
def test_keyboard_navigation(page: Page):
    page.goto(CHAINLIT_URL)
    # Test tab navigation
    page.keyboard.press("Tab")
    input_selector = "textarea, input[type='text']"
    expect(page.locator(input_selector)).to_be_focused()
    
    # Test keyboard shortcuts
    page.keyboard.press("Control+Enter")  # Test send shortcut
    page.keyboard.press("Escape")  # Test closing dialogs

def test_screen_reader_accessibility(page: Page):
    page.goto(CHAINLIT_URL)
    # Verify ARIA labels are present
    expect(page.locator("[aria-label]")).to_have_count(lambda count: count > 0)
    expect(page.locator("[role]")).to_have_count(lambda count: count > 0)

# --- Chat History ---
def test_chat_history(page: Page):
    page.goto(CHAINLIT_URL)
    # Send multiple messages
    messages = ["/report all", "/report aws", "Show me critical issues"]
    for msg in messages:
        page.fill("textarea, input[type='text']", msg)
        page.keyboard.press("Enter")
        page.wait_for_selector(".cl-message, .message, .chat-message")
    
    # Test history navigation
    history_button = "button:has-text('Show history')"
    page.click(history_button)
    expect(page.locator(".history-item")).to_have_count(len(messages))

# --- Mobile Responsiveness ---
@pytest.mark.parametrize("viewport", [
    {"width": 375, "height": 667},  # iPhone SE
    {"width": 768, "height": 1024},  # iPad
    {"width": 1920, "height": 1080},  # Desktop
])
def test_responsive_layout(page: Page, viewport):
    page.set_viewport_size(viewport)
    page.goto(CHAINLIT_URL)
    # Verify key elements are visible
    expect(page.locator("textarea, input[type='text']")).to_be_visible()
    expect(page.locator("button:has-text('Send')")).to_be_visible()

# Run tests with: pytest --headed --browser=chromium tests/ui/test_chainlit_ui.py 