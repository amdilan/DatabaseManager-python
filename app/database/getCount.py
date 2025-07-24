import sqlite3

def GetCountTitleStatus(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = '''
        SELECT ts.status, COUNT(t.id) AS count
        FROM title_status ts
        LEFT JOIN titles t ON ts.id = t.status
        GROUP BY ts.id, ts.status
        ORDER BY ts.id;
        '''
        cursor.execute(query)
        stat = cursor.fetchall()
        print(stat)
        return stat
    
def GetCountTitles(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = '''          
        SELECT COUNT(t.id) AS count
        FROM titles t
        '''
        cursor.execute(query)
        stat = cursor.fetchall()
        print(stat)
        return stat
    
def GetCountUpdates(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = '''          
        SELECT COUNT(u.id) AS count
        FROM updates u
        '''
        cursor.execute(query)
        stat = cursor.fetchall()
        print(stat)
        return stat
    
def GetCountUpdateStatus(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = '''
        SELECT us.status, COUNT(u.id) AS count
        FROM update_status us
        LEFT JOIN updates u ON us.id = u.update_status
        GROUP BY us.id, us.status
        ORDER BY us.id;
        '''
        cursor.execute(query)
        stat = cursor.fetchall()
        print(stat)
        return stat
    
def GetCountTitleAvail(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = '''
        SELECT a.status, COUNT(t.id) AS count
        FROM availability a
        LEFT JOIN titles t ON a.id = t.availability
        GROUP BY a.id, a.status
        ORDER BY a.id;
        '''
        cursor.execute(query)
        stat = cursor.fetchall()
        print(stat)
        return stat
    
def GetCountUpdatePlay(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = '''
        SELECT ps.status, COUNT(u.id) AS count
        FROM playing_status ps
        LEFT JOIN updates u ON ps.id = u.playing_status
        GROUP BY ps.id, ps.status
        ORDER BY ps.id;
        '''
        cursor.execute(query)
        stat = cursor.fetchall()
        print(stat)
        return stat