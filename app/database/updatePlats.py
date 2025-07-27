import sqlite3

def updatePlats(dblocation, data):
    id = data['id']
    name = data['name']
        
    with sqlite3.connect(dblocation) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            query = '''
            UPDATE platforms
            SET platform = ?
            WHERE 
            id = ?
            ;'''
            data = (name, id,)
            cursor.execute(query, data)
            connection.commit()
            return { 'success': True }
        except sqlite3.Error as e:
            # print(e)
            return { 'success': False }
        