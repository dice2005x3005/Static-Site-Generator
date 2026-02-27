import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode(tag="p", value="aqua >")
        self.assertIsNotNone(node.tag)
    
    def test_value(self):
        node = HTMLNode(tag="p", value="aqua >")
        self.assertIsNotNone(node.tag)
    
    def test_children_non(self):
        node = HTMLNode(tag="p", value="aqua >")
        self.assertIsNone(node.children)


class TestLeadNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_p(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")