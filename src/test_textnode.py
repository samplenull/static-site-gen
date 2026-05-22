import unittest
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

    # Add even more test cases (at least 3 in total) to check various edge cases and ensure the robustness of the TextNode class.
    def test_link_node(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.example.com")
        self.assertEqual(node.text, "This is a link")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://www.example.com")

    def test_image_node(self):
        node = TextNode(
            "This is an image", TextType.IMAGE, "https://www.example.com/image.jpg"
        )
        self.assertEqual(node.text, "This is an image")
        self.assertEqual(node.text_type, TextType.IMAGE)
        self.assertEqual(node.url, "https://www.example.com/image.jpg")

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
