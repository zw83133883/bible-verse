import sqlite3

conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Create the table (only if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        reference TEXT NOT NULL,
        verse TEXT NOT NULL,
        type TEXT NOT NULL,
        UNIQUE(reference)
    )
''')

conn.commit()  # Save the changes
conn.close()