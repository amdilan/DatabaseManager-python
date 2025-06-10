import os
import sys
import configparser
from PyQt6 import QtWidgets

CONFIG_FILE = "../../data/config.ini"

def ConfigRead():
    print("test read")

def ReadConfigTheme():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get("Appearance", "theme", fallback="light").lower()

def main():
    ConfigRead()
    
if __name__ == "__main__":
    main()
    print(ReadConfigTheme())