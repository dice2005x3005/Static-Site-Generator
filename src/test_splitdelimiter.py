import unittest
from splitdelimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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
        
class TestExtractMDImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestExtractMDLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
             "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

class SplitNodeImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_single_link(self):
        node = TextNode(
            "Haz click [aqui](https://www.google.com) para buscar.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Haz click ", TextType.TEXT),
            TextNode("aqui", TextType.LINK, "https://www.google.com"),
            TextNode(" para buscar.", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

class TestTextToNode(unittest.TestCase):
    def test_text_to_nodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        self.assertEqual(expected, nodes)

if __name__ == "__main__":
    unittest.main()
