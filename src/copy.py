import os
import shutil
from splitdelimiter import markdown_to_html_node
from pathlib import Path

def copy():
    base = os.path.dirname(os.path.abspath(__file__))
    public = os.path.join(base, "..", "public")
    static = os.path.join(base, "..", "static")

    if os.path.exists(public):
        contenidos = os.listdir(public)
        for i in contenidos:
            ruta = os.path.join(public, i)
            if os.path.isdir(ruta):
                shutil.rmtree(ruta)
            else:
                os.remove(ruta)
        archivos = os.listdir(static)
        for y in archivos:
            ruta2 = os.path.join(static, y)
            if os.path.isdir(ruta2):
                shutil.copytree(ruta2, os.path.join(public, y))
            else:
                shutil.copy(ruta2, public)
    else:
        return "Ruta no encontrada"    
    

def extract_title(markdown):
    f = open(markdown, mode="r")
    mk = f.read()
    f.close()
    splited = mk.split("\n")
    for line in splited:
        if line.startswith("# "):
            return line[2:]
    raise Exception("There is no h1")
        

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    f = open(from_path, mode="r")
    mdFile = f.read()
    f.close()
    f = open(template_path, mode="r")
    tpFile = f.read()
    f.close()
    node = markdown_to_html_node(mdFile)
    html = node.to_html()
    title = extract_title(from_path)
    full_html = tpFile.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    ls = os.listdir(dir_path_content)
    for i in ls:
        path = os.path.join(dir_path_content, i)
        if os.path.isfile(path):
            dest = os.path.join(dest_dir_path, i)
            dest = Path(dest).with_suffix(".html")
            generate_page(path, template_path, dest)
        else:
            dest = os.path.join(dest_dir_path, i)
            generate_pages_recursive(path, template_path, dest)
    


