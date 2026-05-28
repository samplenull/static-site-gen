import unittest
from src.textnode import TextNode, TextType
from src.split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_blocks(self):
        """Test splitting code blocks with backticks"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_multiple_code_blocks(self):
        """Test splitting multiple code blocks"""
        node = TextNode("Here is `code1` and `code2` in text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" in text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_bold_text(self):
        """Test splitting bold text with double asterisks"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_italic_text(self):
        """Test splitting italic text with underscores"""
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_mixed_delimiters(self):
        """Test splitting mixed delimiters in one text"""
        node = TextNode("Text with `code` and **bold** and _italic_", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # Should only process the code delimiters first
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and **bold** and _italic_", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_no_delimiters(self):
        """Test splitting when no delimiters are present"""
        node = TextNode("This is plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("This is plain text", TextType.TEXT)]

        self.assertEqual(result, expected)

    def test_split_empty_text(self):
        """Test splitting empty text"""
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [TextNode("", TextType.TEXT)]

        self.assertEqual(result, expected)

    def test_split_unmatched_delimiter(self):
        """Test that unmatched delimiters raise an exception"""
        node = TextNode("This has `unmatched code", TextType.TEXT)

        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertIn("Invalid Markdown syntax", str(context.exception))

    def test_split_code_block_at_beginning(self):
        """Test code block at the beginning of text"""
        node = TextNode("`code` is here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" is here", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_code_block_at_end(self):
        """Test code block at the end of text"""
        node = TextNode("Here is `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_split_nested_delimiters(self):
        """Test nested delimiters (should not be parsed as nested)"""
        node = TextNode("Text with `nested `code` here`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("nested ", TextType.CODE),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]

        # Only the first `code` should be processed, not nested ones
        self.assertEqual(result, expected)

    def test_non_text_nodes_unchanged(self):
        """Test that non-text nodes remain unchanged"""
        node1 = TextNode("This is normal text", TextType.TEXT)
        node2 = TextNode("Bold content", TextType.BOLD)
        node3 = TextNode("More text", TextType.TEXT)

        result = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)

        expected = [
            TextNode("This is normal text", TextType.TEXT),
            TextNode("Bold content", TextType.BOLD),
            TextNode("More text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)
