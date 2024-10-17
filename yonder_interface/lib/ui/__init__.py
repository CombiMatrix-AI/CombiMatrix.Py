import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Running as compiled executable
    ROOT_DIR = Path(sys.executable).parent.parent
else:
    # Running in a normal Python environment
    ROOT_DIR = Path(__file__).parent.parent.parent.parent