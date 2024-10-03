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

# cursor.execute("DROP TABLE IF EXISTS cached_verses")
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# tables = cursor.fetchall()
# print(tables)
# conn.commit()  # Save the changes
# conn.close()
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS cached_verses (
#         id INTEGER PRIMARY KEY AUTOINCREMENT, 
#         ip_address TEXT NOT NULL,
#         reference TEXT NOT NULL,
#         verse TEXT NOT NULL,
#         type TEXT NOT NULL,
#         image_path TEXT NOT NULL,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#         last_sent BOOLEAN DEFAULT 0,
#         UNIQUE(ip_address,verse)
#     )
# ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS generic_horoscope_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        message TEXT,
        love_rating INT NOT NULL CHECK (love_rating >= 1 AND love_rating <= 5),
        career_rating INT NOT NULL CHECK (career_rating >= 1 AND career_rating <= 5),
        health_rating INT NOT NULL CHECK (health_rating >= 1 AND health_rating <= 5),
        wealth_rating INT NOT NULL CHECK (wealth_rating >= 1 AND wealth_rating <= 5),
        overall_rating INT NOT NULL CHECK (overall_rating >= 1 AND overall_rating <= 5),
        lucky_color TEXT NOT NULL,
        lucky_number TEXT NOT NULL,
        matching_sign TEXT NOT NULL,
        image_path TEXT NOT NULL,
        love_explanation_id INTEGER,
        career_explanation_id INTEGER,
        health_explanation_id INTEGER,
        wealth_explanation_id INTEGER,
        overall_explanation_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_horoscope_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date DATE NOT NULL,
        sign TEXT NOT NULL,
        message_id INTEGER NOT NULL,
        lucky_color_rect_color TEXT NOT NULL,
        lucky_number_rect_color TEXT NOT NULL,
        matching_sign_rect_color TEXT NOT NULL,
        FOREIGN KEY (message_id) REFERENCES generic_horoscope_messages(id),
        UNIQUE (sign, date)
    )
''')

# Create the table for tracking IP addresses and access counts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS horoscope_ip_access_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT NOT NULL,
        access_count INTEGER NOT NULL DEFAULT 1,
        last_access DATE NOT NULL,
        UNIQUE (ip_address)
    )
''')




conn.commit()  # Save the changes
conn.close()