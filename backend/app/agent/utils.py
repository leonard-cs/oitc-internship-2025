import re


def remove_thinking_tags(text: str) -> str:
    """
    Remove <think>...</think> tags and their contents from text.

    Args:
        text (str): The input text that may contain thinking tags

    Returns:
        str: The cleaned text with thinking sections removed
    """
    # Remove <think>...</think> tags and their contents
    # This pattern matches the opening tag, any content (including newlines), and closing tag
    pattern = r"<think>.*?</think>"
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL)

    # Clean up any extra whitespace that might be left
    cleaned_text = cleaned_text.strip()

    return cleaned_text
