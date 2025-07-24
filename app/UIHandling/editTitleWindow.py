from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QDate

from ui.edit_title_window import Ui_EditTitleDialog
import app
from main import DB

class EditTitleDialog(QtWidgets.QDialog, Ui_EditTitleDialog):
    def __init__(self, *args, obj=None, data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.data0 = data
        
        self.data = {
            'id': None,
            'title': None,
            'dev': None,
            'dev2': None,
            'plat': None,
            'rel': None,
            'status': None,
            'src': None,
            'link': None,
            'comment': None,
            }
        self.Rel = None
        self.status = None
        
        self.PopulateDevs()
        self.PopulatePlatforms()
        self.PopulateFields()
        
        self.radioButtonOG.toggled.connect(self.SelectRadio)
        self.radioButtonC.toggled.connect(self.SelectRadio)
        self.radioButtonOH.toggled.connect(self.SelectRadio)
        self.radioButtonA.toggled.connect(self.SelectRadio)
        self.checkBoxRel.toggled.connect(self.HandleRel)
        self.dateEditRel.dateChanged.connect(self.HandleRel)
        
        self.buttonBox.accepted.connect(self.Validate)
        
    def PopulateDevs(self):
        devs = app.GetDevsOrdered(DB)
        self.comboBoxDevs.clear()
        self.comboBoxDevs.setPlaceholderText(' ')
        print(devs)
        for row in devs:
            dev_row = None            
            if row[2]:
                dev_row = f"{row[1]}  [aka]  {row[2]}"
                self.comboBoxDevs.addItem(dev_row, row)
            else:
                self.comboBoxDevs.addItem(row[1], row)
            
        self.comboBoxDevs_2.clear()
        self.comboBoxDevs_2.setPlaceholderText('Optional, Only if available')
        for row in devs:
            dev_row = None            
            if row[2]:
                dev_row = f"{row[1]}  [aka]  {row[2]}"
                self.comboBoxDevs_2.addItem(dev_row, row)
            else:
                self.comboBoxDevs_2.addItem(row[1], row)
            
    def PopulatePlatforms(self):
        self.comboBoxPlatforms.clear()
        self.comboBoxPlatforms.setPlaceholderText(' ')
        platforms = app.GetPlatformsOrdered(DB)
        for row in platforms:
            self.comboBoxPlatforms.addItem(row[1], row)
            
    def PopulateFields(self):
        print(f"EDIT Data: {self.data0}")
        title = app.GetTitlesId(DB, str(self.data0))
        print(title)
        data = title[0]
        self.lineEditID.setText(str(data[0]))
        self.lineEditTitle.setText(data[1])
        if (data[2] == "N / A"):
            self.checkBoxRel.setChecked(True)
            self.dateEditRel.setDisabled(True)
        else:
            self.checkBoxRel.setChecked(False)
            self.dateEditRel.setDate(QDate.fromString(data[2], 'yyyy-MM-dd'))
        self.lineEditSRC.setText(data[3])
        self.lineEditLink.setText(data[4])
        self.plainTextEditComment.setPlainText(data[5])
        self.selectDev(data) # data[6]
        self.selectDev2(data) # data[7]
        if (data[8] == 0): self.radioButtonOG.setChecked(True)
        elif (data[8] == 1): self.radioButtonC.setChecked(True)
        elif (data[8] == 2): self.radioButtonOH.setChecked(True)
        elif (data[8] == 3): self.radioButtonA.setChecked(True)
        self.selectPlat(data) # data[10]        
        
    def selectDev(self, data):
        combo = self.comboBoxDevs
        for index in range(combo.count()):
            item_data = combo.itemData(index)
            if data[6] == item_data[0]:
                combo.setCurrentIndex(index)
                return
        combo.setCurrentIndex(-1)
        combo.setPlaceholderText('[ None ]')
        
    def selectDev2(self, data):
        combo = self.comboBoxDevs_2
        for index in range(combo.count()):
            item_data = combo.itemData(index)
            if data[7] == item_data[0]:
                combo.setCurrentIndex(index)
                return
        combo.setCurrentIndex(-1)
        combo.setPlaceholderText('[ None ]')
        
    def selectPlat(self, data):
        combo = self.comboBoxPlatforms
        for index in range(combo.count()):
            item_data = combo.itemData(index)
            if data[10] == item_data[0]:
                combo.setCurrentIndex(index)
                return
        combo.setCurrentIndex(-1)
        combo.setPlaceholderText('[ None ]')
        
    def SelectRadio(self):
        if (self.radioButtonOG.isChecked()): self.status = 0
        if (self.radioButtonC.isChecked()): self.status = 1
        if (self.radioButtonOH.isChecked()): self.status = 2
        if (self.radioButtonA.isChecked()): self.status = 3
        
    def Validate(self):
        print( self.dateEditRel.date().toPyDate(),not((self.dateEditRel.date().toString('yyyy-MM-dd') != '2000-01-01') or (self.checkBoxRel.isChecked())))
        print(f"Title: {self.lineEditTitle.text()}")
        print(f"Dev: {self.comboBoxDevs.currentIndex()}")
        print(f"Plat: {self.comboBoxPlatforms.currentIndex()}")
        print(f"Rel: {self.dateEditRel.date().toString('yyyy-MM-dd')} N/A: {self.checkBoxRel.isChecked()}")
        print(f"Status: {self.plainTextEditComment.toPlainText()}")
        print(f"Source: {self.lineEditSRC.text()}")
        print(f"Link: {self.lineEditLink.text()}")
        print(f"comment: {self.plainTextEditComment.toPlainText()}")
        
        if (self.lineEditTitle.text() == None) or \
            (self.comboBoxDevs.currentIndex == -1) or \
            (self.comboBoxPlatforms.currentIndex == -1) or \
            (not((self.dateEditRel.date().toString('yyyy-MM-dd') != '2000-01-01') or (self.checkBoxRel.isChecked()))) or \
            (not((self.radioButtonOG.isChecked() or self.radioButtonOH.isChecked() or self.radioButtonC.isChecked() or self.radioButtonA.isChecked())) or \
            (self.lineEditSRC.text() == None) or \
            (self.lineEditLink.text() == None)):
            print('Fill All Fields')
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle('Adding Title')
            dlg.setText("Fill in all the fields.")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            return
        
        self.HandleSubmit()
        
    def HandleSubmit(self):
        self.HandleRel()
        self.SelectRadio()
        print('Submitted')
        self.data['id'] = self.lineEditID.text()
        self.data['title'] = self.lineEditTitle.text()
        self.data['dev'] = self.comboBoxDevs.itemData(self.comboBoxDevs.currentIndex())[0]
        if not(self.comboBoxDevs_2.currentIndex() == -1):
            self.data['dev2'] = self.comboBoxDevs_2.itemData(self.comboBoxDevs_2.currentIndex())[0]
        self.data['rel'] = self.Rel
        # self.data['plat'] = self.comboBoxPlatforms.currentData()[0]
        self.data['plat'] = self.comboBoxPlatforms.itemData(self.comboBoxPlatforms.currentIndex())[0]
        self.data['src'] = self.lineEditSRC.text()
        self.data['link'] = self.lineEditLink.text()
        self.data['status'] = self.status
        self.data['comment'] = self.plainTextEditComment.toPlainText()
        print(self.data)
        result = app.UpdateTitle(DB, self.data)
        
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle('Editing Title')
        if (result['success']):
            dlg.setText("Title Edited Successfully!")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()
            self.close()
        else:
            dlg.setText("Title Edition Failure!")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            
    def HandleRel(self):
        if (self.checkBoxRel.isChecked()):
            self.dateEditRel.setDisabled(True)
            self.Rel = 'N / A'
        else:
            self.dateEditRel.setDisabled(False)
            self.Rel = self.dateEditRel.date().toString('yyyy-MM-dd')