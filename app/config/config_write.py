import os
import sys
import configparser
from PyQt6 import QtWidgets

CONFIG_FILE = "./data/config.ini"

def ConfigWrite():
    print("test write")
    
def WriteConfigTheme(theme):
    config = configparser.ConfigParser()
    config["Appearance"] = {"theme": theme}
    with open(CONFIG_FILE, "w") as f:
        config.write(f)    

def main():
    ConfigWrite()
    
if __name__ == "__main__":
    main()
    WriteConfigTheme("dark")