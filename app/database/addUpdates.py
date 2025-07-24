import sqlite3

def AddUpdates(dblocation, data):
    tid = data['id']
    name = data['name']
    rel = data['rel']
    update = data['update']
    play = data['play']
    comment = data['comment']
        
    with sqlite3.connect(dblocation) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            query = '''
            INSERT INTO updates
            (title_id, update_name, released, update_status, playing_status, comment)
            VALUES 
            (?, ?, ?, ?, ?, ?)
            ;'''
            data = (tid, name, rel, update, play, comment,)
            cursor.execute(query, data)
            connection.commit()
            return { 'success': True }
        except sqlite3.Error as e:
            print(e)
            return { 'success': False }