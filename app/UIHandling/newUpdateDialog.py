from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from ui.add_new_update_window import Ui_NewUpdateDialog
import app
from main import DB

class NewUpdateDialog(QtWidgets.QDialog, Ui_NewUpdateDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.data = {}
        
        self.PopulateTitle()
        
        self.radioButtonP_NP.toggled.connect(self.SelectRadioStatusPlaying)
        self.radioButtonP_P.toggled.connect(self.SelectRadioStatusPlaying)
        self.radioButtonP_PD.toggled.connect(self.SelectRadioStatusPlaying)
        self.radioButtonU_A.toggled.connect(self.SelectRadioStatusUpdate)
        self.radioButtonU_DS.toggled.connect(self.SelectRadioStatusUpdate)
        self.radioButtonU_NA.toggled.connect(self.SelectRadioStatusUpdate)
        self.radioButtonU_TD.toggled.connect(self.SelectRadioStatusUpdate)
        self.comboBox.currentIndexChanged.connect(self.SelectTitle)
        self.checkBoxRel.toggled.connect(self.HandleRel)
        self.dateEditRel.dateChanged.connect(self.HandleRel)
        
        self.buttonBox.accepted.connect(self.Validate)
        
    def PopulateTitle(self):
        title = app.GetTitlesName(DB)
        self.comboBox.clear()
        self.comboBox.setPlaceholderText(' ')
        for row in title:
            self.comboBox.addItem(row[1], row[0])
            
    def SelectTitle(self):
        self.lineEditID.setText(str(self.comboBox.itemData(self.comboBox.currentIndex())))
    
    def SelectRadioStatusUpdate(self):
        if (self.radioButtonU_NA.isChecked()): self.data['update'] = 0
        if (self.radioButtonU_A.isChecked()): self.data['update'] = 1
        if (self.radioButtonU_TD.isChecked()): self.data['update'] = 2
        if (self.radioButtonU_DS.isChecked()): self.data['update'] = 3
    
    def SelectRadioStatusPlaying(self):
        if (self.radioButtonP_NP.isChecked()): self.data['play'] = 0
        if (self.radioButtonP_P.isChecked()): self.data['play'] = 1
        if (self.radioButtonP_PD.isChecked()): self.data['play'] = 2
        
    def HandleRel(self):
        if (self.checkBoxRel.isChecked()):
            self.dateEditRel.setDisabled(True)
            self.data['rel'] = 'N / A'
        else:
            self.dateEditRel.setDisabled(False)
            self.data['rel'] = self.dateEditRel.date().toString('yyyy-MM-dd')
        
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
        self.data['id'] = self.lineEditID.text()
        self.data['name'] = self.lineEditName.text()
        self.data['comment'] = self.plainTextEditComment.toPlainText()
        # print(self.data)
        result = app.AddUpdates(DB, self.data)
        
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle('Adding Title')
        if (result['success']):
            dlg.setText("Update Added Successfully!")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()
            self.close()
        else:
            dlg.setText("Update Addition Failure!")
            dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()