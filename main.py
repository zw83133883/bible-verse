from flask import Flask,jsonify, render_template,request,g,redirect,url_for,abort,session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_apscheduler import APScheduler
import logging
import os
import random
import sqlite3
import uuid
from werkzeug.middleware.proxy_fix import ProxyFix
import tzlocal
import time
from datetime import date, timedelta, datetime
import uuid
import requests

logging.basicConfig(level=logging.INFO)
# Disable logging for specific libraries
logging.getLogger('comtypes').setLevel(logging.ERROR)
logging.getLogger('pyttsx3').setLevel(logging.ERROR)
logging.getLogger("gtts").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)
uuid_expiration_time = timedelta(minutes=10)
DATABASE = "bible.db"


app = Flask(__name__, static_folder='static', template_folder='templates')
cache = Cache(app, config={'CACHE_TYPE': 'simple'}) 
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# app.secret_key = os.getenv('SECRET_KEY', 'for dev')
app.secret_key = 'c4738e82d8075e896fbb3f5d3d7c7c3fa9fba9dbd0eafc9c'
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
# Add this teardown function to close the database connection after each request

# Initialize the rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per hour"]  # Adjust the rate limit as needed
)

import sqlite3
import random
import logging
from datetime import date, timedelta

surah_verse_counts = {
    1: 7,    # Surah Al-Fatiha
    2: 286,  # Surah Al-Baqarah
    3: 200,  # Surah Aal-E-Imran
    4: 176,  # Surah An-Nisa
    5: 120,  # Surah Al-Ma'idah
    6: 165,  # Surah Al-An'am
    7: 206,  # Surah Al-A'raf
    8: 75,   # Surah Al-Anfal
    9: 129,  # Surah At-Tawbah
    10: 109, # Surah Yunus
    11: 123, # Surah Hud
    12: 111, # Surah Yusuf
    13: 43,  # Surah Ar-Ra'd
    14: 52,  # Surah Ibrahim
    15: 99,  # Surah Al-Hijr
    16: 128, # Surah An-Nahl
    17: 111, # Surah Al-Isra
    18: 110, # Surah Al-Kahf
    19: 98,  # Surah Maryam
    20: 135, # Surah Ta-Ha
    21: 112, # Surah Al-Anbiya
    22: 78,  # Surah Al-Hajj
    23: 118, # Surah Al-Mu'minun
    24: 64,  # Surah An-Nur
    25: 77,  # Surah Al-Furqan
    26: 227, # Surah Ash-Shu'ara
    27: 93,  # Surah An-Naml
    28: 88,  # Surah Al-Qasas
    29: 69,  # Surah Al-Ankabut
    30: 60,  # Surah Ar-Rum
    31: 34,  # Surah Luqman
    32: 30,  # Surah As-Sajda
    33: 73,  # Surah Al-Ahzab
    34: 54,  # Surah Saba
    35: 45,  # Surah Fatir
    36: 83,  # Surah Ya-Sin
    37: 182, # Surah As-Saffat
    38: 88,  # Surah Sad
    39: 75,  # Surah Az-Zumar
    40: 85,  # Surah Ghafir
    41: 54,  # Surah Fussilat
    42: 53,  # Surah Ash-Shura
    43: 89,  # Surah Az-Zukhruf
    44: 59,  # Surah Ad-Dukhan
    45: 37,  # Surah Al-Jathiya
    46: 35,  # Surah Al-Ahqaf
    47: 38,  # Surah Muhammad
    48: 29,  # Surah Al-Fath
    49: 18,  # Surah Al-Hujurat
    50: 45,  # Surah Qaf
    51: 60,  # Surah Adh-Dhariyat
    52: 49,  # Surah At-Tur
    53: 62,  # Surah An-Najm
    54: 55,  # Surah Al-Qamar
    55: 78,  # Surah Ar-Rahman
    56: 96,  # Surah Al-Waqia
    57: 29,  # Surah Al-Hadid
    58: 22,  # Surah Al-Mujadila
    59: 24,  # Surah Al-Hashr
    60: 13,  # Surah Al-Mumtahina
    61: 14,  # Surah As-Saff
    62: 11,  # Surah Al-Jumua
    63: 11,  # Surah Al-Munafiqun
    64: 18,  # Surah At-Taghabun
    65: 12,  # Surah At-Talaq
    66: 12,  # Surah At-Tahrim
    67: 30,  # Surah Al-Mulk
    68: 52,  # Surah Al-Qalam
    69: 52,  # Surah Al-Haqqah
    70: 44,  # Surah Al-Ma'arij
    71: 28,  # Surah Nuh
    72: 28,  # Surah Al-Jinn
    73: 20,  # Surah Al-Muzzammil
    74: 56,  # Surah Al-Muddathir
    75: 40,  # Surah Al-Qiyama
    76: 31,  # Surah Al-Insan
    77: 50,  # Surah Al-Mursalat
    78: 40,  # Surah An-Naba
    79: 46,  # Surah An-Naziat
    80: 42,  # Surah Abasa
    81: 29,  # Surah At-Takwir
    82: 19,  # Surah Al-Infitar
    83: 36,  # Surah Al-Mutaffifin
    84: 25,  # Surah Al-Inshiqaq
    85: 22,  # Surah Al-Buruj
    86: 17,  # Surah At-Tariq
    87: 19,  # Surah Al-Ala
    88: 26,  # Surah Al-Ghashiya
    89: 30,  # Surah Al-Fajr
    90: 20,  # Surah Al-Balad
    91: 15,  # Surah Ash-Shams
    92: 21,  # Surah Al-Lail
    93: 11,  # Surah Ad-Duha
    94: 8,   # Surah Al-Inshirah
    95: 8,   # Surah At-Tin
    96: 19,  # Surah Al-Alaq
    97: 5,   # Surah Al-Qadr
    98: 8,   # Surah Al-Bayyina
    99: 8,   # Surah Az-Zalzala
    100: 11, # Surah Al-Adiyat
    101: 11, # Surah Al-Qaria
    102: 8,  # Surah At-Takathur
    103: 3,  # Surah Al-Asr
    104: 9,  # Surah Al-Humaza
    105: 5,  # Surah Al-Fil
    106: 4,  # Surah Quraish
    107: 7,  # Surah Al-Ma'un
    108: 3,  # Surah Al-Kawthar
    109: 6,  # Surah Al-Kafirun
    110: 3,  # Surah An-Nasr
    111: 5,  # Surah Al-Masad
    112: 4,  # Surah Al-Ikhlas
    113: 5,  # Surah Al-Falaq
    114: 6   # Surah An-Nas
}
daily_quran_verse = None
daily_quran_image = None
# Your existing function
def clear_database_table():
    try:
        with sqlite3.connect('bible.db') as conn:
            cursor = conn.cursor()

            # Clear the cached verses
            cursor.execute('DELETE FROM cached_verses')

            # Calculate the dates for yesterday, today, tomorrow, and the day before yesterday
            today = date.today()
            yesterday = today - timedelta(days=1)
            tomorrow = today + timedelta(days=1)

            formatted_yesterday = yesterday.strftime('%m/%d/%Y')
            formatted_today = today.strftime('%m/%d/%Y')
            formatted_tomorrow = tomorrow.strftime('%m/%d/%Y')

            # Delete any data older than yesterday for horoscope
            cursor.execute('DELETE FROM daily_horoscope_assignments WHERE date < ?', (formatted_yesterday,))

            used_message_ids = {sign: set() for sign in get_zodiac_signs()}  # Track used message IDs for each sign

            # Assign horoscopes for today and tomorrow, but first check if they already exist
            for assignment_date in [formatted_today, formatted_tomorrow]:
                for sign in get_zodiac_signs():
                    # Check if an entry already exists for the sign and date
                    cursor.execute(
                        'SELECT COUNT(1) FROM daily_horoscope_assignments WHERE sign = ? AND date = ?',
                        (sign, assignment_date)
                    )
                    if cursor.fetchone()[0] == 0:  # If no record exists
                        shuffle_and_assign_horoscopes(cursor, assignment_date, used_message_ids)

            daily_quran_verse_today = get_random_quran_verse()
            daily_quran_image = get_random_scenic_image()

            logging.info(f"Assigned daily Quran verse for today ({formatted_today}): Surah {daily_quran_verse_today[0]}, Ayah {daily_quran_verse_today[1]}")

            conn.commit()
            logging.info(f"Deleted data older than yesterday, reassigned horoscopes for today ({formatted_today}), and generated for tomorrow ({formatted_tomorrow}).")
    except sqlite3.Error as e:
        logging.error(f"Error clearing the database table and assigning new horoscopes: {e}")

