import unittest
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            node,
            node2,
            "TextNode instances with the same text, text_type, and url should be equal",
        )

    def test_ne(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            repr(node),
            "TextNode(This is a text node, bold, None)",
        )


if __name__ == "__main__":
    unittest.main()
