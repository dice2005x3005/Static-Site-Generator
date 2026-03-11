from textnode import TextNode, TextType
from copy import copy, generate_page


def main():
    xd = TextNode("hola", TextType.LINK, "https://www.boot.dev")
    copy()
    generate_page("content/index.md", "template.html", "public/index.html")

main()