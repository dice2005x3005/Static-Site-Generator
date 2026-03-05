from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new.append(node)
        else:
            info = node.text.split(delimiter)
            if len(info) % 2 == 0:
                raise Exception("someting went wrong")
            for i in range(len(info)):
                if info[i] == "":
                    continue
                if i % 2 == 0:
                    new.append(TextNode(info[i], TextType.TEXT))
                else:
                    new.append(TextNode(info[i], text_type))
    return new


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
    