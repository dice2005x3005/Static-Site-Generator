from textnode import TextNode, TextType
from blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, text_node_to_html_node
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new.append(node)
            continue
        if node.text == "":
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new.append(node)
            continue
        sections = []
        aja = ""
        for i in range(len(matches)):
            if aja == "":
                xd = node.text.split(f"![{matches[i][0]}]({matches[i][1]})", 1)
                aja = 1
            else:
                xd = xd[1].split(f"![{matches[i][0]}]({matches[i][1]})", 1)
            sections.append(xd[0])
        sections.append(xd[1])
        cont = 0
        for x in sections:
            if x != "":
                new.append(TextNode(x, TextType.TEXT))
            if cont <= len(matches)-1:
                new.append(TextNode(matches[cont][0], TextType.IMAGE, url=matches[cont][1]))
                cont += 1
    return new


def split_nodes_link(old_nodes):
    new = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new.append(node)
            continue
        if node.text == "":
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new.append(node)
            continue
        sections = []
        aja = ""
        for i in range(len(matches)):
            if aja == "":
                xd = node.text.split(f"[{matches[i][0]}]({matches[i][1]})", 1)
                aja = 1
            else:
                xd = xd[1].split(f"[{matches[i][0]}]({matches[i][1]})", 1)
            sections.append(xd[0])
        sections.append(xd[1])
        cont = 0
        for x in sections:
            if x != "":
                new.append(TextNode(x, TextType.TEXT))
            if cont <= len(matches)-1:
                new.append(TextNode(matches[cont][0], TextType.LINK, url=matches[cont][1]))
                cont += 1
    return new


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    image = split_nodes_image(code)
    link = split_nodes_link(image)
    return link

def markdown_to_html_node(markdown):
    ans = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.HEADING:
            if block.startswith("# "):
                text = block[2:]
                childs = text_to_children(text)
                node = ParentNode(tag="h1", children=childs)
                ans.append(node)
            elif block.startswith("## "):
                text = block[3:]
                childs = text_to_children(text)
                node = ParentNode(tag="h2", children=childs)
                ans.append(node)
            elif block.startswith("### "):
                text = block[4:]
                childs = text_to_children(text)
                node = ParentNode(tag="h3", children=childs)
                ans.append(node)
            elif block.startswith("#### "):
                text = block[5:]
                childs = text_to_children(text)
                node = ParentNode(tag="h4", children=childs)
                ans.append(node)
            elif block.startswith("##### "):
                text = block[6:]
                childs = text_to_children(text)
                node = ParentNode(tag="h5", children=childs)
                ans.append(node)
            elif block.startswith("###### "):
                text = block[7:]
                childs = text_to_children(text)
                node = ParentNode(tag="h6", children=childs)
                ans.append(node)

        elif type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph = " ".join(line.strip() for line in lines)
            children = text_to_children(paragraph)
            ans.append(ParentNode("p", children))

        elif type == BlockType.QUOTE:
            bloques = block.split("\n")
            lines = [line.lstrip(">").strip() for line in bloques]
            text = " ".join(lines)
            childs = text_to_children(text)
            node = ParentNode(tag="blockquote", children=childs)
            ans.append(node)

        elif type == BlockType.UNORDERED_LIST:
            bloques = block.split("\n")
            items = []
            for line in bloques:
                xd = line.lstrip("-")
                xd2 = xd.strip()
                childs = text_to_children(xd2)
                items.append(ParentNode(tag="li", children=childs))
            node = ParentNode(tag="ul", children=items)
            ans.append(node)

        elif type == BlockType.ORDERED_LIST:
            bloques = block.split("\n")
            items = []
            for line in bloques:
                xd = line.split(". ", 1)[1]
                childs = text_to_children(xd)
                items.append(ParentNode(tag="li", children=childs))
            node = ParentNode(tag="ol", children=items)
            ans.append(node)
            
        elif type == BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            text = block[4:-3]
            raw_text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            code = ParentNode("code", [child])
            ans.append(ParentNode("pre", [code]))
    
    final = ParentNode(tag="div", children=ans)
    return final

        
def text_to_children(text):
    res = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        xd = text_node_to_html_node(node)
        res.append(xd)
    return res
    
            