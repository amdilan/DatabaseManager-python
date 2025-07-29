import sqlite3

def InitializeDB(dblocation):
    location = dblocation
    #connection = sqlite3.connect(location)
    with sqlite3.connect(dblocation) as connection:
        cursor = connection.cursor()
        
        query = {}
        
        query[0] = 'PRAGMA foreign_keys = ON;'
        
        query[1] = '''
        CREATE TABLE IF NOT EXISTS `developers` (
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `developer` TEXT NOT NULL UNIQUE,
            `alias` TEXT,
            `link` TEXT
        );
        '''
        
        query[2] = '''
        CREATE TABLE IF NOT EXISTS `availability` (
            `id` INTEGER NOT NULL PRIMARY KEY,
            `status` TEXT NOT NULL
        );
        '''
        
        query[3] = '''
        CREATE TABLE IF NOT EXISTS `title_status` (
            `id` INTEGER NOT NULL PRIMARY KEY,
            `status` TEXT NOT NULL
        );
        '''
        
        query[4] = '''
        CREATE TABLE IF NOT EXISTS `platforms` (
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `platform` TEXT NOT NULL UNIQUE
        );
        '''
        
        query[5] = '''
        CREATE TABLE IF NOT EXISTS `titles` (
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `name` TEXT NOT NULL,
            `released` TEXT NOT NULL,
            `source` TEXT NOT NULL,
            `link` TEXT NOT NULL,
            `comment` TEXT,
            `developer` INTEGER NOT NULL,
            `developer2` INTEGER,
            `status` INTEGER NOT NULL,
            `availability` INTEGER,
            `platform` INTEGER NOT NULL,
            FOREIGN KEY (`developer`) REFERENCES `developers`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
            FOREIGN KEY (`developer2`) REFERENCES `developers`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
            FOREIGN KEY (`platform`) REFERENCES `platforms`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
            FOREIGN KEY (`status`) REFERENCES `title_status`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
            FOREIGN KEY (`availability`) REFERENCES `availability`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT
        );
        '''
        
        query[6] = '''
        CREATE TABLE IF NOT EXISTS `update_status` (
            `id` INTEGER NOT NULL PRIMARY KEY,
            `status` TEXT NOT NULL
        );
        '''
        
        query[7] = '''
        CREATE TABLE IF NOT EXISTS `playing_status` (
            `id` INTEGER NOT NULL PRIMARY KEY,
            `status` TEXT NOT NULL
        );
        '''
        
        query[8] = '''
        CREATE TABLE IF NOT EXISTS `updates` (
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `title_id` INTEGER NOT NULL,
            `update_name` TEXT NOT NULL,
            `released` TEXT NOT NULL,
            `update_status` INTEGER NOT NULL,
            `playing_status` INTEGER NOT NULL,
            `comment` TEXT,
            FOREIGN KEY (`title_id`) REFERENCES `titles`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
            FOREIGN KEY (`update_status`) REFERENCES `update_status`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT,
            FOREIGN KEY (`playing_status`) REFERENCES `playing_status`(`id`) ON UPDATE CASCADE ON DELETE RESTRICT
        );
        '''
        
        query[9] = '''
        INSERT OR IGNORE INTO `playing_status` ( `id` , `status` )
        VALUES 
        ('0' , 'Not Played'),
        ('1' , 'Playing'),
        ('2' , 'Played');
        '''
        
        query[10] = '''
        INSERT OR IGNORE INTO `update_status` ( `id` , `status` )
        VALUES 
        ('0' , 'Not Available'),
        ('1' , 'Available'),
        ('2' , 'To Download'),
        ('3' , 'Download Skipped');
        '''
        
        query[11] = '''
        INSERT OR IGNORE INTO `availability` ( `id` , `status` )
        VALUES 
        ('0' , 'Not Available'),
        ('1' , 'Available');
        '''
        
        query[12] = '''
        INSERT OR IGNORE INTO `title_status` ( `id` , `status` )
        VALUES 
        ('0' , 'OnGoing'),
        ('1' , 'Completed'),
        ('2' , 'OnHold'),
        ('3' , 'Abandoned');
        '''
        
        query[13] = '''
        -- 1. Trigger for new updates with status 1
        CREATE TRIGGER update_title_availability_insert
        AFTER INSERT ON updates
        FOR EACH ROW
        WHEN NEW.update_status = 1
        BEGIN
            UPDATE titles
            SET availability = 1
            WHERE id = NEW.title_id;
        END;
        '''
        
        query[14] = '''
        -- 2. Trigger when updates are changed to status 1
        CREATE TRIGGER update_title_availability_update
        AFTER UPDATE OF update_status ON updates
        FOR EACH ROW
        WHEN NEW.update_status = 1
        BEGIN
            UPDATE titles
            SET availability = 1
            WHERE id = NEW.title_id;
        END;
        '''
        
        query[15] = '''
        -- 3. Trigger when updates with status 1 are deleted
        CREATE TRIGGER update_availability_after_delete
        AFTER DELETE ON updates
        FOR EACH ROW
        WHEN OLD.update_status = 1
        BEGIN
            -- Set availability to 0 if no more updates with status 1 exist
            UPDATE titles
            SET availability = CASE 
                WHEN (SELECT COUNT(*) FROM updates WHERE title_id = OLD.title_id AND update_status = 1) = 0 THEN 0
                ELSE 1
            END
            WHERE id = OLD.title_id;
        END;
        '''
        
        query[16] = '''
        -- 4. Trigger when updates are changed from status 1 to something else
        CREATE TRIGGER update_availability_status_change
        AFTER UPDATE OF update_status ON updates
        FOR EACH ROW
        WHEN OLD.update_status = 1 AND NEW.update_status != 1
        BEGIN
            -- Set availability to 0 if no more updates with status 1 exist
            UPDATE titles
            SET availability = CASE 
                WHEN (SELECT COUNT(*) FROM updates WHERE title_id = NEW.title_id AND update_status = 1) = 0 THEN 0
                ELSE 1
            END
            WHERE id = NEW.title_id;
        END;
        '''
        
        query[17] = '''
        -- 5. Trigger for new updates with status not 1
        CREATE TRIGGER update_title_availability_not_avail_insert
        AFTER INSERT ON updates
        FOR EACH ROW
        WHEN NEW.update_status != 1
        BEGIN
            UPDATE titles
            SET availability = CASE
                WHEN (SELECT COUNT(*) FROM updates WHERE title_id = NEW.title_id AND update_status = 1) = 0 THEN 0
                ELSE 1
            END
            WHERE id = NEW.title_id;
        END;
        '''
        
        for x in query:
            cursor.execute(query[x])
            # print(query[x])
        connection.commit()
        # print("Tables created successfully!")
        
    
def name(args):
 pass

if __name__ == "__main__":
    InitializeDB()