# Function to get a random Quran verse
def get_random_quran_verse():
    # Randomly select a surah (chapter)
    random_surah = random.randint(1, 114)

    # Get the max number of ayat (verses) for the chosen surah
    max_ayah = surah_verse_counts[random_surah]

    # Randomly select an ayah (verse) within the surah
    random_ayah = random.randint(1, max_ayah)

    # Return the selected surah and ayah
    return random_surah, random_ayah

# Function to generate random light colors (for the lucky info)
def get_random_light_color():
    """Generate a random light color."""
    return f'rgba({random.randint(150, 255)}, {random.randint(150, 255)}, {random.randint(150, 255)}, 0.8)'

# Update the shuffle and assign function to handle lucky info colors
def shuffle_and_assign_horoscopes(cursor, target_date, used_message_ids):
    # Get the list of zodiac signs
    zodiac_signs = get_zodiac_signs()

    # Fetch all generic horoscope messages
    cursor.execute('SELECT id FROM generic_horoscope_messages')
    generic_messages = cursor.fetchall()

    if not generic_messages:
        logging.error("No generic horoscope messages found.")
        return

    # Shuffle the generic messages
    random.shuffle(generic_messages)

    # Assign shuffled messages to zodiac signs for the target date
    for sign in zodiac_signs:
        while True:
            message_id = random.choice(generic_messages)[0]

            # Ensure the message ID hasn't been used for this specific sign across yesterday, today, or tomorrow
            if message_id in used_message_ids[sign]:
                continue  # Skip if the message is already used for this sign

            # Mark the message ID as used for this sign
            used_message_ids[sign].add(message_id)
            break

        # Generate random light colors for the lucky information fields
        lucky_color_rect_color = get_random_light_color()
        lucky_number_rect_color = get_random_light_color()
        matching_sign_rect_color = get_random_light_color()

        # Insert the horoscope for the specific date, sign, and lucky colors
        cursor.execute('''
            INSERT INTO daily_horoscope_assignments (date, sign, message_id, 
                lucky_color_rect_color, lucky_number_rect_color, matching_sign_rect_color)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (target_date, sign, message_id, lucky_color_rect_color, lucky_number_rect_color, matching_sign_rect_color))

    logging.info(f"Assigned unique horoscopes and lucky info colors for {target_date}.")

def get_zodiac_signs():
    return ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 
            'Aquarius', 'Pisces']


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Allows access to rows as dictionaries
    return db
# Default route for when someone accesses the website without any path
@app.route('/')
def home():
    # Return the access denied page with a 404 status code
    return render_template('access_denied.html'), 404

@app.route('/faq')
@limiter.limit("1000 per day")
def faq():
    # Return the access denied page with a 404 status code
    return render_template('faq.html'), 404

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Custom error message for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    reference = "You have Exceeded Amount of Requests for the day"
    verse = "If you would like to unlock unlimited verses feature please contact our support at echocraftllc@gmail.com"
    image_path = get_random_scenic_image()
    return render_template('index-multi.html', verse=verse, reference=reference, image_path=image_path)


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


def get_random_bible_verse():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get the total number of verses
        cursor.execute("SELECT COUNT(*) FROM verses")
        total_verses = cursor.fetchone()[0]

        if total_verses == 0:
            logging.warning("No verses found in the database.")
            return None, None

        # Generate a random index within the range of available verses
        random_index = random.randint(0, total_verses - 1)
        
        # Fetch the verse at the random index
        cursor.execute("SELECT reference, verse, type FROM verses LIMIT 1 OFFSET ?", (random_index,))
        verse_data = cursor.fetchone()

        conn.close()

        if verse_data:
            reference, verse_text,type = verse_data
            return verse_text, reference, type

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
@limiter.limit("10000 per day")
def styles():
    return app.send_static_file('styles.css')

# Decorator to protect routes
def session_key_required(f):
    def decorated_function(*args, **kwargs):
        session_key = request.args.get('session_key')
        if session_key != app.secret_key:
            return jsonify({"msg": "Session key is missing or invalid"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def generate_unique_path():
    # You can use a library like `uuid` or `secrets` to generate a secure random string
    return str(uuid.uuid4())

@app.route('/random_quran_verse', methods=['GET'])
@limiter.limit("1000 per day")
@session_key_required
def random_quran_verse():
    try:    
        global daily_quran_verse
        global daily_quran_image
        unique_id = str(uuid.uuid4())
        session['quran_verse_uuid'] = unique_id  # Use 'bible_verse_uuid' for this project
        # Get the surah and ayah from daily_quran_verse
        surah, ayah = daily_quran_verse

        # Construct the API URL
        api_url = f"https://quranapi.pages.dev/api/{surah}/{ayah}.json"

        # Call the Quran API
        response = requests.get(api_url)
        if response.status_code != 200:
            return "Error retrieving Quran verse from API.", 500
        verse_data = response.json()

        print(verse_data)

        # Extract relevant data from the API response
        surah_name = verse_data.get('surahName')
        surah_name_arabic = verse_data.get('surahNameArabic')
        english_verse = verse_data.get('english')
        arabic_verse = verse_data.get('arabic1')
        mp3_audio_url = next(iter(verse_data.get('audio', {}).values()))['url']

        return redirect(url_for(
            'quran_verse',
            surah=surah_name,
            surah_arabic=surah_name_arabic,
            verse=english_verse,
            verse_arabic=arabic_verse,
            audio_urls=mp3_audio_url,
            image_path=daily_quran_image,
            uuid=unique_id
        ))

    except Exception as e:
        logging.error(f"Error in /random_verse endpoint: {e}")
        return "Internal server error.", 500

@app.route('/quran_verse/<uuid>', methods=['GET'])
@limiter.limit("1000 per day")
def quran_verse(uuid):
    stored_uuid = session.get('quran_verse_uuid')
    
    # Check if the UUID in the session matches the provided UUID
    if not stored_uuid or stored_uuid != uuid:
        return render_template('access_denied.html'), 404
    
    # If the UUID matches, clear it from the session for one-time use
    session.pop('quran_verse_uuid', None)
    
    try:
        # Retrieve the verse, surah, image path, and additional parameters
        verse = request.args.get('verse', '')
        reference = request.args.get('surah', '')
        reference_arabic = request.args.get('surah_arabic', '')
        verse_arabic = request.args.get('verse_arabic', '')
        image_path = request.args.get('image_path', '')
        audio_urls = request.args.get('audio_urls')
        print(audio_urls)

        # Render the 'index-arabic.html' template with the passed parameters
        return render_template(
            'index-arabic.html',
            verse=verse,
            reference=reference,
            reference_arabic=reference_arabic, 
            verse_arabic=verse_arabic,
            image_path=image_path,
            audio_urls=audio_urls
        )
    except Exception as e:
        logging.error(f"Error in /quran_verse endpoint: {e}")
        return "Internal server error.", 500

# Flask route
@app.route('/random_verse', methods=['GET'])
@limiter.limit("1000 per day")
@session_key_required
def random_verse():
    try:
        # Generate a unique UUID and store it in the session
        unique_id = str(uuid.uuid4())
        session['bible_verse_uuid'] = unique_id  # Use 'bible_verse_uuid' for this project

        # Retrieve random verse and scenic image
        bible_verse, reference, type = get_random_bible_verse()
        image_path = get_random_scenic_image()

        # Cache the verse using the user's IP address
        user_ip = request.remote_addr
        result = cache_verse(user_ip, reference, bible_verse, type, image_path)

        if result:
            cached_reference, cached_verse, cached_type, cached_image_path, *_ = result
            # Redirect to the verse page, passing the cached values along with the UUID
            return redirect(url_for('bible_verse', verse=cached_verse, reference=cached_reference, image_path=cached_image_path, uuid=unique_id))

    except Exception as e:
        logging.error(f"Error in /random_verse endpoint: {e}")
        return "Internal server error.", 500
    

@app.route('/bible_verse/<uuid>', methods=['GET'])
@limiter.limit("1000 per day")
def bible_verse(uuid):
    stored_uuid = session.get('bible_verse_uuid')
    
    if not stored_uuid or stored_uuid != uuid:
        return render_template('access_denied.html'), 404
    # If the UUID matches, clear it from the session for one-time use
    session.pop('bible_verse_uuid', None)
    try:
        verse = request.args.get('verse', '')
        reference = request.args.get('reference', '')
        image_path = request.args.get('image_path','')
        return render_template('index-multi.html', verse=verse, reference=reference, image_path=image_path)
    except Exception as e:
        logging.error(f"Error in /bible_verse endpoint: {e}")
        return "Internal server error.", 500

# Helper function to calculate expiration date based on subscription type
def calculate_expiration(tier):
    start_date = datetime.now()
    if tier == "daily":
        return (start_date + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    elif tier == "weekly":
        return (start_date + timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S')
    elif tier == "monthly":
        return (start_date + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    elif tier == "yearly":
        return (start_date + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
    return None

@app.route('/echomimic_register', methods=['POST'])
def register():
    data = request.json
    user_uuid = data.get("uuid")
    username = data.get("username")
    password = data.get("password")  # No hashing, plain-text password
    device_fingerprint = data.get("device_fingerprint")

    # Connect to the database
    conn = get_db()
    cursor = conn.cursor()

    # Check if the UUID is valid and issued in subscription_uuids table
    cursor.execute("SELECT tier, issued FROM subscription_uuids WHERE uuid = ?", (user_uuid,))
    uuid_record = cursor.fetchone()

    if not uuid_record:
        conn.close()
        return jsonify({"status": "failed", "message": "Invalid UUID."}), 400

    tier, issued = uuid_record
    if issued == 0:
        conn.close()
        return jsonify({"status": "failed", "message": "UUID has not been issued."}), 400

    # Check if username is already registered
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"status": "failed", "message": "Username already exists."}), 400

    # Calculate expiration date based on tier
    expiration_date = calculate_expiration(tier)

    # Register the user by inserting into users table
    cursor.execute('''
    INSERT INTO users (uuid, username, password, device_fingerprint, subscription_type, expiration_date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_uuid, username, password, device_fingerprint, tier, expiration_date))  # Storing plain-text password

    # Commit and close the connection
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Registration successful.", "expiration_date": expiration_date}), 200

