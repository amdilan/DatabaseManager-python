import sys
import os

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        # base_path = os.path.dirname(os.path.abspath(__file__))
        # base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def external_path(relative_path):
    """ Get path relative to the EXE file's directory """
    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def ResourcePath(relative_path, local=None):
    """ Get path according to location specification. If external use "ext" after relative path:
        ResourcePath(relative_path, 'ext')
    """
    if local == "ext":
        base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
    else:
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)