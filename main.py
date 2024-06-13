from flask import Flask,jsonify, render_template,request,g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import logging
import os
import textwrap
import random
import pyttsx3
import base64
import sqlite3

logging.basicConfig(level=logging.INFO)
# Disable logging for specific libraries
logging.getLogger('comtypes').setLevel(logging.ERROR)
logging.getLogger('pyttsx3').setLevel(logging.ERROR)
logging.getLogger("gtts").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)
DATABASE = "bible.db"  # Replace with your database name


app = Flask(__name__, static_folder='static', template_folder='templates')

# Add this teardown function to close the database connection after each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

engine = pyttsx3.init()
TOP_VERSES_FILE = os.path.join(os.path.dirname(__file__),"top_verses.txt")


# Initialize the rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per minute"]  # Adjust the rate limit as needed
)
# Custom error message for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "You have exceeded the request limit. Please try again later."
    }), 429


english_font_file = os.path.join(os.path.dirname(__file__), 'font', "font.ttf")
chinese_font_file = os.path.join(os.path.dirname(__file__), 'font', "chinese.ttf")

# Load verses into memory once
def load_verses(file_path):
    try:
        with open(file_path, 'r') as file:
            verses = [line.strip() for line in file if line.strip()]
        return verses
    except Exception as e:
        logging.error(f"Error loading verses: {e}")
        return []

# Load the verses once at the start
VERSUS = load_verses(TOP_VERSES_FILE)

# def get_random_bible_verse(version='niv'):
#     if not VERSUS:
#         logging.warning("No verses available.")  # Log a warning instead of returning a tuple
#         return None, None  # Return None for both verse and reference if no verses

#     random_verse = random.choice(VERSUS)  
#     # Split the book from the chapter/verse, accounting for multi-word book names with numbers
#     words = random_verse.split(" ")
#     if words[0].isdigit():
#         book = " ".join(words[:2]) 
#         reference = words[2]      
#     else:
#         book = words[0]
#         reference = words[1]

#     url = f"http://ibibles.net/quote.php?{version}-{book.replace(' ', '')}/{reference}"
#     print(f"Fetching verse from URL: {url}")  # Print the URL
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         timestamp_element = soup.find('small')

#         if timestamp_element:  # Check if timestamp element is found
#             verse_text = timestamp_element.next_sibling.strip()
#             verse_text = verse_text.split(" (")[0]  # Remove reference
#             return verse_text, random_verse  # Return the verse text and reference
#         else:
#             print(f"Fetching verse from URL: {url}")
#             logging.error("Timestamp element not found in HTML response.")  # Log the error
#     else:
#         logging.error(f"Error fetching Bible verse: {response.status_code}")  # Log the error

#     return None, None  # Return None if verse retrieval or parsing fails
# Function to get a random Bible verse from the database

def get_random_bible_verse(version='niv'):
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get the total number of verses for the given version
        cursor.execute("SELECT COUNT(*) FROM verses WHERE language = ?", (version,))
        total_verses = cursor.fetchone()[0]

        if total_verses == 0:
            logging.warning(f"No verses found for version: {version}")
            return None, None

        # Generate a random index within the range of available verses
        random_index = random.randint(0, total_verses - 1)
        
        # Fetch the verse at the random index
        cursor.execute("SELECT reference, verse FROM verses WHERE language = ? LIMIT 1 OFFSET ?", (version, random_index))
        verse_data = cursor.fetchone()

        conn.close()

        if verse_data:
            print(verse_data)
            reference, verse_text = verse_data
            return verse_text, reference

    except sqlite3.Error as e:
        logging.error(f"Error fetching Bible verse from database: {e}")
        return None, None


def get_random_scenic_image():
    try:
        image_directory = os.path.join('static', 'images')
        image_file = random.choice(os.listdir(image_directory))
        image_path = os.path.join('images', image_file).replace("\\", "/")
        return image_path
    except Exception as e:
        logging.error(f"Error fetching scenic image: {e}")
        return None

@app.route('/static/styles.css')
def styles():
    return app.send_static_file('styles.css')


# Flask route
@app.route('/random_verse', methods=['GET'])
def random_verse():
    try:
        # Get the requested version or default to 'niv'
        version = request.args.get('version', 'niv')  
        if version not in ['niv', 'cus']:  # Validate the version
            return "Invalid version. Please use 'niv' or 'cus'.", 400
        bible_verse, reference = get_random_bible_verse(version)
        image_path = get_random_scenic_image()

        return render_template('index.html', verse=bible_verse, reference=reference, image_path=image_path)
    except Exception as e:
        logging.error(f"Error in /random_verse endpoint: {e}")
        return "Internal server error.", 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)