# Endpoint to handle login
@app.route('/echomimic_login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    device_fingerprint = data.get("device_fingerprint")

    # Connect to the database
    conn = get_db()
    cursor = conn.cursor()

    # Check if username exists, password matches, and device fingerprint is correct
    cursor.execute("SELECT password, expiration_date, device_fingerprint FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()

    if not user_record:
        conn.close()
        return jsonify({"status": "failed", "message": "Invalid credentials."}), 401

    stored_password, expiration_date, stored_fingerprint = user_record
    if stored_password != password:  # Compare plain-text password
        conn.close()
        return jsonify({"status": "failed", "message": "Invalid credentials."}), 401

    if stored_fingerprint != device_fingerprint:
        conn.close()
        return jsonify({"status": "failed", "message": "Unrecognized device."}), 401

    # Close connection and return success with expiration date
    conn.close()
    return jsonify({"status": "success", "expiration_date": expiration_date}), 200

@app.route('/horoscope/<sign>', methods=['GET'])
@session_key_required
@limiter.limit("1000 per day")
def render_horoscope_page(sign):
    # Define the zodiac signs (in lowercase) to match the URL
    zodiac_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                    'libra', 'scorpio', 'sagittarius', 'capricorn', 
                    'aquarius', 'pisces']

    # Validate the zodiac sign
    if sign.lower() not in zodiac_signs:
        abort(404)

    # Generate a unique UUID
    unique_id = str(uuid.uuid4())
    # Store the UUID in the session for validation later
    session['horoscope_uuid'] = unique_id

    # Redirect the user to a new URL with the UUID
    safe_url = url_for('render_clean_horoscope_with_uuid', sign=sign, uuid=unique_id)
    return redirect(safe_url)

@app.route('/horoscope-view/<sign>/<uuid>', methods=['GET'])
@limiter.limit("1000 per day")
def render_clean_horoscope_with_uuid(sign, uuid):
    stored_uuid = session.get('horoscope_uuid')
    
    if not stored_uuid or stored_uuid != uuid:
        return render_template('access_denied.html'), 404
    # If the UUID matches, clear it from the session for one-time use
    session.pop('horoscope_uuid', None)

    # Fetch "today's" horoscope data
    today = date.today().strftime('%m/%d/%Y')

    # Fetch the horoscope data for today, including the colors and explanation IDs
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT daily_horoscope_assignments.date,
               generic_horoscope_messages.message, 
               generic_horoscope_messages.love_rating,
               generic_horoscope_messages.career_rating,
               generic_horoscope_messages.health_rating,
               generic_horoscope_messages.wealth_rating,
               generic_horoscope_messages.overall_rating,
               generic_horoscope_messages.lucky_color,
               generic_horoscope_messages.lucky_number,
               generic_horoscope_messages.matching_sign,
               generic_horoscope_messages.image_path,
               generic_horoscope_messages.love_explanation_id,   -- Fetch the explanation IDs
               generic_horoscope_messages.career_explanation_id, -- Fetch the explanation IDs
               generic_horoscope_messages.health_explanation_id, -- Fetch the explanation IDs
               generic_horoscope_messages.wealth_explanation_id, -- Fetch the explanation IDs
               generic_horoscope_messages.overall_explanation_id, -- Fetch the explanation IDs
               daily_horoscope_assignments.lucky_color_rect_color,
               daily_horoscope_assignments.lucky_number_rect_color,
               daily_horoscope_assignments.matching_sign_rect_color
        FROM daily_horoscope_assignments
        JOIN generic_horoscope_messages 
        ON daily_horoscope_assignments.message_id = generic_horoscope_messages.id
        WHERE daily_horoscope_assignments.date = ? 
          AND daily_horoscope_assignments.sign = ?
    ''', (today, sign.capitalize()))

    horoscope = cursor.fetchone()

    if not horoscope:
        abort(404)

    # Prepare horoscope data, including the explanation IDs and colors for the lucky items
    horoscope_data = {
        'date': today,
        'message': horoscope[1],
        'love_rating': horoscope[2],
        'career_rating': horoscope[3],
        'health_rating': horoscope[4],
        'wealth_rating': horoscope[5],
        'overall_rating': horoscope[6],
        'lucky_color': horoscope[7],
        'lucky_number': horoscope[8],
        'matching_sign': horoscope[9],
        'image_path' : horoscope[10],
        'love_explanation_id': horoscope[11],     # Add explanation IDs to the returned data
        'career_explanation_id': horoscope[12],   # Add explanation IDs to the returned data
        'health_explanation_id': horoscope[13],   # Add explanation IDs to the returned data
        'wealth_explanation_id': horoscope[14],   # Add explanation IDs to the returned data
        'overall_explanation_id': horoscope[15],  # Add explanation IDs to the returned data
        'lucky_color_rect_color': horoscope[16],  # Fetch the color for the lucky color block
        'lucky_number_rect_color': horoscope[17],  # Fetch the color for the lucky number block
        'matching_sign_rect_color': horoscope[18]  # Fetch the color for the matching sign block
    }

    # Render the HTML page with today's horoscope data and colors
    return render_template('horoscope.html', sign=sign.capitalize(), horoscope_data=horoscope_data)



@app.route('/horoscope/<sign>/<day>', methods=['GET'])
@limiter.limit("1000 per day")
def show_horoscope(sign, day):
    sign = sign.lower()

    # Determine the date based on the 'day' parameter
    if day == 'yesterday':
        target_date = date.today() - timedelta(days=1)
    elif day == 'tomorrow':
        target_date = date.today() + timedelta(days=1)
    else:
        target_date = date.today()

    formatted_date = target_date.strftime('%m/%d/%Y')

    # Fetch horoscope data, colors, and explanation IDs from the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT daily_horoscope_assignments.date,
               generic_horoscope_messages.message, 
               generic_horoscope_messages.love_rating,
               generic_horoscope_messages.career_rating,
               generic_horoscope_messages.health_rating,
               generic_horoscope_messages.wealth_rating,
               generic_horoscope_messages.overall_rating,
               generic_horoscope_messages.lucky_color,
               generic_horoscope_messages.lucky_number,
               generic_horoscope_messages.matching_sign,
               generic_horoscope_messages.image_path,
               generic_horoscope_messages.love_explanation_id,   -- Fetch the explanation IDs
               generic_horoscope_messages.career_explanation_id, -- Fetch the explanation IDs
               generic_horoscope_messages.health_explanation_id, -- Fetch the explanation IDs
               generic_horoscope_messages.wealth_explanation_id, -- Fetch the explanation IDs
               generic_horoscope_messages.overall_explanation_id, -- Fetch the explanation IDs
               daily_horoscope_assignments.lucky_color_rect_color,
               daily_horoscope_assignments.lucky_number_rect_color,
               daily_horoscope_assignments.matching_sign_rect_color
        FROM daily_horoscope_assignments
        JOIN generic_horoscope_messages 
        ON daily_horoscope_assignments.message_id = generic_horoscope_messages.id
        WHERE daily_horoscope_assignments.date = ? 
          AND daily_horoscope_assignments.sign = ?
    ''', (formatted_date, sign.capitalize()))

    horoscope = cursor.fetchone()

    if not horoscope:
        abort(404)

    # Prepare the data for rendering the template, including explanation IDs
    horoscope_data = {
        'date': formatted_date,
        'message': horoscope[1],
        'love_rating': horoscope[2],
        'career_rating': horoscope[3],
        'health_rating': horoscope[4],
        'wealth_rating': horoscope[5],
        'overall_rating': horoscope[6],
        'lucky_color': horoscope[7],
        'lucky_number': horoscope[8],
        'matching_sign': horoscope[9],
        'image_path': horoscope[10],
        'love_explanation_id': horoscope[11],     # Include explanation IDs in the returned data
        'career_explanation_id': horoscope[12],   # Include explanation IDs in the returned data
        'health_explanation_id': horoscope[13],   # Include explanation IDs in the returned data
        'wealth_explanation_id': horoscope[14],   # Include explanation IDs in the returned data
        'overall_explanation_id': horoscope[15],  # Include explanation IDs in the returned data
        'lucky_color_rect_color': horoscope[16],
        'lucky_number_rect_color': horoscope[17],
        'matching_sign_rect_color': horoscope[18],
    }

    return jsonify(horoscope_data)



