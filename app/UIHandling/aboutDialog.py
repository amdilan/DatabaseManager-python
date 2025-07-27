from PyQt6 import QtWidgets
from PyQt6.QtCore import PYQT_VERSION_STR
from PyQt6.QtGui import QDesktopServices

from ui.about import Ui_DialogAbout
import sys

class AboutDialog(QtWidgets.QDialog, Ui_DialogAbout):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.labelVersion.setText(f"Version: 1.0.2")
        self.labelPyQtVersion.setText(f"PyQt6: v{PYQT_VERSION_STR}")
        self.labelPyVersion.setText(f"Python: v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        
        self.labelGithub.setText('<a href="https://github.com/amdilan/DatabaseManager-python">Github.com</a>')
        self.labelGithub.setOpenExternalLinks(True)
        