from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from ui.main_window import Ui_MainWindow
import app
import time
from main import DB

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.PopulateTitles()
        
        self.pushButtonNewUpdate.clicked.connect(self.HandleNewUpdateClick)
        self.pushButtonNewTitle.clicked.connect(self.HandleNewTitleClick)
        self.actionTheme.changed.connect(self.HandleNewThemeChanged)
        self.actionPlatforms.triggered.connect(self.HandleMenuPlatforms)
        self.actionDevelopers.triggered.connect(self.HandleMenuDevs)
                
    def HandleNewTitleClick(self):
        # print("...")
        dlg = NewTitleDialog()
        dlg.exec()
        
    def HandleNewUpdateClick(self):
        # print(".....")
        dlg = NewUpdateDialog()
        dlg.exec()
    
    def HandleNewThemeChanged(self):
        # print(".")
        pass
    
    def CheckDarkTheme(self, CONFIG_FILE):
        if app.IsDarkTheme(CONFIG_FILE):
            self.actionTheme.setChecked(True)
        else:
            self.actionTheme.setChecked(False)
            
    def HandleMenuPlatforms(self):
        dlg = PlatformDialog()
        dlg.exec()
    
    def HandleMenuDevs(self):
        dlg = DevDialog()
        dlg.exec()
        
    def PopulateTitles(self):
        self.tableWidgetTitles.clear()
        titles = app.GetTitles(DB)
        self.tableWidgetTitles.setColumnCount(9)
        self.tableWidgetTitles.setHorizontalHeaderLabels(["ID", "Name", "Devs", "Released", "Status", "Platform", "Web Link", "Availability", "Comment"])
        
        try:
            self.tableWidgetTitles.cellClicked.disconnect()
        except:
            pass
        
        self.tableWidgetTitles.setRowCount(len(titles))
        
        self.tableWidgetTitles.resizeColumnsToContents()
                        
from ui.add_new_title_window import Ui_NewTitleDialog

class NewTitleDialog(QtWidgets.QDialog, Ui_NewTitleDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.data = {
            'title': '',
            'dev': '',
            'dev2': '',
            'plat': '',
            'rel': '',
            'status ': '',
            'src': '',
            'link ': '',
            'comment': '',
            'avail': '',
            }
        self.Rel = ''
        self.status = ''
        
        self.PopulateDevs()
        self.PopulatePlatforms()
        
        self.buttonBox.accepted.connect(self.Validate)
               
    def PopulateDevs(self):
        self.comboBoxDevs.clear()
        devs = app.GetDevs(DB)
        # print(devs)
        for row in devs:
            self.comboBoxDevs.addItem(row[1], row[0])
            
    def PopulatePlatforms(self):
        self.comboBoxPlatforms.clear()
        platforms = app.GetPlatforms(DB)
        for row in platforms:
            self.comboBoxPlatforms.addItem(row[1], row[0])
            
    def SelectRadio(self):
        if (self.radioButtonOG.isChecked()): self.status
        if (self.radioButtonOH.isChecked()): pass
        if (self.radioButtonC.isChecked()): pass
        if (self.radioButtonA.isChecked()): pass
                    
    def HandleSubmit(self):
        # print('Submitted')
        self.data['title'] = self.lineEditTitle.text()
        self.data['dev'] = self.comboBoxDevs.itemData(self.comboBoxDevs.currentIndex())
        self.data['dev2'] = ''
        self.data['rel'] = self.Rel
        self.data['plat'] = self.comboBoxPlatforms.itemData(self.comboBoxPlatforms.currentIndex)
        self.data['src'] = self.lineEditSRC.text()
        self.data['link'] = self.lineEditLink.text()
        # self.data['avail'] = self.
        self.data['status'] = self.status
        self.data['comment'] = self.plainTextEditComment.toPlainText()
        # print(self.dateEditRel.date().toPyDate())
        # print(self.data)
        
    def Validate(self):
        if (self.lineEditTitle.text() == '') or (self.comboBoxDevs.currentIndex == -1) or (self.comboBoxPlatforms.currentIndex == -1) or (not((self.dateEditRel.date().toString('yyyy-MM-dd') != '2000-01-01') or (self.checkBoxRel.isChecked()))) or ((self.radioButtonOG.isChecked() or self.radioButtonOH.isChecked() or self.radioButtonC.isChecked() or self.radioButtonA.isChecked()) or (self.lineEditSRC.text() == '') or (self.lineEditLink.text() == '')):
            # print( self.dateEditRel.date().toPyDate(),not((self.dateEditRel.date().toString('yyyy-MM-dd') != '2000-01-01') or (self.checkBoxRel.isChecked())))
            # print(f"comment: {self.plainTextEditComment.toPlainText()}")
            # print('Fill All Fields')
            return
        
        self.HandleSubmit()
                    
from ui.add_new_update_window import Ui_NewUpdateDialog

class NewUpdateDialog(QtWidgets.QDialog, Ui_NewUpdateDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
from ui.platforms_dialog import Ui_PlatformDialog        

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
        
from ui.Devs_dialog import Ui_DevDialog

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
    
    
from ui.message_dialog import Ui_MessageDialog
            
class MsgDialog(QtWidgets.QDialog, Ui_MessageDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
    def SetTitle(self, Title):
        self.MessageDialog.title(f"{Title}")
