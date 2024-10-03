import sqlite3
import random
import json

# Database connection setup
conn = sqlite3.connect('bible.db')
cursor = conn.cursor()

# Load the explanation JSON
with open('static/horoscope-json/rating_explanation.json', encoding='utf-8') as json_file:
    rating_explanations = json.load(json_file)


def get_explanation_id(category, rating):
    """Retrieve an explanation ID from the JSON based on the category and rating."""
    explanations = rating_explanations.get(category, {}).get(str(rating), [])
    return random.choice(explanations)['id'] if explanations else None

# Assign image paths
image_paths = [f'horoscope-images/{i}.jpg' for i in range(1, 41)]

# Generate 1000 horoscope entries without any base message
horoscope_messages = []
for i in range(1000):  # Loop for 1000 iterations
    love_rating = random.randint(1, 5)
    career_rating = random.randint(1, 5)
    health_rating = random.randint(1, 5)
    wealth_rating = random.randint(1, 5)

    # Get explanation IDs from the JSON file based on the rating
    love_explanation_id = get_explanation_id('love', love_rating)
    career_explanation_id = get_explanation_id('career', career_rating)
    health_explanation_id = get_explanation_id('health', health_rating)
    wealth_explanation_id = get_explanation_id('wealth', wealth_rating)

    # Calculate overall rating as the average of the four ratings and convert to an integer
    overall_rating = int(round((love_rating + career_rating + health_rating + wealth_rating) / 4))

    # Get the overall explanation ID based on the overall rating
    overall_explanation_id = get_explanation_id('overall', overall_rating)

    horoscope_message = {
        'love_rating': love_rating,
        'career_rating': career_rating,
        'health_rating': health_rating,
        'wealth_rating': wealth_rating,
        'overall_rating': overall_rating,  # Overall rating as an integer
        'lucky_color': random.choice(['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Black', 'White']),
        'lucky_number': str(random.randint(1, 99)),
        'matching_sign': random.choice(['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                                          'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']),
        'image_path': random.choice(image_paths),
        'love_explanation_id': love_explanation_id,
        'career_explanation_id': career_explanation_id,
        'health_explanation_id': health_explanation_id,
        'wealth_explanation_id': wealth_explanation_id,
        'overall_explanation_id': overall_explanation_id  # Add the overall explanation ID
    }
    horoscope_messages.append(horoscope_message)

# Insert records into the database
for message in horoscope_messages:
    cursor.execute(f"""
        INSERT INTO generic_horoscope_messages 
        (message, love_rating, career_rating, health_rating, wealth_rating, overall_rating, 
        lucky_color, lucky_number, matching_sign, image_path, 
        love_explanation_id, career_explanation_id, health_explanation_id, wealth_explanation_id, overall_explanation_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, ("",  # Insert empty string for message
          message['love_rating'], message['career_rating'], 
          message['health_rating'], message['wealth_rating'], 
          message['overall_rating'], message['lucky_color'], 
          message['lucky_number'], message['matching_sign'], 
          message['image_path'], message['love_explanation_id'], 
          message['career_explanation_id'], message['health_explanation_id'], 
          message['wealth_explanation_id'], message['overall_explanation_id']))


# Commit the changes
conn.commit()

# Verify by selecting all records from the table
cursor.execute("SELECT * FROM generic_horoscope_messages;")
inserted_messages = cursor.fetchall()

# Print out the inserted records for debugging
print("Inserted records:")
for record in inserted_messages:
    print(record)

# Close the connection
conn.close()
