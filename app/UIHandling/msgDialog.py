from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from ui.message_dialog import Ui_MessageDialog
            
class MsgDialog(QtWidgets.QDialog, Ui_MessageDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
    def SetTitle(self, Title):
        self.MessageDialog.title(f"{Title}")
