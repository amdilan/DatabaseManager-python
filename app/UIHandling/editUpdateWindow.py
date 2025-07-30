from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QDate

from ui.edit_update_window import Ui_EditUpdateDialog
import app
from main import DB

class EditUpdateDialog(QtWidgets.QDialog, Ui_EditUpdateDialog):
    def __init__(self, *args, obj=None, data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.data0 = data
        
        self.data = {}
        
        self.PopulateTitle()
        self.PopulateFields()
        
        self.radioButtonP_NP.toggled.connect(self.SelectRadioStatusPlaying)
        self.radioButtonP_P.toggled.connect(self.SelectRadioStatusPlaying)
        self.radioButtonP_PD.toggled.connect(self.SelectRadioStatusPlaying)
        self.radioButtonU_A.toggled.connect(self.SelectRadioStatusUpdate)
        self.radioButtonU_DS.toggled.connect(self.SelectRadioStatusUpdate)
        self.radioButtonU_NA.toggled.connect(self.SelectRadioStatusUpdate)
        self.radioButtonU_TD.toggled.connect(self.SelectRadioStatusUpdate)
        # self.comboBox.currentIndexChanged.connect(self.SelectTitle)
        self.checkBoxRel.toggled.connect(self.HandleRel)
        self.dateEditRel.dateChanged.connect(self.HandleRel)
        
        self.buttonBox.accepted.connect(self.Validate)
        
    def PopulateTitle(self):
        title = app.GetTitlesName(DB)
        self.comboBox.clear()
        self.comboBox.setPlaceholderText(' ')
        for row in title:
            self.comboBox.addItem(row[1], row[0])
            
    def SelectRadioStatusUpdate(self):
        if (self.radioButtonU_NA.isChecked()): self.data['update'] = 0
        if (self.radioButtonU_A.isChecked()): self.data['update'] = 1
        if (self.radioButtonU_TD.isChecked()): self.data['update'] = 2
        if (self.radioButtonU_DS.isChecked()): self.data['update'] = 3
    
    def SelectRadioStatusPlaying(self):
        if (self.radioButtonP_NP.isChecked()): self.data['play'] = 0
        if (self.radioButtonP_P.isChecked()): self.data['play'] = 1
        if (self.radioButtonP_PD.isChecked()): self.data['play'] = 2
        
    def selectTitle(self, data):
        combo = self.comboBox
        for index in range(combo.count()):
            item_data = combo.itemData(index)
            if data[1] == item_data:
                combo.setCurrentIndex(index)
                return
        combo.setCurrentIndex(-1)
        combo.setPlaceholderText('[ None ]')
        
    def HandleRel(self):
        if (self.checkBoxRel.isChecked()):
            self.dateEditRel.setDisabled(True)
            self.data['rel'] = 'N / A'
        else:
            self.dateEditRel.setDisabled(False)
            self.data['rel'] = self.dateEditRel.date().toString('yyyy-MM-dd')
            
    def PopulateFields(self):
        update = app.GetUpdatesId(DB, str(self.data0))
        data = update[0]
        # print(update)
        self.lineEditUID.setText(str(data[0]))
        self.lineEditID.setText(str(data[1]))
        self.selectTitle(data) # title
        self.lineEditName.setText(data[2])
        if (data[3] == "N / A"):
            self.checkBoxRel.setChecked(True)
            self.dateEditRel.setDisabled(True)
        else:
            self.checkBoxRel.setChecked(False)
            self.dateEditRel.setDate(QDate.fromString(data[3], 'yyyy-MM-dd'))
        if (data[4] == 0): self.radioButtonU_NA.setChecked(True)
        elif (data[4] == 1): self.radioButtonU_A.setChecked(True)
        elif (data[4] == 2): self.radioButtonU_TD.setChecked(True)
        elif (data[4] == 3): self.radioButtonU_DS.setChecked(True)
        if (data[5] == 0): self.radioButtonP_NP.setChecked(True)
        elif (data[5] == 1): self.radioButtonP_P.setChecked(True)
        elif (data[5] == 2): self.radioButtonP_PD.setChecked(True)
        self.plainTextEditComment.setPlainText(data[6])
        
    def Validate(self):
        if (self.comboBox.currentIndex() == -1) or \
            (self.lineEditName.text() == None) or \
            (not((self.dateEditRel.date().toString('yyyy-MM-dd') != '2000-01-01') or (self.checkBoxRel.isChecked()))) or \
            (not(self.radioButtonP_NP.isChecked() or self.radioButtonP_P.isChecked() or self.radioButtonP_PD.isChecked())) or \
            (not(self.radioButtonU_A.isChecked() or self.radioButtonU_DS.isChecked() or self.radioButtonU_NA.isChecked() or self.radioButtonU_TD.isChecked())):
                # print('Fill All Fields')
                dlg = QtWidgets.QMessageBox(self)
                dlg.setWindowTitle('Adding Title')
                dlg.setText("Fill in all the fields.")
                dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()
                return
        
        self.HandleSubmit()
        
    def HandleSubmit(self):
        self.data['id'] = self.lineEditUID.text()
        self.data['tid'] = self.lineEditID.text()
        self.data['name'] = self.lineEditName.text()
        self.data['comment'] = self.plainTextEditComment.toPlainText()
        self.HandleRel()
        self.SelectRadioStatusPlaying()
        self.SelectRadioStatusUpdate()
        # print(self.data)
        result = app.UpdateUpdate(DB, self.data)
        
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle('Editing Title')
        if (result['success']):
            dlg.setText("Update Edited Successfully!")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()
            self.close()
            super().accept()
        else:
            dlg.setText("Update Edition Failure!")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()