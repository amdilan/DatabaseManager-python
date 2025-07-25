# Form implementation generated from reading ui file 'ui/add_new_title_window.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import app


class Ui_NewTitleDialog(object):
    def setupUi(self, NewTitleDialog):
        NewTitleDialog.setObjectName("NewTitleDialog")
        NewTitleDialog.resize(650, 385)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewTitleDialog.sizePolicy().hasHeightForWidth())
        NewTitleDialog.setSizePolicy(sizePolicy)
        NewTitleDialog.setMinimumSize(QtCore.QSize(650, 385))
        NewTitleDialog.setMaximumSize(QtCore.QSize(650, 385))
        font = QtGui.QFont()
        font.setPointSize(10)
        NewTitleDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(app.resource_path("ui\\assets\\drawer.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        NewTitleDialog.setWindowIcon(icon)
        NewTitleDialog.setSizeGripEnabled(False)
        NewTitleDialog.setModal(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=NewTitleDialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 340, 341, 32))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEditTitle = QtWidgets.QLineEdit(parent=NewTitleDialog)
        self.lineEditTitle.setGeometry(QtCore.QRect(130, 20, 500, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEditTitle.setFont(font)
        self.lineEditTitle.setText("")
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.lineEditSRC = QtWidgets.QLineEdit(parent=NewTitleDialog)
        self.lineEditSRC.setGeometry(QtCore.QRect(130, 200, 500, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEditSRC.setFont(font)
        self.lineEditSRC.setObjectName("lineEditSRC")
        self.lineEditLink = QtWidgets.QLineEdit(parent=NewTitleDialog)
        self.lineEditLink.setGeometry(QtCore.QRect(130, 230, 500, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEditLink.setFont(font)
        self.lineEditLink.setObjectName("lineEditLink")
        self.label = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.comboBoxDevs = QtWidgets.QComboBox(parent=NewTitleDialog)
        self.comboBoxDevs.setGeometry(QtCore.QRect(130, 50, 473, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBoxDevs.setFont(font)
        self.comboBoxDevs.setPlaceholderText("")
        self.comboBoxDevs.setObjectName("comboBoxDevs")
        self.label_4 = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label_4.setGeometry(QtCore.QRect(20, 200, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.dateEditRel = QtWidgets.QDateEdit(parent=NewTitleDialog)
        self.dateEditRel.setGeometry(QtCore.QRect(130, 140, 110, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.dateEditRel.setFont(font)
        self.dateEditRel.setFrame(True)
        self.dateEditRel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dateEditRel.setMinimumDate(QtCore.QDate(2000, 1, 1))
        self.dateEditRel.setCalendarPopup(True)
        self.dateEditRel.setDate(QtCore.QDate(2000, 1, 1))
        self.dateEditRel.setObjectName("dateEditRel")
        self.pushButton = QtWidgets.QPushButton(parent=NewTitleDialog)
        self.pushButton.setGeometry(QtCore.QRect(608, 50, 22, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(app.resource_path("ui\\assets\\add-dev.png")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        self.label_5 = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label_5.setGeometry(QtCore.QRect(20, 230, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label_6.setGeometry(QtCore.QRect(20, 110, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.comboBoxPlatforms = QtWidgets.QComboBox(parent=NewTitleDialog)
        self.comboBoxPlatforms.setGeometry(QtCore.QRect(130, 110, 250, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBoxPlatforms.setFont(font)
        self.comboBoxPlatforms.setPlaceholderText("")
        self.comboBoxPlatforms.setObjectName("comboBoxPlatforms")
        self.label_7 = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label_7.setGeometry(QtCore.QRect(20, 260, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.plainTextEditComment = QtWidgets.QPlainTextEdit(parent=NewTitleDialog)
        self.plainTextEditComment.setGeometry(QtCore.QRect(130, 260, 500, 66))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.plainTextEditComment.setFont(font)
        self.plainTextEditComment.setPlainText("")
        self.plainTextEditComment.setObjectName("plainTextEditComment")
        self.checkBoxRel = QtWidgets.QCheckBox(parent=NewTitleDialog)
        self.checkBoxRel.setGeometry(QtCore.QRect(250, 141, 51, 20))
        self.checkBoxRel.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.checkBoxRel.setObjectName("checkBoxRel")
        self.label_8 = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label_8.setGeometry(QtCore.QRect(20, 170, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.widget = QtWidgets.QWidget(parent=NewTitleDialog)
        self.widget.setGeometry(QtCore.QRect(130, 160, 501, 40))
        self.widget.setObjectName("widget")
        self.radioButtonOG = QtWidgets.QRadioButton(parent=self.widget)
        self.radioButtonOG.setGeometry(QtCore.QRect(10, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioButtonOG.setFont(font)
        self.radioButtonOG.setObjectName("radioButtonOG")
        self.radioButtonOH = QtWidgets.QRadioButton(parent=self.widget)
        self.radioButtonOH.setGeometry(QtCore.QRect(120, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioButtonOH.setFont(font)
        self.radioButtonOH.setObjectName("radioButtonOH")
        self.radioButtonC = QtWidgets.QRadioButton(parent=self.widget)
        self.radioButtonC.setGeometry(QtCore.QRect(230, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioButtonC.setFont(font)
        self.radioButtonC.setObjectName("radioButtonC")
        self.radioButtonA = QtWidgets.QRadioButton(parent=self.widget)
        self.radioButtonA.setGeometry(QtCore.QRect(340, 10, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioButtonA.setFont(font)
        self.radioButtonA.setObjectName("radioButtonA")
        self.label_9 = QtWidgets.QLabel(parent=NewTitleDialog)
        self.label_9.setGeometry(QtCore.QRect(20, 80, 111, 22))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.comboBoxDevs_2 = QtWidgets.QComboBox(parent=NewTitleDialog)
        self.comboBoxDevs_2.setGeometry(QtCore.QRect(130, 80, 473, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBoxDevs_2.setFont(font)
        self.comboBoxDevs_2.setPlaceholderText("")
        self.comboBoxDevs_2.setObjectName("comboBoxDevs_2")
        self.lineEditSRC.raise_()
        self.buttonBox.raise_()
        self.lineEditTitle.raise_()
        self.lineEditLink.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.comboBoxDevs.raise_()
        self.label_4.raise_()
        self.dateEditRel.raise_()
        self.pushButton.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.comboBoxPlatforms.raise_()
        self.label_7.raise_()
        self.plainTextEditComment.raise_()
        self.checkBoxRel.raise_()
        self.label_8.raise_()
        self.widget.raise_()
        self.label_9.raise_()
        self.comboBoxDevs_2.raise_()

        self.retranslateUi(NewTitleDialog)
        self.buttonBox.rejected.connect(NewTitleDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(NewTitleDialog)
        NewTitleDialog.setTabOrder(self.lineEditTitle, self.comboBoxDevs)
        NewTitleDialog.setTabOrder(self.comboBoxDevs, self.pushButton)
        NewTitleDialog.setTabOrder(self.pushButton, self.comboBoxDevs_2)
        NewTitleDialog.setTabOrder(self.comboBoxDevs_2, self.comboBoxPlatforms)
        NewTitleDialog.setTabOrder(self.comboBoxPlatforms, self.dateEditRel)
        NewTitleDialog.setTabOrder(self.dateEditRel, self.checkBoxRel)
        NewTitleDialog.setTabOrder(self.checkBoxRel, self.radioButtonOG)
        NewTitleDialog.setTabOrder(self.radioButtonOG, self.radioButtonOH)
        NewTitleDialog.setTabOrder(self.radioButtonOH, self.radioButtonC)
        NewTitleDialog.setTabOrder(self.radioButtonC, self.radioButtonA)
        NewTitleDialog.setTabOrder(self.radioButtonA, self.lineEditSRC)
        NewTitleDialog.setTabOrder(self.lineEditSRC, self.lineEditLink)
        NewTitleDialog.setTabOrder(self.lineEditLink, self.plainTextEditComment)

    def retranslateUi(self, NewTitleDialog):
        _translate = QtCore.QCoreApplication.translate
        NewTitleDialog.setWindowTitle(_translate("NewTitleDialog", "Add New Title"))
        self.label.setText(_translate("NewTitleDialog", "Title"))
        self.label_2.setText(_translate("NewTitleDialog", "Developer"))
        self.label_3.setText(_translate("NewTitleDialog", "Release Date"))
        self.label_4.setText(_translate("NewTitleDialog", "Source"))
        self.dateEditRel.setDisplayFormat(_translate("NewTitleDialog", "yyyy-MM-dd"))
        self.pushButton.setToolTip(_translate("NewTitleDialog", "Add New Developer"))
        self.label_5.setText(_translate("NewTitleDialog", "Web Link"))
        self.label_6.setText(_translate("NewTitleDialog", "Engine"))
        self.label_7.setText(_translate("NewTitleDialog", "Comments"))
        self.checkBoxRel.setToolTip(_translate("NewTitleDialog", "Check if date not available"))
        self.checkBoxRel.setText(_translate("NewTitleDialog", "N/A"))
        self.label_8.setText(_translate("NewTitleDialog", "Dev. Status"))
        self.radioButtonOG.setText(_translate("NewTitleDialog", "On Going"))
        self.radioButtonOH.setText(_translate("NewTitleDialog", "On Hold"))
        self.radioButtonC.setText(_translate("NewTitleDialog", "Completed"))
        self.radioButtonA.setText(_translate("NewTitleDialog", "Abandoned"))
        self.label_9.setText(_translate("NewTitleDialog", "Developer 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewTitleDialog = QtWidgets.QDialog()
    ui = Ui_NewTitleDialog()
    ui.setupUi(NewTitleDialog)
    NewTitleDialog.show()
    sys.exit(app.exec())
