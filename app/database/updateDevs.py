import sqlite3

def updateDevs(dblocation, data):
    id = data['id']
    name = data['name']
    alias = data['alias']
    link = data['link']
        
    with sqlite3.connect(dblocation) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            query = '''
            UPDATE developers
            SET developer = ?, alias = ?, link = ?
            WHERE 
            id = ?
            ;'''
            data = (name, alias, link, id)
            cursor.execute(query, data)
            connection.commit()
            return { 'success': True }
        except sqlite3.Error as e:
            print(e)
            return { 'success': False }
        