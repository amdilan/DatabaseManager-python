import sqlite3

def UpdateTitle(dblocation, data):
    id = data['id']
    title = data['title']
    dev = data['dev']
    dev2 = data['dev2']
    plat = data['plat']
    rel = data['rel']
    status = data['status']    
    src = data['src']
    link = data['link']
    comment = data['comment']
    # avail = data['avail']
    
    with sqlite3.connect(dblocation) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            query = '''
            UPDATE
                titles
            SET
                name = ?, developer = ?, developer2 = ?, platform = ?, released = ?, status = ?, source = ?, link = ?, comment =?
            WHERE 
                id = ?
            ;'''
            data = (title, dev, dev2, plat, rel, status, src, link, comment, id,)
            cursor.execute(query, data)
            connection.commit()
            return { 'success': True }
        except sqlite3.Error as e:
            # print(e)
            return { 'success': False }
        