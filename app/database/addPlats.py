import sqlite3

def AddPlats(dblocation, data):
    name = data['name']
        
    with sqlite3.connect(dblocation) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            query = '''
            INSERT INTO platforms
            ( id, platform )
            VALUES 
            (NULL, ?)
            ;'''
            data = (name,)
            cursor.execute(query, data)
            connection.commit()
            return { 'success': True }
        except sqlite3.Error as e:
            # print(e)
            return { 'success': False }
        