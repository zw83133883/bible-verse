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
    default_limits=["10 per minute"]  # Adjust the rate limit as needed
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
        cursor.execute("SELECT * FROM verses WHERE language = ? LIMIT 1 OFFSET ?", (version, random_index))
        verse_data = cursor.fetchone()

        conn.close()

        if verse_data:
            _, reference, verse_text, _, audio_data = verse_data 
            return verse_text, reference, audio_data

    except sqlite3.Error as e:
        logging.error(f"Error fetching Bible verse from database: {e}")
        return None, None


def get_random_scenic_image():
    try:
        # Get the current directory
        current_directory = os.getcwd()
        # Path to the images folder
        images_folder = os.path.join(current_directory, 'images')
        # List all files in the 'images' directory
        image_files = os.listdir(images_folder)
        # Select a random image file
        image_file = random.choice(image_files)
        # Open the selected image file
        image = Image.open(os.path.join(images_folder, image_file))
        # Resize the image to 1080x1920
        resized_image = image.resize((1080, 1920))
        # Save the resized image to a BytesIO object
        resized_bytes = BytesIO()
        resized_image.save(resized_bytes, format='JPEG')
        resized_bytes.seek(0)
        return resized_bytes
    except Exception as e:
        logging.error(f"Error fetching scenic image: {e}")
        return None
    
def get_logo(logo_type, x, y):
    try:
        current_directory = os.getcwd()
        logo_folder = os.path.join(current_directory, 'logo')
        logo_path = os.path.join(logo_folder, f'{logo_type}.png')
        # Open the logo image file
        with open(logo_path, 'rb') as logo_file:
            logo_image = Image.open(logo_file).convert("RGBA")  # Ensure the image is in RGBA mode for transparency
        # Resize the logo image to the default size
        default_logo_size = (512, 512)  # Update with your default logo size
        resized_logo_image = logo_image.resize(default_logo_size)
        # Save the resized logo image to a BytesIO object
        resized_logo_bytes = BytesIO()
        resized_logo_image.save(resized_logo_bytes, format='PNG')  # Use the appropriate format for your logo
        resized_logo_bytes.seek(0)
        return resized_logo_bytes
    except Exception as e:
        logging.error(f"Error fetching logo image: {e}")
        return None


def overlay_text_on_image(version,logo_bytes, image_bytes, verse, reference, screen_width, screen_height):
        # Define a dictionary to map versions to font files
    font_map = {
        'niv': english_font_file,  # Replace with the actual path to your NIV font
        'cus':chinese_font_file
    }
    try:
        # Open the image
        image = Image.open(image_bytes).convert("RGBA")

        # Check if the image is smaller than the screen dimensions
        if image.width < screen_width or image.height < screen_height:
            # Create a new blank image with the screen dimensions
            new_image = Image.new("RGBA", (screen_width, screen_height), (255, 255, 255, 255))
            # Paste the smaller image onto the new image, centered
            offset_x = (screen_width - image.width) // 2
            offset_y = (screen_height - image.height) // 2
            new_image.paste(image, (offset_x, offset_y))
            image = new_image

        # Create a text overlay
        txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)

        # Remove "(web)" from the reference
        reference = reference.replace('(web)', '')
        font_file = font_map.get(version.lower(),english_font_file)
        # Font settings
        font_size = 60
        font = ImageFont.truetype(font_file, font_size)
        line_spacing = 10  # Adjust for desired spacing between lines
        shadow_offset = 2

        # Dynamically wrap the reference text if it's too long
        wrapped_reference = textwrap.fill(reference, width=35)
        ref_lines = wrapped_reference.splitlines()

        # Dynamically wrap the verse text
        wrapped_verse = textwrap.fill(verse, width=35)
        verse_lines = wrapped_verse.splitlines()



        # Calculate text dimensions
        if ref_lines:  # Check if ref_lines is not empty
            ref_line_height = max([d.textbbox((0, 0), line, font=font)[3] for line in ref_lines])
        else:
            ref_line_height = 0  # Or set a default value if needed

        if verse_lines:  # Check if verse_lines is not empty
            verse_line_height = max([d.textbbox((0, 0), line, font=font)[3] for line in verse_lines])
        else:
            verse_line_height = 0  # Or set a default value if needed


        ref_height = (ref_line_height + line_spacing) * len(ref_lines) - line_spacing
        verse_height = (verse_line_height + line_spacing) * len(verse_lines) - line_spacing

        total_text_height = ref_height + verse_height + 20

        # Determine text placement for centering
        y = (screen_height - total_text_height) // 2

        # Draw reference text with drop shadow
        for line in ref_lines:
            ref_x = (screen_width - d.textbbox((0, 0), line, font=font)[2]) // 2
            d.text((ref_x + shadow_offset, y + shadow_offset), line, font=font, fill=(0, 0, 0, 150))
            d.text((ref_x, y), line, font=font, fill=(255, 255, 255, 255))
            y += ref_line_height + line_spacing

        y += 20  # Additional spacing between reference and verse

        for line in verse_lines:
            verse_x = (screen_width - d.textbbox((0, 0), line, font=font)[2]) // 2
            d.text((verse_x + shadow_offset, y + shadow_offset), line, font=font, fill=(0, 0, 0, 150))
            d.text((verse_x, y), line, font=font, fill=(255, 255, 255, 255))
            y += verse_line_height + line_spacing

        # audio = Image.open(audio_bytes).convert("RGBA")
        # # Resize the logo to fit the image width
        # audio_width = screen_width //6
        # audio_height = int((audio_width / audio.width) * audio.height)
        # audio = audio.resize((audio_width, audio_height))

        # audio_x = screen_width - audio.width - 60  # 20 pixels from the right edge
        # audio_y = screen_height - audio.height - 360  # 20 pixels from the bottom edge
        # image.paste(audio, (audio_x, audio_y), audio)


        # Open the audio image
        logo = Image.open(logo_bytes).convert("RGBA")
        # Resize the logo to fit the image width
        logo_width = screen_width // 10
        logo_height = int((logo_width / logo.width) * logo.height)
        logo = logo.resize((logo_width, logo_height))

        # Calculate logo position at the bottom, centered
        logo_x = (screen_width - logo.width) // 2
        logo_y = screen_height - logo.height - 40

        # Paste the logo onto the image
        image.paste(logo, (logo_x, logo_y), logo)

        combined = Image.alpha_composite(image, txt)

        combined_bytes = BytesIO()
        combined.save(combined_bytes, format='PNG')
        combined_bytes.seek(0)
        return combined_bytes
    except Exception as e:
        logging.error(f"Error overlaying text on image: {e}")
        return None

