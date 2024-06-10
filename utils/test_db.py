import sqlite3
import random
import logging

DATABASE = "../bible.db"  # Adjust path if necessary

def get_random_bible_verse(version='niv'):
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Fetch a random verse for the specified version
        cursor.execute("SELECT * FROM verses WHERE language = ? ORDER BY RANDOM() LIMIT 1", (version,))
        result = cursor.fetchone()

        conn.close()

        if result:
            _, reference, verse_text, _, audio_data = result
            print(f"Retrieved verse ({version}): {reference} - {verse_text}")
            return verse_text, reference
        else:
            logging.warning(f"No verses found for version: {version}")
            return None, None

    except sqlite3.Error as e:
        logging.error(f"Error fetching Bible verse from database: {e}")
        return None, None

if __name__ == "__main__":
    # Test by fetching a few random verses
    for _ in range(5): 
        verse_text, reference = get_random_bible_verse()  # Default to 'niv'
        if verse_text and reference:
            print(f"Verse: {verse_text}\nReference: {reference}\n")
        else:
            print("No verse found.\n")
