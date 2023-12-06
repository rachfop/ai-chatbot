def escape_markdown(text: str) -> str:
    """
    Escapes special characters for Telegram Markdown V2 to make the text more readable.

    Args:
        text (str): The text to be formatted for Telegram Markdown V2.

    Returns:
        str: The formatted text.
    """

    # Characters that need escaping in Telegram Markdown V2, only when used in special contexts
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

    # Escape only if these characters are not already escaped
    for char in special_chars:
        text = text.replace(char, f'\\{char}')

    return text