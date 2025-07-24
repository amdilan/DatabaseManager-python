from PyQt6 import QtWidgets
import app
import sys

CONFIG_FILE = app.ResourcePath("data\\config.ini", "ext")
DB = app.ResourcePath("data\\PyDMdatabase.db", "ext")

class main():
    app.CheckPath(app.ResourcePath("data", "ext"))
    app.IsExistDB(DB)
    
if __name__ == "__main__":
    App = QtWidgets.QApplication(app.LoadTheme(CONFIG_FILE))
    window = app.MainWindow()
    window.show()
    window.CheckDarkTheme(CONFIG_FILE)
    main()
    sys.exit(App.exec())