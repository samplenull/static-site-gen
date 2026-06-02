import unittest
from src.link import extract_markdown_images, extract_markdown_links


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