def cache_verse(ip_address, reference, verse, type, image_path):
    retries = 5
    delay = 1
    
    while retries > 0:
        try:
            with sqlite3.connect('bible.db', timeout=10) as conn:
                cursor = conn.cursor()
                
                # Get the current time in the local timezone
                now = datetime.now()
                today = now.strftime('%Y-%m-%d')
                
                # Check if the verse is already cached for the IP address today
                cursor.execute('''
                    SELECT COUNT(*) FROM cached_verses 
                    WHERE ip_address = ? AND reference = ? AND verse = ?
                ''', (ip_address, reference, verse))
                exists = cursor.fetchone()[0] > 0
                
                if exists:
                    cached_data = get_cached_verse(ip_address)
                    return cached_data
                
                # Check the number of cached verses for the IP address today
                cursor.execute('''
                    SELECT COUNT(*) FROM cached_verses 
                    WHERE ip_address = ? AND DATE(timestamp) = ?
                ''', (ip_address, today))
                count = cursor.fetchone()[0]
                
                if count < 2:
                    # If there are less than 2 cached verses today, insert the new verse
                    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute('''
                        INSERT INTO cached_verses (ip_address, reference, verse, type, image_path, timestamp, last_sent)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (ip_address, reference, verse, type, image_path, timestamp, False))
                    conn.commit()
                    return reference, verse, type, image_path
                else:
                    # If there are already 2 cached verses today, select a random existing record
                    cached_data = get_cached_verse(ip_address)
                    return cached_data
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logging.error("UNIQUE constraint failed, restarting application.")
                restart_application()
            else:
                raise
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                retries -= 1
                time.sleep(delay)
            else:
                raise
        except Exception as e:
            raise

    raise sqlite3.OperationalError("Database is locked and retry attempts exceeded")

def restart_application():
    # Ensure any necessary cleanup is done here
    os.execv(__file__, ['python'] + [__file__])

def log_ip_access(ip_address):
    # Connect to the database
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()

    today = date.today().isoformat()

    # Try to update access log if the IP exists
    cursor.execute('''
        UPDATE horoscope_ip_access_log
        SET access_count = access_count + 1, last_access = ?
        WHERE ip_address = ?
    ''', (today, ip_address))

    # If no row was updated, insert a new log entry
    if cursor.rowcount == 0:
        cursor.execute('''
            INSERT INTO horoscope_ip_access_log (ip_address, last_access)
            VALUES (?, ?)
        ''', (ip_address, today))

    conn.commit()
    conn.close()

def get_cached_verse(ip_address):
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()

    # Start a transaction to ensure consistency
    conn.execute('BEGIN TRANSACTION')

    # Select a verse where last_sent is 0
    cursor.execute('''
        SELECT reference, verse, type, image_path FROM cached_verses
        WHERE ip_address = ? AND last_sent = 0
        ORDER BY timestamp DESC
        LIMIT 1
    ''', (ip_address,))
    verse = cursor.fetchone()
    
    if verse:
        # Update the selected verse's last_sent to 1
        cursor.execute('''
            UPDATE cached_verses
            SET last_sent = 1
            WHERE ip_address = ? AND reference = ?
        ''', (ip_address, verse[0]))

        # Update the remaining records' last_sent to 0
        cursor.execute('''
            UPDATE cached_verses
            SET last_sent = 0
            WHERE ip_address = ? AND reference != ?
        ''', (ip_address, verse[0]))

        # Commit the transaction
        conn.commit()
    else:
        # If no verse was found, rollback the transaction
        conn.rollback()

    conn.close()
    return verse
@app.before_first_request
def set_default_daily_quran_verse():
    global daily_quran_verse
    global daily_quran_image
    daily_quran_image = get_random_scenic_image()
    daily_quran_verse = get_random_quran_verse()
    logging.info(f"Assigned default daily Quran verse on startup: Surah {daily_quran_verse[0]}, Ayah {daily_quran_verse[1]}")

@scheduler.task('cron', id='clear_database_task', hour=0, minute=0)
def scheduled_task():
    clear_database_table()

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    run_flask()