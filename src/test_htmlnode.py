import unittest
from htmlnode import HTMLNode


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
