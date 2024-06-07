from flask import Flask, send_file
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import logging
import os
import textwrap
from gtts import gTTS

app = Flask(__name__)

# API Ninjas configuration
API_NINJAS_KEY = 'KOhfDMigH08gPebS/BhCVg==L5zJzDOsSgwbTLh0'  # Replace if needed
CATEGORY = 'nature'
API_URL = 'https://api.api-ninjas.com/v1/randomimage?category={}'


# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# Font Setup
font_directory = os.path.dirname(os.path.abspath(__file__))
font_file = os.path.join(font_directory, "ModernSans-Light.ttf")  # Replace with your modern font file

# Function to fetch a random Bible verse
def get_random_bible_verse():
    try:
        response = requests.get("https://bible-api.com/?random=verse")
        response.raise_for_status()
        data = response.json()
        verse = data['text']
        # Remove "(web)" before extracting the translation ID
        reference = f"{data['reference'].replace('(web)', '')} ({data['translation_id']})" 
        return verse, reference
    except requests.RequestException as e:
        logging.error(f"Error fetching Bible verse: {e}")
        return "Could not fetch Bible verse at this time.", ""

# Function to get a random scenic image from API Ninjas
from PIL import Image

def get_random_scenic_image():
    try:
        response = requests.get(API_URL.format(CATEGORY), headers={'X-Api-Key': API_NINJAS_KEY, 'Accept': 'image/jpg'}, stream=True)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        # Resize the image to 1080x1920
        resized_image = image.resize((1080, 1920))
        # Save the resized image to a BytesIO object
        resized_bytes = BytesIO()
        resized_image.save(resized_bytes, format='JPEG')
        resized_bytes.seek(0)
        return resized_bytes
    except requests.RequestException as e:
        logging.error(f"Error fetching scenic image: {e}")
        if response.status_code == 400:
            logging.error(f"Response content: {response.content}")
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
        font = ImageFont.truetype("./font.ttf", font_size)
        line_spacing = 10  # Adjust for desired spacing between lines
        shadow_offset = 2

        # Wrap and justify verse text
        wrapped_verse = textwrap.fill(verse, width=35)
        verse_lines = wrapped_verse.splitlines()

        # Calculate text dimensions
        left, top, ref_width, ref_height = d.textbbox((0, 0), reference, font=font)

        # Calculate total height of the verse, including line spacing
        _, _, _, line_height = d.textbbox((0, 0), "A", font=font)  # Get height of a single line
        verse_height = (line_height + line_spacing) * len(verse_lines) - line_spacing  # Total height with spacing

        total_text_height = ref_height + verse_height + 20

        # Determine text placement for centering
        ref_x = (screen_width - ref_width) // 2
        verse_x = (screen_width - max([d.textbbox((0, 0), line, font=font)[2] for line in verse_lines])) // 2
        y = (screen_height - total_text_height) // 2

        # Draw text with drop shadow
        d.text((ref_x + shadow_offset, y + shadow_offset), reference, font=font, fill=(0, 0, 0, 150))
        d.text((ref_x, y), reference, font=font, fill=(255, 255, 255, 255))

        # Draw verse lines with proper vertical spacing
        y += ref_height + 20
        for line in verse_lines:
            d.text((verse_x + shadow_offset, y + shadow_offset), line, font=font, fill=(0, 0, 0, 150))
            d.text((verse_x, y), line, font=font, fill=(255, 255, 255, 255))
            y += line_height + line_spacing

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
