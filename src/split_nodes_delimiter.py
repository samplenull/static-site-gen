from typing import List
from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    """
    Split text nodes based on a delimiter and return new nodes with the specified text type.

    Args:
        old_nodes: List of TextNode objects to process
        delimiter: The delimiter string to split on (e.g., "`", "**", "_")
        text_type: The TextType to assign to the delimited content

    Returns:
        List of TextNode objects with splits applied
    """
    new_nodes = []

    for node in old_nodes:
        # Only process nodes that are of the TEXT type
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Handle empty text case - skip creating empty nodes
        if not node.text:
            continue

        # Split the text by delimiter and alternate between regular and formatted text
        parts = node.text.split(delimiter)

        # Check for unmatched delimiters - if there's an even number of parts,
        # it means we have an unmatched opening delimiter
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter: {delimiter}")

        # If there are no delimiters, keep the original node
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        # Process parts, alternating between regular text and formatted text
        result_nodes = []
        for i, part in enumerate(parts):
            # Only add non-empty parts
            if part:
                # Even indices are regular text, odd indices are formatted text
                if i % 2 == 0:
                    result_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    result_nodes.append(TextNode(part, text_type))

        new_nodes.extend(result_nodes)

    return new_nodes
