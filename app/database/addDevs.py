import sqlite3

def AddDevs(dblocation, data):
    name = data['name']
    alias = data['alias']
    link = data['link']
        
    with sqlite3.connect(dblocation) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            query = '''
            INSERT INTO developers
            ( id, developer, alias, link )
            VALUES 
            (NULL, ?, ?, ?)
            ;'''
            data = (name, alias, link)
            cursor.execute(query, data)
            connection.commit()
            return { 'success': True }
        except sqlite3.Error as e:
            print(e)
            return { 'success': False }
        