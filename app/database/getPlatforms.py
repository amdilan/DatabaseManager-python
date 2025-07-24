import sqlite3

def GetPlatforms(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = 'SELECT * FROM platforms;'
        cursor.execute(query)
        platforms = cursor.fetchall()
        return platforms
    
def GetPlatformsOrdered(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = 'SELECT * FROM platforms ORDER BY platform ASC;'
        cursor.execute(query)
        platforms = cursor.fetchall()
        return platforms