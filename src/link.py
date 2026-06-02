import re


def extract_markdown_images(text):
    """
    takes raw markdown text and returns a list of tuples.
    Each tuple should contain the alt text and the URL of any markdown images.
    """
    # Pattern to match markdown image syntax ![alt_text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    # Find all matches
    matches = re.findall(pattern, text)

    return matches


def extract_markdown_links(text):
    """
    takes raw markdown text and returns a list of tuples.
    Each tuple should contain the anchor text and the URL of any markdown links.
    """
    # Pattern to match markdown link syntax [anchor_text](url)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    # Find all matches
    matches = re.findall(pattern, text)

    return matches
