import sqlite3

conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Create the table (only if it doesn't already exist)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS verses (
#         id INTEGER PRIMARY KEY AUTOINCREMENT, 
#         reference TEXT NOT NULL,
#         verse TEXT NOT NULL,
#         language TEXT NOT NULL,
#         audio BLOB,
#         UNIQUE(reference, language)
#     )
# ''')

cursor.execute("DROP TABLE IF EXISTS cached_verses")
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# tables = cursor.fetchall()
# print(tables)
# conn.commit()  # Save the changes
# conn.close()
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