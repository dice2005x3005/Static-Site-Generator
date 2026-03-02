import unittest
from splitdelimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitDelimiter(unittest.TestCase):
    def testeq(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
            ])

    def TestMultiple(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        node1 = TextNode("**fncs** chapter 2 season 5 **jelty** pls **dont break that wall**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node1], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
            TextNode("fncs", TextType.BOLD),
            TextNode(" chapter 2 season 5 ", TextType.TEXT),
            TextNode("jelty", TextType.BOLD),
            TextNode(" pls ", TextType.TEXT),
            TextNode("dont break that wall", TextType.BOLD),
            ])