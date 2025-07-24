import sqlite3

def GetUpdates(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = 'SELECT * FROM updates;'
        cursor.execute(query)
        updates = cursor.fetchall()
        return updates
    
def GetUpdatesId(dblocation, id):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        data = (id,)
        query = 'SELECT * FROM updates WHERE id = ?;'
        cursor.execute(query, data)
        updates = cursor.fetchall()
        return updates