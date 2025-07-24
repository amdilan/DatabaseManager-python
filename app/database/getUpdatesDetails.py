import sqlite3

def GetUpdateDetails(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = '''
        SELECT
            u.id,
            u.title_id,
            t.name AS title,
            u.update_name,
            u.released,
            us.status AS update_status,
            ps.status AS playing_status,
            u.comment
        FROM 
            updates u
        LEFT JOIN
            titles t
        ON
            u.title_id = t.id
        LEFT JOIN
            update_status us
        ON
            u.update_status = us.id
        LEFT JOIN
            playing_status ps
        ON
            u.playing_status = ps.id
        ;
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        return results