from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices

from ui.Devs_dialog import Ui_DevDialog
import app
from main import DB

class DevDialog(QtWidgets.QDialog, Ui_DevDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.data ={
            'id': None,
            'name': None,
            'alias': None,
            'link': None
        }
        self.selectedData = None
        
        self.PopulateDevs()
        self.pushButtonEdit.setDisabled(True)
        self.pushButtonDelete.setDisabled(True)
        self.pushButtonNew.clicked.connect(self.HandleNew)
        self.pushButtonSave.clicked.connect(self.HandleSave)
        self.pushButtonEdit.clicked.connect(self.HandleEdit)
        self.pushButtonDelete.clicked.connect(self.HandleDelete)
        self.tableWidgetDevs.itemSelectionChanged.connect(self.HandleSelection)
        
    def PopulateDevs(self):
        devs = app.GetDevs(DB)
        self.tableWidgetDevs.clear()            
        self.tableWidgetDevs.setColumnCount(3)
        self.tableWidgetDevs.setHorizontalHeaderLabels(["Devs", "Alias", "Link"])
        
        # Disconnect any existing connections to avoid multiple signals
        try:
            self.tableWidgetDevs.cellClicked.disconnect()
        except:
            pass
        
        self.tableWidgetDevs.setRowCount(len(devs))
        for row_idx, row in enumerate(devs):
            # Assuming row[0] is the ID (hidden data), row[1] is Devs, and maybe row[2] is Alias?
            # Adjust indices according to your actual data structure
            item_dev = QtWidgets.QTableWidgetItem(row[1])  # Devs
            item_alias = QtWidgets.QTableWidgetItem(row[2] if len(row) > 2 else "")  # Alias
            
            item_link_text = "Link"
            item_link = self.create_link_item(row[3] if (len(row) > 3) else "", item_link_text)

            # If you need to store the ID (row[0]) with the items
            item_dev.setData(Qt.ItemDataRole.UserRole, row)

            self.tableWidgetDevs.setItem(row_idx, 0, item_dev)
            self.tableWidgetDevs.setItem(row_idx, 1, item_alias)
            if not(row[3] == "" or row[3] == None):
                self.tableWidgetDevs.setItem(row_idx, 2, item_link)
        self.tableWidgetDevs.cellClicked.connect(self.open_link)
        self.tableWidgetDevs.resizeColumnsToContents()
                
        self.LineEditDisable(True)
        
    def HandleSelection(self):
        selectedItem = self.tableWidgetDevs.selectedItems()
        if not selectedItem:
            return
        # print(selectedItem)
        self.pushButtonEdit.setDisabled(False)
        self.pushButtonDelete.setDisabled(False)
        
        item = selectedItem[0]
        row = item.row()
        self.selectedData = self.tableWidgetDevs.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # print(f"Selected ID: {self.selectedData[0]}")
        
    def ClearSelection(self):
        self.tableWidgetDevs.clearSelection()
        self.tableWidgetDevs.setCurrentItem(None)
        self.pushButtonEdit.setDisabled(True)
        self.pushButtonDelete.setDisabled(True)
            
    def LineEditDisable(self, Bool):
        self.lineEditDev.setDisabled(Bool)
        self.lineEditDevAlias.setDisabled(Bool)
        self.lineEditDevLink.setDisabled(Bool)
        
    def HandleNew(self):
        self.data['id'] = None
        self.data['name'] = None
        self.data['alias'] = None
        self.data['link'] = None
        self.lineEditDev.setText(None)
        self.lineEditDevAlias.setText(None)
        self.lineEditDevLink.setText(None)
        self.label.setText(None)
        self.ClearSelection()        
        self.LineEditDisable(False)
            
    def HandleSave(self):
        self.data['name'] = self.lineEditDev.text()
        self.data['alias'] = self.lineEditDevAlias.text()
        self.data['link'] = self.lineEditDevLink.text()
        
        if self.data['id'] == None:
            result = app.AddDevs(DB, self.data)
            if (result['success']):
                self.HandleNew()
                self.label.setText('Added Successfully!')
            else:
                self.label.setText('Duplicate, Try again!')
            self.PopulateDevs()
        else:
            result = app.updateDevs(DB, self.data)
            if (result['success']):
                self.HandleNew()
                self.label.setText('Updated Successfully!')
            else:
                self.label.setText('Duplicate, Try again!')
            self.PopulateDevs()
            
    def HandleEdit(self):
        self.data['id'] = self.selectedData[0]
        self.data['name'] = self.selectedData[1]
        self.data['alias'] = self.selectedData[2]
        self.data['link'] = self.selectedData[3]
        
        self.lineEditDev.setText(self.selectedData[1])
        self.lineEditDevAlias.setText(self.selectedData[2])
        self.lineEditDevLink.setText(self.selectedData[3])
        self.LineEditDisable(False)
    
    def HandleDelete(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle('Deleting Dev.')
        dlg.setText(f"Are sure to delete Dev.\n{self.selectedData[1]} ?")
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
        result = app.DeleteDevs(DB, id)
        if result['success']:
            self.label.setText('Delete Successfully!')
            self.HandleNew()
        else:
            self.label.setText('Deletion Failed!')
        self.PopulateDevs()
            
    def create_link_item(self, url, text):
        item = QtWidgets.QTableWidgetItem(text)
        item.setData(Qt.ItemDataRole.UserRole, url)  # Store URL
        item.setForeground(Qt.GlobalColor.blue)       # Blue text
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        return item

    def open_link(self, row, col):
        if col == 2:
            item = self.tableWidgetDevs.item(row, col)
            if item and (url := item.data(Qt.ItemDataRole.UserRole)):
                QDesktopServices.openUrl(QUrl(url))        
