import os

def CheckPath(path):
    """ This will check if the path exists, if not creates. """
    os.makedirs(path, exist_ok=True)