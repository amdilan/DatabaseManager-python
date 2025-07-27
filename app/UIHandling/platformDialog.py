from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from ui.platforms_dialog import Ui_PlatformDialog        
import app
from main import DB

class PlatformDialog(QtWidgets.QDialog, Ui_PlatformDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.data ={
            'id': None,
            'name': None
        }
        self.selectedData = None
        
        self.PopulatePlatforms()
        self.pushButtonEdit.setDisabled(True)
        self.pushButtonDelete.setDisabled(True)
        self.pushButtonNew.clicked.connect(self.HandleNew)
        self.pushButtonSave.clicked.connect(self.HandleSave)
        self.pushButtonEdit.clicked.connect(self.HandleEdit)
        self.pushButtonDelete.clicked.connect(self.HandleDelete)
        self.listWidgetPlat.itemSelectionChanged.connect(self.HandleSelection)
        
    def PopulatePlatforms(self):
        self.listWidgetPlat.clear()
        platforms = app.GetPlatforms(DB)
        for row in platforms:
            item = QtWidgets.QListWidgetItem(row[1])
            item.setData(Qt.ItemDataRole.UserRole, row)
            self.listWidgetPlat.addItem(item)
        self.lineEditPlat.setDisabled(True)
            
    def HandleSelection(self):
        selectedItem = self.listWidgetPlat.selectedItems()
        if not selectedItem:
            return
        # print(selectedItem)
        self.pushButtonEdit.setDisabled(False)
        self.pushButtonDelete.setDisabled(False)
        
        item = selectedItem[0]
        # print(item)
        row = self.listWidgetPlat.row(item)
        self.selectedData = self.listWidgetPlat.item(row).data(Qt.ItemDataRole.UserRole)
        
        # print(f"Selected ID: {self.selectedData[0]}")
        
    def ClearSelection(self):
        self.listWidgetPlat.clearSelection()
        self.listWidgetPlat.setCurrentItem(None)
        self.pushButtonEdit.setDisabled(True)
        self.pushButtonDelete.setDisabled(True)
            
    def HandleNew(self):
        self.data['id'] = None
        self.data['name'] = None
        self.lineEditPlat.setText(None)
        self.label.setText(None)
        self.ClearSelection()
        self.lineEditPlat.setDisabled(False)
        
    def HandleSave(self):
        self.data['name'] = self.lineEditPlat.text()
        
        if self.data['id'] == None:
            result = app.AddPlats(DB, self.data)
            if (result['success']):
                self.HandleNew()
                self.label.setText('Added Successfully!')
            else:
                self.label.setText('Duplicate, Try again!')
            self.PopulatePlatforms()
        else:
            result = app.updatePlats(DB, self.data)
            if (result['success']):
                self.HandleNew()
                self.label.setText('Updated Successfully!')
            else:
                self.label.setText('Duplicate, Try again!')
            self.PopulatePlatforms()
        
    def HandleEdit(self):
        self.data['id'] = self.selectedData[0]
        self.data['name'] = self.selectedData[1]
        
        self.lineEditPlat.setText(self.selectedData[1])
        self.lineEditPlat.setDisabled(False)
        
    def HandleDelete(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle('Deleting Dev.')
        dlg.setText(f"Are sure to delete Platform\n{self.selectedData[1]} ?")
        dlg.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        btn = dlg.exec()
        if btn == QtWidgets.QMessageBox.StandardButton.Yes:
            pass
        else:
            return
        
        id = self.selectedData[0]
        # print(f"id : {id}")
        # print(f"id : {self.selectedData}")
        result = app.DeletePlats(DB, id)
        if result['success']:
            self.HandleNew()
            self.label.setText('Delete Successfully!')
        else:
            self.label.setText('Deletion Failed!')
        self.PopulatePlatforms()
