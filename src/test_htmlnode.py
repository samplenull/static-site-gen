import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


# generate test cases for HTMLNode class
class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode(tag="div", children=[HTMLNode(value="Hello World")])
        self.assertEqual(node.to_html(), "<div>Hello World</div>")

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a", props={"href": "https://www.example.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 'href="https://www.example.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode(tag="p", value="This is a paragraph.")
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=This is a paragraph., children=[], props={})",
        )

    # leafnode test cases
    def test_leafnode_to_html(self):
        node = LeafNode(
            tag="a",
            value="Link to example.com",
            props={"href": "https://www.example.com/image.jpg"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.example.com/image.jpg">Link to example.com</a>',
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # more test cases for ParentNode
    def test_parent_node_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")]).to_html()

    def test_parent_node_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    # more test cases for LeafNode
    def test_leaf_node_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()
