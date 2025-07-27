from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from ui.add_new_title_window import Ui_NewTitleDialog
import app
from main import DB

class NewTitleDialog(QtWidgets.QDialog, Ui_NewTitleDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.data = {
            'title': None,
            'dev': None,
            'dev2': None,
            'plat': None,
            'rel': None,
            'status': None,
            'src': None,
            'link': None,
            'comment': None,
            'avail': None,
            }
        self.Rel = None
        self.status = None
        
        # self.comboBoxDevs_2.setStyleSheet("QComboBox QAbstractItemView { color: black; }")
        
        self.PopulateDevs()
        self.PopulatePlatforms()
        
        self.pushButton.clicked.connect(self.HandleAddDev)
        
        self.radioButtonOG.toggled.connect(self.SelectRadio)
        self.radioButtonC.toggled.connect(self.SelectRadio)
        self.radioButtonOH.toggled.connect(self.SelectRadio)
        self.radioButtonA.toggled.connect(self.SelectRadio)
        self.checkBoxRel.toggled.connect(self.HandleRel)
        self.dateEditRel.dateChanged.connect(self.HandleRel)
        
        self.buttonBox.accepted.connect(self.Validate)
               
    def HandleAddDev(self):
        dlg = app.DevDialog()
        dlg.exec()
        self.PopulateDevs()
               
    def PopulateDevs(self):
        devs = app.GetDevsOrdered(DB)
        self.comboBoxDevs.clear()
        self.comboBoxDevs.setPlaceholderText(' ')
        # print(devs)
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
            
    def SelectRadio(self):
        if (self.radioButtonOG.isChecked()): self.status = 0
        if (self.radioButtonC.isChecked()): self.status = 1
        if (self.radioButtonOH.isChecked()): self.status = 2
        if (self.radioButtonA.isChecked()): self.status = 3
        
    def HandleRel(self):
        if (self.checkBoxRel.isChecked()):
            self.dateEditRel.setDisabled(True)
            self.Rel = 'N / A'
        else:
            self.dateEditRel.setDisabled(False)
            self.Rel = self.dateEditRel.date().toString('yyyy-MM-dd')
                    
    def HandleSubmit(self):        
        # print('Submitted')
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
        # print(self.data)
        result = app.AddTitles(DB, self.data)
        
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle('Adding Title')
        if (result['success']):
            dlg.setText("Title Added Successfully!")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()
            self.close()
        else:
            dlg.setText("Title Addition Failure!")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
        
    def Validate(self):                
        # print( self.dateEditRel.date().toPyDate(),not((self.dateEditRel.date().toString('yyyy-MM-dd') != '2000-01-01') or (self.checkBoxRel.isChecked())))
        # print(f"Title: {self.lineEditTitle.text()}")
        # print(f"Dev: {self.comboBoxDevs.currentIndex()}")
        # print(f"Plat: {self.comboBoxPlatforms.currentIndex()}")
        # print(f"Rel: {self.dateEditRel.date().toString('yyyy-MM-dd')} N/A: {self.checkBoxRel.isChecked()}")
        # print(f"Status: {self.plainTextEditComment.toPlainText()}")
        # print(f"Source: {self.lineEditSRC.text()}")
        # print(f"Link: {self.lineEditLink.text()}")
        # print(f"comment: {self.plainTextEditComment.toPlainText()}")
        
        dev1 = self.comboBoxDevs.currentData()
        dev2 = self.comboBoxDevs_2.currentData() if self.comboBoxDevs_2.currentIndex() >= 0 else None
        
        if dev2 is not None and dev1[0] == dev2[0]:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle('Error')
            dlg.setText("You cannot select the same developer in both fields.")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            self.PopulateDevs()
            return
        
        if (self.lineEditTitle.text() == None) or \
            (self.comboBoxDevs.currentIndex() == -1) or \
            (self.comboBoxPlatforms.currentIndex() == -1) or \
            (not((self.dateEditRel.date().toString('yyyy-MM-dd') != '2000-01-01') or (self.checkBoxRel.isChecked()))) or \
            (not((self.radioButtonOG.isChecked() or self.radioButtonOH.isChecked() or self.radioButtonC.isChecked() or self.radioButtonA.isChecked())) or \
            (self.lineEditSRC.text() == None) or \
            (self.lineEditLink.text() == None)):
            # print('Fill All Fields')
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle('Adding Title')
            dlg.setText("Fill in all the fields.")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            return
        
        self.HandleSubmit()
