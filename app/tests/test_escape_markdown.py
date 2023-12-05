from app.activities.helpers import escape_markdown

import pytest


def test_escape_markdown():
    # Test escaping various Markdown special characters
    assert escape_markdown("*bold* _italic_ [link](url)") == r"\*bold\* \_italic\_ \[link\]\(url\)"
    assert escape_markdown("~strikethrough~") == r"\~strikethrough\~"
    assert escape_markdown("`code`") == r"\`code\`"
    assert escape_markdown("# Heading") == r"\# Heading"
    assert escape_markdown("normal text") == "normal text"


# Optional: You can also write specific tests for each special character
def test_escape_asterisk():
    assert escape_markdown("*") == r"\*"

def test_escape_underscore():
    assert escape_markdown("_") == r"\_"

# ... and so on for other characters
