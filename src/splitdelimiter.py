from textnode import TextNode, TextType

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




