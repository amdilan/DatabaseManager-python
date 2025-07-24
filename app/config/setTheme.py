from .config_read import ReadConfigTheme
from .config_write import WriteConfigTheme
import sys

def LoadTheme(CONFIG_FILE):
    theme = ReadConfigTheme(CONFIG_FILE)
    # print(theme)
    match theme:
        case "light":
            # print("L: ", theme)
            return sys.argv + ['-platform', 'windows:darkmode=1']
        case "dark":
            # print("D: ", theme)
            return sys.argv + ['-platform', 'windows:darkmode=2']
    # if (theme == 'light'):
    #     return sys.argv + ['-platform', 'windows:darkmode=1']
    # elif (theme == 'dark'):
    #     return sys.argv + ['-platform', 'windows:darkmode=0']
    
def IsDarkTheme(CONFIG_FILE):
    theme = ReadConfigTheme(CONFIG_FILE)
    match theme:
        case "light":
            # print("L: ", theme)
            return False
        case "dark":
            # print("D: ", theme)
            return True
    