import sqlite3

def UpdateUpdate(dblocation, data):
    id = data['id']
    title_id = data['tid']
    name = data['name']    
    rel = data['rel']
    play = data['play']    
    update = data['update']
    comment = data['comment']
    
    with sqlite3.connect(dblocation) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            query = '''
            UPDATE
                updates
            SET
                title_id = ?, update_name = ?, released = ?, update_status = ?, playing_status = ?, comment =?
            WHERE 
                id = ?
            ;'''
            data = (title_id, name, rel, update, play, comment, id,)
            cursor.execute(query, data)
            connection.commit()
            return { 'success': True }
        except sqlite3.Error as e:
            print(e)
            return { 'success': False }
        