# def get_font_size(text, language, max_size=60, min_size=20):
#     base_size = max_size
#     if language == "cus":  # or any other Chinese language code
#         base_size = 40  # Smaller base size for Chinese

#     length = len(text)
#     font_size = base_size - (length // 10)  # Adjust divisor as needed
#     return max(font_size, min_size)  


# Flask route
@app.route('/random_verse', methods=['GET'])
def random_verse():
    try:
        # Get the requested version or default to 'niv'
        version = request.args.get('version', 'niv')  
        if version not in ['niv', 'cus']:  # Validate the version
            return "Invalid version. Please use 'niv' or 'cus'.", 400
        bible_verse, reference, audio_data = get_random_bible_verse(version)
        image_bytes = get_random_scenic_image()

        logo_bytes = get_logo('logo',512,512)
        # audio_logo_bytes = get_logo('audio',980,862)
        if image_bytes is None:
            return "Could not fetch scenic image at this time.", 500
            # Select a male voice with an accent
        # for voice in engine.getProperty('voices'):
        #     if "David" in voice.name:  # Or any other clearly male voice name
        #         engine.setProperty('voice', voice.id)
        #         break
         # Generate TTS audio
        # language_code = "en" if version == "niv" else "zh-CN" 
        # tts = gTTS(bible_verse, lang=language_code)
        # audio_bytes_io = BytesIO()
        # tts.write_to_fp(audio_bytes_io)
        # audio_bytes_io.seek(0)

        combined_image_bytes = overlay_text_on_image(version,logo_bytes,image_bytes, bible_verse, reference,1080,1920)
        if combined_image_bytes is None:
            return "Error processing image.", 500    

        # Convert audio bytes to base64 string
        # audio_data_base64 = base64.b64encode(audio_bytes_io.getvalue()).decode('utf-8')
               # Insert verse into the database
        # insert_verse(reference, bible_verse, 'niv', audio_data_base64)
        return render_template('index.html', image_data=base64.b64encode(combined_image_bytes.getvalue()).decode(),audio_data=audio_data)
    except Exception as e:
        logging.error(f"Error in /random_verse endpoint: {e}")
        return "Internal server error.", 500
    
# Helper function to set a male voice (extracted for clarity)
def set_male_voice(engine):
    for voice in engine.getProperty('voices'):
        if voice.gender == 'Male':
            engine.setProperty('voice', voice.id)
            return  # Exit the loop after setting the first male voice


def insert_verse(reference, verse, language, audio_data):
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR IGNORE INTO verses (reference, verse, language, audio)
            VALUES (?, ?, ?, ?)
        ''', (reference, verse, language, audio_data))

        conn.commit()
        if cursor.rowcount > 0:  # Check if a row was actually inserted
            last_row_id = cursor.lastrowid  # Get the ID of the inserted row
            logging.info(f"Successfully inserted verse ID {last_row_id}: {reference} ({language})")
        else:
            logging.info(f"Verse already exists: {reference} ({language})")

    except sqlite3.Error as e:
        logging.error(f"Error inserting verse into database: {e}")
        conn.rollback()  # Rollback the transaction on error
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=False)
