def markdown_to_blocks(markdown):
    line = markdown.split("\n\n")
    new = []
    for i in line:
        if i != "":
            i.strip()
            new.append(i)
    return new
