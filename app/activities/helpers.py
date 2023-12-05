import re

def escape_markdown(text: str) -> str:
    """
    Escape markdown special characters.

    Args:
        text (str): The text to be converted.

    Returns:
        str: The escaped text.
    """
    # Regular expression pattern for Markdown special characters
    pattern = r'([_\*\[\]\(\)~`>#\+\-=|{}\.!])'

    # Replace each special character with a backslash followed by the character
    return re.sub(pattern, r'\\\1', text)
