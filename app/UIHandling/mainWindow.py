from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QDesktopServices, QColor, QBrush

from ui.main_window import Ui_MainWindow
import app
from main import DB, CONFIG_FILE

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.PopulateStats()
        
        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        self.actionTheme.triggered.connect(self.ChangeTheme)
        
        self.toolButtonRefreshTitle.clicked.connect(self.PopulateTitles)
        self.toolButtonRefreshUpdate.clicked.connect(self.PopulateUpdates)
        
        self.pushButtonNewUpdate.clicked.connect(self.HandleNewUpdateClick)
        self.pushButtonNewTitle.clicked.connect(self.HandleNewTitleClick)
        self.actionTheme.changed.connect(self.HandleNewThemeChanged)
        self.actionPlatforms.triggered.connect(self.HandleMenuPlatforms)
        self.actionDevelopers.triggered.connect(self.HandleMenuDevs)
        self.actionAbout.triggered.connect(self.HandleAbout)
        
        self.lineEditSearchTitle.textChanged.connect(self.start_search_time_Title)
        self.lineEditSearchUpdate.textChanged.connect(self.start_search_time_Update)
        
         # Search delay timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filterTableTitle)
        
         # Search delay timer
        self.search_timerUpdate = QTimer()
        self.search_timerUpdate.setSingleShot(True)
        self.search_timerUpdate.timeout.connect(self.filterTableUpdate)
        
    def start_search_time_Title(self):
        self.search_timer.start(300)  # 300ms delay before searching
        
    def start_search_time_Update(self):
        self.search_timerUpdate.start(300)  # 300ms delay before searching
                
    def on_tab_changed(self, index):
        """Triggered when tab changes"""        
        # You can add your custom logic here
        if index == 0:
            self.PopulateStats()
        elif index == 1:
            self.PopulateTitles()
        elif index == 2:
            self.PopulateUpdates()
                
    def HandleNewTitleClick(self):
        print("...")
        dlg = app.NewTitleDialog()
        dlg.exec()
        self.PopulateTitles()
        
    def HandleNewUpdateClick(self):
        print(".....")
        dlg = app.NewUpdateDialog()
        dlg.exec()
        self.PopulateUpdates()
    
    def HandleNewThemeChanged(self):
        print(".")
        pass
    
    def CheckDarkTheme(self, CONFIG_FILE):
        if app.IsDarkTheme(CONFIG_FILE):
            self.actionTheme.setChecked(True)
        else:
            self.actionTheme.setChecked(False)
           
    def ChangeTheme(self):
        if (self.actionTheme.isChecked()):
            app.WriteConfigTheme(CONFIG_FILE, 'dark')
            self.HandleRestart()
        else:
            app.WriteConfigTheme(CONFIG_FILE, 'light')
            self.HandleRestart()
            
    def HandleRestart(self):
        dlg = QtWidgets.QMessageBox.question(
            self, 'Changing Theme',
            "The theme change will applied after application restart.\nPlease close application, and run the application again!",
            QtWidgets.QMessageBox.StandardButton.Ok
        )        
                    
    def HandleMenuPlatforms(self):
        dlg = app.PlatformDialog()
        dlg.exec()
    
    def HandleMenuDevs(self):
        dlg = app.DevDialog()
        dlg.exec()
        
    def HandleAbout(self):
        dlg = app.AboutDialog()
        dlg.exec()
    
    def PopulateStats(self):
        lcdTotalTitles = self.lcdNumberT0
        lcdTotalTOngoing = self.lcdNumberT1
        lcdTotalTOnhold = self.lcdNumberT2
        lcdTotalTCompleted = self.lcdNumberT3
        lcdTotalTAbandoned = self.lcdNumberT4
        
        lcdTotalUpdates = self.lcdNumberU0
        lcdTotalUA = self.lcdNumberU1
        lcdTotalUNA = self.lcdNumberU2
        lcdTotalUTD = self.lcdNumberU3
        lcdTotalUDS = self.lcdNumberU4
        
        lcdUTAvail = self.lcdNumberTU0
        lcdUTP = self.lcdNumberTU1
        lcdUTNP = self.lcdNumberTU2
        lcdUTNotAvail = self.lcdNumberTU3
        lcdUTPD = self.lcdNumberTU4
        
        tt = app.GetCountTitles(DB)
        ts = app.GetCountTitleStatus(DB)
        lcdTotalTitles.display(tt[0][0])
        lcdTotalTOngoing.display(ts[0][1])
        lcdTotalTCompleted.display(ts[1][1])
        lcdTotalTOnhold.display(ts[2][1])
        lcdTotalTAbandoned.display(ts[3][1])
        
        tu = app.GetCountUpdates(DB)
        us = app.GetCountUpdateStatus(DB)
        lcdTotalUpdates.display(tu[0][0])
        lcdTotalUNA.display(us[0][1])
        lcdTotalUA.display(us[1][1])
        lcdTotalUTD.display(us[2][1])
        lcdTotalUDS.display(us[3][1])
        
        ta = app.GetCountTitleAvail(DB)
        lcdUTNotAvail.display(ta[0][1])
        lcdUTAvail.display(ta[1][1])
        tp = app.GetCountUpdatePlay(DB)
        lcdUTNP.display(tp[0][1])
        lcdUTP.display(tp[1][1])
        lcdUTPD.display(tp[2][1])
                
    def PopulateTitles(self):
        self.tableWidgetTitles.clear()
        titles = app.GetTitleDetails(DB)
        print(titles)
        self.tableWidgetTitles.setColumnCount(10)
        self.tableWidgetTitles.setHorizontalHeaderLabels(["T. ID", "Name", "Devs", "Released", "Status", "Platform", "Web Link", "Availability", "Comment", ""])
        
        try:
            self.tableWidgetTitles.cellClicked.disconnect()
        except:
            pass
        
        self.tableWidgetTitles.setRowCount(len(titles))
        for row_idx, row in enumerate(titles):
            item_id = QtWidgets.QTableWidgetItem(str(row[0]))
            item_name = QtWidgets.QTableWidgetItem(row[1])
            item_rel = QtWidgets.QTableWidgetItem(row[4])
            item_status = QtWidgets.QTableWidgetItem(row[5])
            item_plat = QtWidgets.QTableWidgetItem(row[6])
            item_link_text = QtWidgets.QTableWidgetItem(row[7])
            item_link_src = row[8]
            item_avail = QtWidgets.QTableWidgetItem(row[9])
            item_comment = QtWidgets.QTableWidgetItem(row[10])

            item_link = None
            if not(item_link_src == "" or item_link_src == None):
                item_link = self.create_link_item(item_link_src, item_link_text)
            
            item_devs = None
            dev_names = []
            if row[2]:
                if row[11]:
                    dev_name = f"{row[2]} [aka] {row[11]}"
                    dev_names.append(dev_name)
                else:
                    dev_names.append(row[2])
            if row[3]:
                if row[12]:
                    dev_name = f"{row[3]} [aka] {row[12]}"
                    dev_names.append(dev_name)
                else:
                    dev_names.append(row[3])
            dev_text = "\n".join(dev_names)
            item_devs = QtWidgets.QTableWidgetItem(dev_text)
            # item_devs.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  
            item_devs.setTextAlignment(Qt.AlignmentFlag.AlignLeft)  
            self.tableWidgetTitles.setStyleSheet("""
                    QTableWidget {
                        gridline-color: #ccc;
                    }
                    QTableWidget::item {
                        padding: 3px;
                    }
                """)
            
            self.tableWidgetTitles.setWordWrap(True)
            item_id.setData(Qt.ItemDataRole.UserRole, row)
            
            self.tableWidgetTitles.setItem(row_idx, 0, item_id)
            self.tableWidgetTitles.setItem(row_idx, 1, item_name)
            self.tableWidgetTitles.setItem(row_idx, 2, item_devs)
            self.tableWidgetTitles.setItem(row_idx, 3, item_rel)
            self.tableWidgetTitles.setItem(row_idx, 4, item_status)
            self.tableWidgetTitles.setItem(row_idx, 5, item_plat)
            self.tableWidgetTitles.setItem(row_idx, 6, item_link)
            self.tableWidgetTitles.setItem(row_idx, 7, item_avail)
            self.tableWidgetTitles.setItem(row_idx, 8, item_comment)
            
            # Create a tool button with menu for actions column
            tool_button = QtWidgets.QToolButton()
            tool_button.setText("⋮")  # Vertical ellipsis character
            tool_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")

            # Create menu
            menu = QtWidgets.QMenu()
            edit_action = menu.addAction("Edit")
            delete_action = menu.addAction("Delete")
            
            # Connect actions to slots
            edit_action.triggered.connect(lambda _, r=row_idx: self.edit_title(r))
            delete_action.triggered.connect(lambda _, r=row_idx: self.delete_title(r))
            
            tool_button.setMenu(menu)
            tool_button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        
            # Add the button to the table
            self.tableWidgetTitles.setCellWidget(row_idx, 9, tool_button)
            
        self.tableWidgetTitles.cellClicked.connect(self.open_link)
        self.tableWidgetTitles.resizeColumnsToContents()
        self.tableWidgetTitles.resizeRowsToContents()
        
    def PopulateUpdates(self):
        self.tableWidgetUpdate.clear()
        titles = app.GetUpdateDetails(DB)
        print(titles)
        self.tableWidgetUpdate.setColumnCount(9)
        self.tableWidgetUpdate.setHorizontalHeaderLabels(["U. ID", "T. ID", "Title", "Version", "Released", "Update Status", "Play Status", "Comment", ""])
        
        try:
            self.tableWidgetUpdate.cellClicked.disconnect()
        except:
            pass
        
        self.tableWidgetUpdate.setRowCount(len(titles))
        for row_idx, row in enumerate(titles):
            item_id = QtWidgets.QTableWidgetItem(str(row[0]))
            item_Tid = QtWidgets.QTableWidgetItem(str(row[1]))
            item_title = QtWidgets.QTableWidgetItem(row[2])
            item_update = QtWidgets.QTableWidgetItem(row[3])
            item_rel = QtWidgets.QTableWidgetItem(row[4])
            item_US = QtWidgets.QTableWidgetItem(row[5])
            item_PS = QtWidgets.QTableWidgetItem(row[6])
            item_comment = QtWidgets.QTableWidgetItem(row[7])
            self.tableWidgetUpdate.setStyleSheet("""
                    QTableWidget {
                        gridline-color: #ccc;
                    }
                    QTableWidget::item {
                        padding: 3px;
                    }
                """)
            
            self.tableWidgetUpdate.setWordWrap(True)
            item_id.setData(Qt.ItemDataRole.UserRole, row)
            
            self.tableWidgetUpdate.setItem(row_idx, 0, item_id)
            self.tableWidgetUpdate.setItem(row_idx, 1, item_Tid)
            self.tableWidgetUpdate.setItem(row_idx, 2, item_title)
            self.tableWidgetUpdate.setItem(row_idx, 3, item_update)
            self.tableWidgetUpdate.setItem(row_idx, 4, item_rel)
            self.tableWidgetUpdate.setItem(row_idx, 5, item_US)
            self.tableWidgetUpdate.setItem(row_idx, 6, item_PS)
            self.tableWidgetUpdate.setItem(row_idx, 7, item_comment)
            
            # Create a tool button with menu for actions column
            tool_button = QtWidgets.QToolButton()
            tool_button.setText("⋮")  # Vertical ellipsis character
            tool_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")

            # Create menu
            menu = QtWidgets.QMenu()
            edit_action = menu.addAction("Edit")
            delete_action = menu.addAction("Delete")
            
            # Connect actions to slots
            edit_action.triggered.connect(lambda _, r=row_idx: self.edit_update(r))
            delete_action.triggered.connect(lambda _, r=row_idx: self.delete_update(r))
            
            tool_button.setMenu(menu)
            tool_button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        
            # Add the button to the table
            self.tableWidgetUpdate.setCellWidget(row_idx, 8, tool_button)
            
        self.tableWidgetUpdate.cellClicked.connect(self.open_link)
        self.tableWidgetUpdate.resizeColumnsToContents()
        self.tableWidgetUpdate.resizeRowsToContents()
        
    def edit_title(self, row):
        print(f"Editing row {row}")
        item = self.tableWidgetTitles.item(row, 0)
        if item:
            row_data = item.data(Qt.ItemDataRole.UserRole)
        dlg = app.EditTitleDialog(data=row_data[0])
        dlg.exec()
        self.PopulateTitles()
    
    def delete_title(self, row):
        # Implement your delete functionality here
        print(f"Deleting row {row}")
        # Example confirmation dialog:
        reply = QtWidgets.QMessageBox.question(
            self, 'Delete Title', 
            'Are you sure you want to delete this title?',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            # Delete logic here
            item = self.tableWidgetTitles.item(row, 0)
            if item:
                row_data = item.data(Qt.ItemDataRole.UserRole)
            result = app.DeleteTitle(DB, row_data[0])
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle('Deleting Title')
            if (result['success']):
                dlg.setText("Title Deleted Successfully!")
                dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                dlg.exec()
                self.PopulateTitles()
            else:
                dlg.setText("Title Deletion Failure!")
                dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()
        
    def edit_update(self, row):
        print(f"Editing row {row}")
        item = self.tableWidgetUpdate.item(row, 0)
        if item:
            row_data = item.data(Qt.ItemDataRole.UserRole)
        dlg = app.EditUpdateDialog(data=row_data[0])
        dlg.exec()
        self.PopulateUpdates()
    
    def delete_update(self, row):
        # Implement your delete functionality here
        print(f"Deleting row {row}")
        # Example confirmation dialog:
        reply = QtWidgets.QMessageBox.question(
            self, 'Delete Update', 
            'Are you sure you want to delete this update?',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            # Delete logic here
            item = self.tableWidgetUpdate.item(row, 0)
            if item:
                row_data = item.data(Qt.ItemDataRole.UserRole)
            result = app.DeleteUpdate(DB, row_data[0])
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle('Deleting Update')
            if (result['success']):
                dlg.setText("Update Deleted Successfully!")
                dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                dlg.exec()
                self.PopulateUpdates()
            else:
                dlg.setText("Update Deletion Failure!")
                dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

    def create_link_item(self, url, text):
        item = QtWidgets.QTableWidgetItem(text)
        item.setData(Qt.ItemDataRole.UserRole, url)  # Store URL
        item.setForeground(Qt.GlobalColor.blue)       # Blue text
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        return item

    def open_link(self, row, col):
        if col == 6:
            item = self.tableWidgetTitles.item(row, col)
            if item and (url := item.data(Qt.ItemDataRole.UserRole)):
                QDesktopServices.openUrl(QUrl(url))
                
    def filterTableTitle(self):
        search_text = self.lineEditSearchTitle.text().strip().lower()
        
        for row in range(self.tableWidgetTitles.rowCount()):
            row_found = False
            if not search_text:
                self.tableWidgetTitles.setRowHidden(row, False)
                for col in range(self.tableWidgetTitles.columnCount()):
                    item = self.tableWidgetTitles.item(row, col)
                    if item:
                        item.setBackground(QBrush())  # Reset to default
                        item.setForeground(QBrush())
                        if col == 6:
                            item.setForeground(QBrush(QColor('blue')))
                continue
            
            for col in range(self.tableWidgetTitles.columnCount()):
                item = self.tableWidgetTitles.item(row, col)
                
                if col == 6:
                            item.setForeground(QBrush(QColor('blue')))
                
                if col == 9:
                    continue
                
                if item and search_text in item.text().lower():
                    row_found = True
                    item.setBackground(QBrush(QColor(255, 255, 0)))
                    item.setForeground(QBrush(QColor('black')))
                    break
                else:
                    item.setForeground(QBrush())
                    item.setBackground(QBrush())
                    pass
            self.tableWidgetTitles.setRowHidden(row, not row_found)
            
    def filterTableUpdate(self):
        search_text = self.lineEditSearchUpdate.text().strip().lower()
        
        for row in range(self.tableWidgetUpdate.rowCount()):
            row_found = False
            if not search_text:
                self.tableWidgetUpdate.setRowHidden(row, False)
                for col in range(self.tableWidgetUpdate.columnCount()):
                    item = self.tableWidgetUpdate.item(row, col)
                    if item:
                        item.setBackground(QBrush())  # Reset to default
                        item.setForeground(QBrush())                        
                continue
            
            for col in range(self.tableWidgetUpdate.columnCount()):
                item = self.tableWidgetUpdate.item(row, col)
                                
                if col == 8:
                    continue
                
                if item and search_text in item.text().lower():
                    row_found = True
                    item.setBackground(QBrush(QColor(255, 255, 0)))
                    item.setForeground(QBrush(QColor('black')))
                    break
                else:
                    item.setForeground(QBrush())
                    item.setBackground(QBrush())
                    pass
            self.tableWidgetUpdate.setRowHidden(row, not row_found)