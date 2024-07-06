import sqlite3

conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Drop the existing cached_verses table (if it exists)
cursor.execute("DROP TABLE IF EXISTS cached_verses")

# Remove the audio column from the verses table 
cursor.execute('ALTER TABLE verses DROP COLUMN audio')

# Now, create the two tables with the desired schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        reference TEXT NOT NULL,
        verse TEXT NOT NULL,
        language TEXT NOT NULL,  
        UNIQUE(reference, language)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cached_verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        ip_address TEXT NOT NULL,
        reference TEXT NOT NULL,
        verse TEXT NOT NULL,
        language TEXT NOT NULL,
        image_path TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_sent BOOLEAN DEFAULT 0,      
        UNIQUE(ip_address,verse)
    )
''')

conn.commit()  # Save the changes
conn.close()