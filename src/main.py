from textnode import TextNode, TextType

def main():
    xd = TextNode("hola", TextType.LINK, "https://www.boot.dev")
    print(xd)

main()