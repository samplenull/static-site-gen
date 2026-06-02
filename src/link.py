import re
from textnode import TextNode
from textnode import TextType


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split TextNodes containing markdown images into multiple nodes.
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # If it's not regular text, just add the node as-is
            new_nodes.append(node)
            continue

        # Extract all images from the text
        images = extract_markdown_images(node.text)

        if not images:
            # If no images found, add the original node
            new_nodes.append(node)
            continue

        # Split the text at each image and create nodes
        original_text = node.text
        remaining_text = original_text

        for alt_text, url in images:
            # Find the image markdown in the remaining text
            image_markdown = f"![{alt_text}]({url})"

            # Split only at the first occurrence
            parts = remaining_text.split(image_markdown, 1)

            # Add text before image as a regular TEXT node
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the image as an IMAGE node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Update remaining text to the part after the image
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        # If there's any text left after the last image, add it as a TEXT node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split TextNodes containing markdown links into multiple nodes.
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            # If it's not regular text, just add the node as-is
            new_nodes.append(node)
            continue

        # Extract all links from the text
        links = extract_markdown_links(node.text)

        if not links:
            # If no links found, add the original node
            new_nodes.append(node)
            continue

        # Split the text at each link and create nodes
        original_text = node.text
        remaining_text = original_text

        for anchor_text, url in links:
            # Find the link markdown in the remaining text
            link_markdown = f"[{anchor_text}]({url})"

            # Split only at the first occurrence
            parts = remaining_text.split(link_markdown, 1)

            # Add text before link as a regular TEXT node
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the link as a LINK node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            # Update remaining text to the part after the link
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        # If there's any text left after the last link, add it as a TEXT node
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes
