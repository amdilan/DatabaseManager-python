import sqlite3

def GetTitles(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = 'SELECT * FROM titles;'
        cursor.execute(query)
        titles = cursor.fetchall()
        return titles
    
def GetTitlesId(dblocation, id):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        data = (id,)
        query = 'SELECT * FROM titles WHERE id = ?;'
        cursor.execute(query, data)
        titles = cursor.fetchall()
        return titles
    
def GetTitlesName(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = 'SELECT id, name FROM titles;'
        cursor.execute(query)
        titles = cursor.fetchall()
        return titles