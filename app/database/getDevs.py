import sqlite3

def GetDevs(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = 'SELECT * FROM developers;'
        cursor.execute(query)
        devs = cursor.fetchall()
        print(devs)
        return devs
    
def GetDevsOrdered(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = 'SELECT * FROM developers ORDER BY developer ASC;'
        cursor.execute(query)
        devs = cursor.fetchall()
        print(devs)
        return devs