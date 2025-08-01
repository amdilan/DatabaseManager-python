import sqlite3

def DeletePlats(dblocation, id):
    with sqlite3.connect(dblocation) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            query = '''
            DELETE FROM 
                platforms
            WHERE 
                id = ?
            ;'''
            # data = (f"'{id}'")
            data = (id,)
            # print(data)
            cursor.execute(query, data)
            connection.commit()
            return { 'success': True }
        except sqlite3.Error as e:
            # print(e)
            return { 'success': False }
        