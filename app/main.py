from flask import Flask, send_file,jsonify
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import logging
import os
import textwrap
from gtts import gTTS
import random

app = Flask(__name__)

# Initialize the rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"]  # Adjust the rate limit as needed
)
# Custom error message for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "You have exceeded the request limit. Please try again later."
    }), 429


# API Ninjas configuration
API_NINJAS_KEY = 'KOhfDMigH08gPebS/BhCVg==L5zJzDOsSgwbTLh0'  # Replace if needed
CATEGORY = 'nature'
API_URL = 'https://api.api-ninjas.com/v1/randomimage?category={}'


# Logging configuration
logging.basicConfig(level=logging.DEBUG)

font_file = os.path.join(os.path.dirname(__file__), '..', 'font', "font.ttf")


# Path to the top_verses.txt file
TOP_VERSES_FILE = os.path.join(os.path.dirname(__file__), '..',"top_verses.txt")

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

def get_random_bible_verse():
    if not VERSUS:
        return "No verses available.", ""
    try:
        random_verse = random.choice(VERSUS)
        # Fetch the verse details from the API
        response = requests.get(f"https://bible-api.com/{random_verse}")
        response.raise_for_status()
        data = response.json()
        verse = data['text']
        reference = f"{data['reference'].replace('(web)', '')} ({data['translation_id']})"
        return verse, reference
    except requests.RequestException as e:
        logging.error(f"Error fetching Bible verse: {e}")
        return "Could not fetch Bible verse at this time.", ""


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



def overlay_text_on_image(image_bytes, verse, reference, screen_width, screen_height):
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
        ref_line_height = max([d.textbbox((0, 0), line, font=font)[3] for line in ref_lines])
        verse_line_height = max([d.textbbox((0, 0), line, font=font)[3] for line in verse_lines])

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

        # Draw verse lines with proper vertical spacing
        for line in verse_lines:
            verse_x = (screen_width - d.textbbox((0, 0), line, font=font)[2]) // 2
            d.text((verse_x + shadow_offset, y + shadow_offset), line, font=font, fill=(0, 0, 0, 150))
            d.text((verse_x, y), line, font=font, fill=(255, 255, 255, 255))
            y += verse_line_height + line_spacing

        combined = Image.alpha_composite(image, txt)

        combined_bytes = BytesIO()
        combined.save(combined_bytes, format='PNG')
        combined_bytes.seek(0)
        return combined_bytes
    except Exception as e:
        logging.error(f"Error overlaying text on image: {e}")
        return None




# Flask route
@app.route('/random_verse', methods=['GET'])
def random_verse():
    try:
        bible_verse, reference = get_random_bible_verse()
        image_bytes = get_random_scenic_image()
        if image_bytes is None:
            return "Could not fetch scenic image at this time.", 500

        combined_image_bytes = overlay_text_on_image(image_bytes, bible_verse, reference,1080,1920)
        if combined_image_bytes is None:
            return "Error processing image.", 500

        return send_file(combined_image_bytes, mimetype='image/png')
    except Exception as e:
        logging.error(f"Error in /random_verse endpoint: {e}")
        return "Internal server error.", 500



if __name__ == '__main__':
    app.run(debug=True)
