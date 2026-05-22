from textnode import TextNode
from textnode import TextType


def main():
    print("Hello from best static site generator in Universe!")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)


main()
