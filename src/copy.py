import os
import shutil

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
    