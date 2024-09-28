import sqlite3
import random
from datetime import date, timedelta

# Database connection setup
DATABASE = 'bible.db'

def get_random_light_color():
    """Generate a random light color."""
    return f'rgba({random.randint(150, 255)}, {random.randint(150, 255)}, {random.randint(150, 255)}, 0.8)'

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

    # Compute the dates for yesterday, today, and tomorrow in 'mm/dd/yyyy' format
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Format the dates as 'mm/dd/yyyy'
    formatted_today = today.strftime('%m/%d/%Y')
    formatted_yesterday = yesterday.strftime('%m/%d/%Y')
    formatted_tomorrow = tomorrow.strftime('%m/%d/%Y')

    # Delete old assignments for yesterday, today, and tomorrow
    cursor.execute('DELETE FROM daily_horoscope_assignments WHERE date IN (?, ?, ?)', 
                   (formatted_yesterday, formatted_today, formatted_tomorrow))

    # Track message_ids used for yesterday, today, and tomorrow to avoid duplicates
    used_message_ids = set()

    # Function to insert assignments for a specific date
    def assign_horoscopes_for_date(date_str):
        for sign in zodiac_signs:
            while True:
                message_id = random.choice(generic_messages)[0]  # Select a random message ID
                
                # Ensure that the message is unique across yesterday, today, and tomorrow
                if message_id not in used_message_ids:
                    used_message_ids.add(message_id)
                    
                    # Generate random light colors for the lucky fields
                    lucky_color_rect_color = get_random_light_color()
                    lucky_number_rect_color = get_random_light_color()
                    matching_sign_rect_color = get_random_light_color()

                    # Insert the data into the daily_horoscope_assignments table
                    cursor.execute('''
                        INSERT INTO daily_horoscope_assignments (date, sign, message_id, lucky_color_rect_color, lucky_number_rect_color, matching_sign_rect_color)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (date_str, sign, message_id, lucky_color_rect_color, lucky_number_rect_color, matching_sign_rect_color))
                    
                    break

    # Assign horoscopes for yesterday, today, and tomorrow
    assign_horoscopes_for_date(formatted_yesterday)
    assign_horoscopes_for_date(formatted_today)
    assign_horoscopes_for_date(formatted_tomorrow)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to insert daily horoscope assignments
insert_daily_horoscope_assignments()
