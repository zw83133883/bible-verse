import sqlite3
import random
from datetime import date

# Database connection setup
DATABASE = 'bible.db'

def insert_daily_horoscope_assignments():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # List of zodiac signs
    zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 
                    'Aquarius', 'Pisces']

    # Fetch all generic horoscope messages
    cursor.execute('SELECT id FROM generic_horoscope_messages')
    generic_messages = cursor.fetchall()

    if not generic_messages:
        print("No generic horoscope messages found.")
        return

    # Delete old assignments for today
    today = date.today().strftime('%m-%d-%Y')


    cursor.execute('DELETE FROM daily_horoscope_assignments WHERE date = ?', (today,))

    # Assign random messages to zodiac signs for today
    for sign in zodiac_signs:
        while True:
            message_id = random.choice(generic_messages)[0]  # Select a random message ID
            
            # Check if the message's matching sign is the same as the current zodiac sign
            cursor.execute('''
                SELECT matching_sign FROM generic_horoscope_messages WHERE id = ?
            ''', (message_id,))
            matching_sign = cursor.fetchone()
            
            if matching_sign is None or matching_sign[0] == sign:
                break  # If no matching sign or it matches, break the loop

        cursor.execute('''
            INSERT INTO daily_horoscope_assignments (date, sign, message_id)
            VALUES (?, ?, ?)
        ''', (today, sign, message_id))

    conn.commit()
    conn.close()

# Call the function to insert daily horoscope assignments
insert_daily_horoscope_assignments()
