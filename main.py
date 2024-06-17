from flask import Flask,jsonify, render_template,request,g,session,redirect,url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import logging
import os
import textwrap
import random
import pyttsx3
import base64
import sqlite3
import uuid
from werkzeug.middleware.proxy_fix import ProxyFix

logging.basicConfig(level=logging.INFO)
# Disable logging for specific libraries
logging.getLogger('comtypes').setLevel(logging.ERROR)
logging.getLogger('pyttsx3').setLevel(logging.ERROR)
logging.getLogger("gtts").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)
DATABASE = "bible.db"  # Replace with your database name


app = Flask(__name__, static_folder='static', template_folder='templates')
cache = Cache(app, config={'CACHE_TYPE': 'simple'}) 
print(os.environ) 
app.secret_key = os.getenv('SECRET_KEY', 'for dev') 
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
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


# Initialize the rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per hour"]  # Adjust the rate limit as needed
)
# Custom error message for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
        verse = session.get('verse', '')
        reference = session.get('reference', '')
        unique_path = session.get('unique_path', '')
        return redirect(url_for('bible_verse', verse=verse, reference=reference, path=unique_path))


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
@limiter.limit("2 per day")
@session_key_required
def random_verse():
    try:
        # Get the requested version or default to 'niv'
        version = request.args.get('version', 'niv')  
        if version not in ['niv', 'cus']:  # Validate the version
            return "Invalid version. Please use 'niv' or 'cus'.", 400
        bible_verse, reference = get_random_bible_verse(version)
        image_path = get_random_scenic_image()

        # Store in session for caching
        session['verse'] = bible_verse
        session['reference'] = reference
        session['image_path'] = image_path
        unique_path = generate_unique_path()
        session['unique_path'] = unique_path
        
        return redirect(url_for('bible_verse', verse=bible_verse, reference=reference, path=unique_path))
        # return redirect(url_for('bible_verse', path=unique_path)) 
    except Exception as e:
        logging.error(f"Error in /random_verse endpoint: {e}")
        return "Internal server error.", 500

@app.route('/bible_verse/<path:path>', methods=['GET'])
@limiter.limit("30 per day")
def bible_verse(path):
    try:
        # bible_verse = session.get('verse', '')
        # reference = session.get('reference', '')
        # image_path = session.get('image_path', '')

        # # #return render_template('index.html', verse=cached_data['verse'], reference=cached_data['reference'], image_path=cached_data['image_path'])
        # return render_template('index.html', verse=bible_verse, reference=reference, image_path=image_path)
                # Retrieve data from session if the path matches
        if session.get('unique_path') == path:
            verse = session.get('verse', '')
            reference = session.get('reference', '')
            image_path = session.get('image_path', '')
            return render_template('index.html', verse=verse, reference=reference, image_path=image_path)
        else:
            return render_template(['rate_limit_error.html'])
    except Exception as e:
        logging.error(f"Error in /bible_verse endpoint: {e}")
        return "Internal server error.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)