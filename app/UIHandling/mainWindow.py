from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QDesktopServices, QColor, QBrush

from ui.main_window import Ui_MainWindow
import app
from main import DB, CONFIG_FILE

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.proxy_modelTitles = QtCore.QSortFilterProxyModel()
        self.proxy_modelTitles.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_modelTitles.setFilterKeyColumn(-1)
        self.proxy_modelUpdates = QtCore.QSortFilterProxyModel()
        self.proxy_modelUpdates.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_modelUpdates.setFilterKeyColumn(-1)
        
        self.PopulateStats()
        self.PopulateTitles()
        self.PopulateUpdates()
        
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
        
    def __del__(self):
        self.search_timer.stop()
        self.search_timerUpdate.stop()
        del self.proxy_modelTitles
        del self.proxy_modelUpdates
                
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
        # print("...")
        dlg = app.NewTitleDialog()
        dlg.exec()
        self.PopulateTitles()
        
    def HandleNewUpdateClick(self):
        # print(".....")
        dlg = app.NewUpdateDialog()
        dlg.exec()
        self.PopulateUpdates()
    
    def HandleNewThemeChanged(self):
        # print(".")
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
        titles = app.GetTitleDetails(DB)

        self.modelTitles = TitlesTableModel(titles)
        self.proxy_modelTitles.setSourceModel(self.modelTitles)
        self.tableTitles.setSortingEnabled(False)
        self.tableTitles.setModel(self.proxy_modelTitles)
        
        try:
            self.proxy_modelTitles.layoutChanged.disconnect()
        except:
            pass
        
        self.tableTitles.setStyleSheet("""
            QTableView {
                gridline-color: #ccc;
            }
            QTableView::item {
                padding: 3px;
            }
        """)

        self.tableTitles.setSortingEnabled(True)
        self.proxy_modelTitles.layoutChanged.connect(self.AssignButtonsTitles)
        self.AssignButtonsTitles()
        self.tableTitles.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.tableTitles.setItemDelegateForColumn(6, HyperlinkDelegate(self.tableTitles))
        self.tableTitles.viewport().setMouseTracking(True)
        self.tableTitles.viewport().installEventFilter(self)
        self.tableTitles.setWordWrap(True)
        self.tableTitles.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.tableTitles.resizeColumnsToContents()
        self.tableTitles.resizeRowsToContents()
        # self.tableTitles.clicked.connect(self.open_link)
        
    def AssignButtonsTitles(self):
        # Clear existing buttons
        for row in range(self.proxy_modelTitles.rowCount()):
            self.tableTitles.setIndexWidget(
                self.proxy_modelTitles.index(row, self.proxy_modelTitles.columnCount()-1),
                None
        )
        
        # Add tool buttons for the last column
        for row in range(self.proxy_modelTitles.rowCount()):
            tool_button = QtWidgets.QToolButton()
            proxy_index = self.proxy_modelTitles.index(row, 0)
            persistent_index = QtCore.QPersistentModelIndex(proxy_index)
                        
            tool_button.setText("⋮")
            tool_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")
            
            menu = QtWidgets.QMenu()
            edit_action = menu.addAction("Edit")
            delete_action = menu.addAction("Delete")
            
            edit_action.triggered.connect(lambda _, r=persistent_index: self.edit_title(r))
            delete_action.triggered.connect(lambda _, r=persistent_index: self.delete_title(r))
            
            tool_button.setMenu(menu)
            tool_button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
            tool_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            
            self.tableTitles.setIndexWidget(
                self.proxy_modelTitles.index(row, self.proxy_modelTitles.columnCount()-1),
                tool_button
            )
        
    def PopulateUpdates(self):
        update = app.GetUpdateDetails(DB)
        
        self.modelUpdates = UpdatesTableModel(update)
        self.proxy_modelUpdates.setSourceModel(self.modelUpdates)
        self.tableTitles.setSortingEnabled(False)
        self.tableUpdates.setModel(self.proxy_modelUpdates)
        
        try:
            self.proxy_modelUpdates.layoutChanged.disconnect()
        except:
            pass
        
        self.tableUpdates.setStyleSheet("""
            QTableView {
                gridline-color: #ccc;
            }
            QTableView::item {
                padding: 3px;
            }
        """)
        
        self.tableUpdates.setSortingEnabled(True)
        self.proxy_modelUpdates.layoutChanged.connect(self.AssignButtonsUpdates)
        self.AssignButtonsUpdates()
        self.tableUpdates.setWordWrap(True)
        self.tableUpdates.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.tableUpdates.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.tableUpdates.resizeColumnsToContents()
        self.tableUpdates.resizeRowsToContents()
        
    def AssignButtonsUpdates(self):
        # Clear existing buttons
        for row in range(self.proxy_modelUpdates.rowCount()):
            self.tableUpdates.setIndexWidget(
                self.proxy_modelUpdates.index(row, self.proxy_modelUpdates.columnCount()-1),
                None
        )
            
        for row in range(self.proxy_modelUpdates.rowCount()):
            tool_button = QtWidgets.QToolButton()
            proxy_index = self.proxy_modelUpdates.index(row, 0)
            persistent_index = QtCore.QPersistentModelIndex(proxy_index)
            
            tool_button.setText("⋮")
            tool_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")
            
            menu = QtWidgets.QMenu()
            edit_action = menu.addAction("Edit")
            delete_action = menu.addAction("Delete")
            
            edit_action.triggered.connect(lambda _, r=persistent_index: self.edit_update(r))
            delete_action.triggered.connect(lambda _, r=persistent_index: self.delete_update(r))
            
            tool_button.setMenu(menu)
            tool_button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
            tool_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            
            self.tableUpdates.setIndexWidget(
                self.proxy_modelUpdates.index(row, self.proxy_modelUpdates.columnCount()-1),
                tool_button
            )
    
    def edit_title(self, row):
        # print(f"Editing row {row}")
        if not row.isValid():
            return
        # proxy_index = self.proxy_modelTitles.index(row, 0)
        # source_index = self.proxy_modelTitles.mapToSource(proxy_index)
        proxy_index = QtCore.QModelIndex(row)
        source_index = self.proxy_modelTitles.mapToSource(proxy_index)
        if not source_index.isValid():
            return
        row_data = self.modelTitles.data(source_index, QtCore.Qt.ItemDataRole.UserRole)
        if not row_data:
            return
        # print(f'title edit data: {row_data}')
        dlg = app.EditTitleDialog(data=row_data[0], parent=self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.PopulateTitles()
    
    def delete_title(self, row):
        # print(f"Deleting row {row}")
        if not row:
            return
        proxy_index = QtCore.QModelIndex(row)
        source_index = self.proxy_modelTitles.mapToSource(proxy_index)
        row_data = self.modelTitles.data(source_index, QtCore.Qt.ItemDataRole.UserRole)
        reply = QtWidgets.QMessageBox.question(
            self, 'Delete Title', 
            f"Are you sure you want to delete this title?\n{row_data[0]} — {row_data[1]}",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            # Delete logic here
            if not row_data:
                return
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
        # print(f"Editing row {row}")
        if not row:
            return
        proxy_index = QtCore.QModelIndex(row)
        source_index = self.proxy_modelUpdates.mapToSource(proxy_index)
        if not source_index.isValid():
            return
        row_data = self.modelUpdates.data(source_index, QtCore.Qt.ItemDataRole.UserRole)
        if not row_data:
            return
        # print(row_data)
        dlg = app.EditUpdateDialog(data=row_data[0])
        dlg.exec()
        self.PopulateUpdates()
    
    def delete_update(self, row):
        # print(f"Deleting row {row}")
        if not row:
            return
        proxy_index = QtCore.QModelIndex(row)
        source_index = self.proxy_modelUpdates.mapToSource(proxy_index)
        row_data = self.modelUpdates.data(source_index, QtCore.Qt.ItemDataRole.UserRole)
        reply = QtWidgets.QMessageBox.question(
            self, 'Delete Update', 
            f"Are you sure you want to delete this update?\nTitle: {row_data[1]} - {row_data[2]}\nUpdate: {row_data[0]} - {row_data[3]}",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            # Delete logic here
            if not row_data:
                return
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
        search_text = self.lineEditSearchTitle.text().strip()
        self.proxy_modelTitles.setFilterFixedString(search_text)
        self.AssignButtonsTitles()
            
    def filterTableUpdate(self):
        search_text = self.lineEditSearchUpdate.text().strip()
        self.proxy_modelUpdates.setFilterFixedString(search_text)
        self.AssignButtonsUpdates()
    
    def eventFilter(self, obj, event):
        if obj == self.tableTitles.viewport(): 
            if event.type() == QtCore.QEvent.Type.Leave:
                self.tableTitles.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        elif event.type() == QtCore.QEvent.Type.MouseMove:
            index = self.tableTitles.indexAt(event.pos())
            if index.column() == 6:  # URL column
                self.tableTitles.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            else:
                self.tableTitles.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        return super().eventFilter(obj, event)
                
class TitlesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self.headers = ["T. ID", "Name", "Devs", "Released", "Status", "Platform", "Web Link", "Availability", "Comment", ""]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.headers)

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        record = self._data[row]

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return record[0]
            elif col == 1:
                return record[1]
            elif col == 2:
                devs = []
                if record[2]:
                    devs.append(f"{record[2]} [aka] {record[11]}" if record[11] else record[2])
                if record[3]:
                    devs.append(f"{record[3]} [aka] {record[12]}" if record[12] else record[3])
                return "\n".join(devs)
            elif col == 3:
                return record[4]
            elif col == 4:
                return record[5]
            elif col == 5:
                return record[6]
            elif col == 6:
                return record[7]  # display text
            elif col == 7:
                return record[9]
            elif col == 8:
                return record[10]
            elif col == 9:
                return "⋮"
        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return record  # full row data for potential use
        return None

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return super().headerData(section, orientation, role)
    
    def sort(self, column: int, order: QtCore.Qt.SortOrder):
        self.layoutAboutToBeChanged.emit()
        
        def sort_key(row):
            # Customize based on column
            if column == 0:  # T. ID
                return int(row[0]) if row[0] else -1
            elif column == 1:  # Name
                return row[1].lower()
            elif column == 2:  # Devs
                devs = []
                if row[2]:
                    devs.append(f"{row[2]} [aka] {row[11]}" if row[11] else row[2])
                if row[3]:
                    devs.append(f"{row[3]} [aka] {row[12]}" if row[12] else row[3])
                return "\n".join(devs).lower()
            elif column == 3:  # Released
                return QtCore.QDate.fromString(row[4], "yyyy-MM-dd")
            elif column == 4:  # Status
                return row[5] or ""
            elif column == 5:  # Platform
                return row[6] or ""
            elif column == 6:  # Web Link Text
                return row[7] or ""
            elif column == 7:  # Availability
                return row[9] or ""
            elif column == 8:  # Comment
                return row[10] or ""
            elif column == 9:
                return
            else:
                return "" # skip action column
            
        self._data.sort(key=sort_key, reverse=(order == QtCore.Qt.SortOrder.DescendingOrder))
        self.layoutChanged.emit()

class UpdatesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self.headers = ["U. ID", "T. ID", "Title", "Version", "Released", "Update Status", "Play Status", "Comment", ""]
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.headers)
    
    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        record = self._data[row]

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return record[0] # UID
            elif col == 1:
                return record[1] # TID
            elif col == 2:
                return record[2] # TName
            elif col == 3:
                return record[3] # Update/Version
            elif col == 4:
                return record[4] # Rel
            elif col == 5:
                return record[5] # UpdateStatus
            elif col == 6:
                return record[6] # PlayStatus
            elif col == 7:
                return record[7] # Comment
            elif col == 8:
                return "⋮"
        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return record  # full row data for potential use
        return None
    
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        return super().headerData(section, orientation, role)
    
    def sort(self, column: int, order: QtCore.Qt.SortOrder):
        self.layoutAboutToBeChanged.emit()
        
        def sort_key(row):
            # Customize based on column
            if column == 0:  # U. ID
                return int(row[0]) if row[0] else -1
            elif column == 1:  # T. ID
                return int(row[0]) if row[0] else -1
            elif column == 2:  # TName
                return row[2] or ""
            elif column == 3:  # Update/Version
                return row[3] or ""
            elif column == 4:  # Rel
                return QtCore.QDate.fromString(row[4], "yyyy-MM-dd") or ""
            elif column == 5:  # UpdateStatus
                return row[5] or ""
            elif column == 6:  # PlayStatus
                return row[6] or ""
            elif column == 7:  # Comment
                return row[7] or ""
            else:
                return ""  # skip action column
            
        self._data.sort(key=sort_key, reverse=(order == QtCore.Qt.SortOrder.DescendingOrder))
        self.layoutChanged.emit()

import webbrowser
from urllib.parse import urlparse

class HyperlinkDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if index.column() == 6:
            text = index.data(QtCore.Qt.ItemDataRole.DisplayRole)
            painter.save()
            painter.setPen(QtGui.QPen(QtGui.QColor('blue')))
            font = option.font
            font.setUnderline(True)
            painter.setFont(font)
            rect = option.rect.adjusted(4, 0, -4, 0)  # Optional padding
            painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft, text)
            painter.restore()
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if index.column() == 6 and event.type() == QtCore.QEvent.Type.MouseButtonRelease:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                row_data = index.data(QtCore.Qt.ItemDataRole.UserRole)
                url = row_data[8]  # actual URL
                if url and HyperlinkDelegate.is_valid_url(url):
                    webbrowser.open(url)
                else:
                    QtWidgets.QMessageBox.warning(None, "Invalid Link", f"Invalid URL:\n{url}")
        return super().editorEvent(event, model, option, index)

    def helpEvent(self, event, view, option, index):
        if index.column() == 6:
            row_data = index.data(QtCore.Qt.ItemDataRole.UserRole)
            url = row_data[8]
            if url:
                QtWidgets.QToolTip.showText(event.globalPos(), url)
            view.viewport().setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            return True
        return super().helpEvent(event, view, option, index)

    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False