from flask import Flask,jsonify, render_template,request,g,redirect,url_for
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
import datetime

logging.basicConfig(level=logging.INFO)
# Disable logging for specific libraries
logging.getLogger('comtypes').setLevel(logging.ERROR)
logging.getLogger('pyttsx3').setLevel(logging.ERROR)
logging.getLogger("gtts").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)

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
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Function to clear the database table
def clear_database_table():
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cached_verses')
    conn.commit()
    conn.close()
    logging.info("Database table cleared.")
        


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Initialize the rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per hour"]  # Adjust the rate limit as needed
)
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
@limiter.limit("10 per day")
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

# Flask route
@app.route('/random_verse', methods=['GET'])
@limiter.limit("10 per day")
@session_key_required
def random_verse():
    try:
        # Get the requested version or default to 'niv'
        # version = request.args.get('version', 'niv')  
        # if version not in ['niv', 'cus']:  # Validate the version
        #     return "Invalid version. Please use 'niv' or 'cus'.", 400
        bible_verse, reference,type = get_random_bible_verse()
        image_path = get_random_scenic_image()

        user_ip = request.remote_addr
        result = cache_verse(user_ip, reference, bible_verse,type, image_path)
        if result:
            cached_reference,cached_verse, cached_type, cached_image_path,*_ = result
            return redirect(url_for('bible_verse', verse=cached_verse, reference=cached_reference,image_path=cached_image_path))
        # return redirect(url_for('bible_verse', path=unique_path)) 
    except Exception as e:
        logging.error(f"Error in /random_verse endpoint: {e}")
        return "Internal server error.", 500
    
@app.route('/random_verse_multi_language', methods=['GET'])
@limiter.limit("10 per day")
@session_key_required
def random_verse_multi_language():
    try:
        # Get the requested version or default to 'niv'
        # version = request.args.get('version', 'niv')  
        # if version not in ['niv', 'cus']:  # Validate the version
        #     return "Invalid version. Please use 'niv' or 'cus'.", 400
        bible_verse, reference,type = get_random_bible_verse()
        image_path = get_random_scenic_image()

        user_ip = request.remote_addr
        result = cache_verse(user_ip, reference, bible_verse,type, image_path)
        if result:
            cached_reference,cached_verse, cached_type, cached_image_path,*_ = result
            return redirect(url_for('bible_verse_multi_language', verse=cached_verse, reference=cached_reference,image_path=cached_image_path))
        # return redirect(url_for('bible_verse', path=unique_path)) 
    except Exception as e:
        logging.error(f"Error in /random_verse endpoint: {e}")
        return "Internal server error.", 500

@app.route('/bible_verse_multi_language', methods=['GET'])
@limiter.limit("10 per day")
def bible_verse_multi_language():
    try:
        verse = request.args.get('verse', '')
        reference = request.args.get('reference', '')
        image_path = request.args.get('image_path','')
        return render_template('index-multi.html', verse=verse, reference=reference, image_path=image_path)
    except Exception as e:
        logging.error(f"Error in /bible_verse endpoint: {e}")
        return "Internal server error.", 500    

@app.route('/bible_verse', methods=['GET'])
@limiter.limit("10 per day")
def bible_verse():
    try:
        # # Get user's IP address
        # user_ip = request.remote_addr
        # # Retrieve cached verse from the database
        # cached_data = get_cached_verse(user_ip)
        # if cached_data:
        #     reference, verse, language, image_path = cached_data
        #     print(cached_data)
        #     return render_template('index.html', verse=verse, reference=reference, image_path=image_path)
        # else:
        #     return render_template('rate_limit_error.html')
        verse = request.args.get('verse', '')
        reference = request.args.get('reference', '')
        image_path = request.args.get('image_path','')
        return render_template('index.html', verse=verse, reference=reference, image_path=image_path)
    except Exception as e:
        logging.error(f"Error in /bible_verse endpoint: {e}")
        return "Internal server error.", 500

    
def cache_verse(ip_address, reference,verse,type, image_path):
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()

    # Get the current time in the local timezone
    now = datetime.datetime.now()
    # Format the date as 'YYYY-MM-DD'
    today = now.strftime('%Y-%m-%d')

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
        conn.close()
        return reference, verse, type, image_path
    else:
        # If there are already 2 cached verses today, select a random existing record
        cached_data = get_cached_verse(ip_address)
        conn.close()
        return cached_data


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

@scheduler.task('cron', id='clear_database_task', hour=0, minute=0)
def scheduled_task():
    clear_database_table()

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':

    run_flask()