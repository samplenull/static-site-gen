import unittest
from src.link import extract_markdown_images, extract_markdown_links
from src.link import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images_basic(self):
        text = "Here's an image: ![alt text](image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "image.jpg")])

    def test_extract_markdown_images_multiple(self):
        text = "Image 1: ![alt1](img1.jpg). Image 2: ![alt2](img2.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt1", "img1.jpg"), ("alt2", "img2.png")])

    def test_extract_markdown_images_with_spaces(self):
        text = "![alt with spaces](image path.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt with spaces", "image path.jpg")])

    def test_extract_markdown_images_empty_alt(self):
        text = "![](image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "image.jpg")])

    def test_extract_markdown_images_no_match(self):
        text = "This has no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_basic(self):
        text = "Check out [this link](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("this link", "https://example.com")])

    def test_extract_mark_link_multiple(self):
        text = "[Link 1](https://example1.com). [Link 2](https://example2.com)"
        result = extract_markdown_links(text)
        self.assertEqual(
            result,
            [("Link 1", "https://example1.com"), ("Link 2", "https://example2.com")],
        )

    def test_extract_markdown_links_with_spaces(self):
        text = "[link with spaces](url with spaces.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link with spaces", "url with spaces.com")])

    def test_extract_markdown_links_empty_anchor(self):
        text = "[](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "https://example.com")])

    def test_extract_markdown_links_no_match(self):
        text = "This has no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_and_links_mixed(self):
        text = "![image](img.jpg) and [link](url.com)"
        result_images = extract_markdown_images(text)
        result_links = extract_markdown_links(text)
        self.assertEqual(result_images, [("image", "img.jpg")])
        self.assertEqual(result_links, [("link", "url.com")])

    def test_extract_markdown_images_special_chars(self):
        text = r'![alt "quote"](image"url.jpg)'
        result = extract_markdown_images(text)
        self.assertEqual(result, [('alt "quote"', 'image"url.jpg')])

    def test_extract_markdown_links_special_chars(self):
        text = r'[link "quote"](url"url.com)'
        result = extract_markdown_links(text)
        self.assertEqual(result, [('link "quote"', 'url"url.com')])


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "Here's an image: ![alt text](https://example.com/image.png)", TextType.TEXT
        )
        result = split_nodes_image([node])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Here's an image: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt text")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/image.png")

    def test_multiple_images(self):
        node = TextNode(
            "Image 1: ![alt1](img1.png) and Image 2: ![alt2](img2.png)", TextType.TEXT
        )
        result = split_nodes_image([node])

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Image 1: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt1")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "img1.png")
        self.assertEqual(result[2].text, " and Image 2: ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "alt2")
        self.assertEqual(result[3].text_type, TextType.IMAGE)
        self.assertEqual(result[3].url, "img2.png")

    def test_image_with_no_surrounding_text(self):
        node = TextNode("![alt text](https://example.com/image.png)", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "alt text")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "https://example.com/image.png")

    def test_image_at_end_with_trailing_text(self):
        node = TextNode(
            "Here's some text ![alt](image.png) and more text", TextType.TEXT
        )
        result = split_nodes_image([node])

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Here's some text ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "image.png")
        self.assertEqual(result[2].text, " and more text")
        self.assertEqual(result[2].text_type, TextType.TEXT)


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "Here's a link: [click here](https://example.com/page)", TextType.TEXT
        )
        result = split_nodes_link([node])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Here's a link: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "click here")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/page")

    def test_multiple_links(self):
        node = TextNode(
            "Link 1: [first](link1.html) and Link 2: [second](link2.html)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Link 1: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "first")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "link1.html")
        self.assertEqual(result[2].text, " and Link 2: ")
        self.assertEqual(result[2].text_type, TextType.TEXT)
        self.assertEqual(result[3].text, "second")
        self.assertEqual(result[3].text_type, TextType.LINK)
        self.assertEqual(result[3].url, "link2.html")

    def test_link_with_no_surrounding_text(self):
        node = TextNode("[click here](https://example.com/page)", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "click here")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "https://example.com/page")

    def test_link_at_end_with_trailing_text(self):
        node = TextNode(
            "Here's some text [click here](page.html) and more text", TextType.TEXT
        )
        result = split_nodes_link([node])

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Here's some text ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "click here")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "page.html")
        self.assertEqual(result[2].text, " and more text")
        self.assertEqual(result[2].text_type, TextType.TEXT)
