from textnode import TextNode, TextType
from copy import copy, generate_page, generate_pages_recursive


def main():
    copy()
    generate_pages_recursive("content", "template.html", "public")

main()