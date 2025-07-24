import os
import app

def IsExistDB(DB):
    if not(os.path.exists(DB)):
        app.InitializeDB(DB)
        