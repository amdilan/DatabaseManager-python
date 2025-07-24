import sqlite3

def GetTitleDetails(dblocation):
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        query = '''
        SELECT
            t.id,
            t.name,
            d1.developer,
            d2.developer,
            t.released,
            s.status,
            p.platform,
            t.source,
            t.link,
            a.status,
            t.comment,
            d1.alias,
            d2.alias
        FROM 
            titles t
        LEFT JOIN
            developers d1
        ON
            t.developer = d1.id
        LEFT JOIN
            developers d2
        ON
            t.developer2 = d2.id
        LEFT JOIN
            availability a
        ON
            t.availability = a.id
        LEFT JOIN
            platforms p
        ON
            t.platform = p.id
        LEFT JOIN
            title_status s
        ON t.status = s.id
        ;
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        return results