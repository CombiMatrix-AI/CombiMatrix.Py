import PyInstaller.__main__
from .lib.ui import ROOT_DIR

path_to_main = str(ROOT_DIR / "app.py")

def install():
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        # other pyinstaller options... 
    ])