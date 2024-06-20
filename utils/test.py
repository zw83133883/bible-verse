import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

base_url = "https://www.yappyspeaks.com"
image_dir = "/public/bg_images/"

def generate_image_name(number):
    """
    Generate a single image name for a given number.
    """
    return f"{number:010}.png"

def image_name_generator(start, end):
    """
    A generator to yield image names from start to end.
    """
    for number in range(start, end + 1):
        yield f"{number:010}.png"

def check_image_exists(url):
    """
    Check if an image exists at the given URL.
    """
    response = requests.head(url)
    return response.status_code == 200

def scrape_website_for_images(base_url, image_dir, start_number, end_number):
    """
    Scrape the website and check for images in the specified range.
    """
    found_images = []
    for image_name in image_name_generator(start_number, end_number):
        image_url = urljoin(base_url, image_dir + image_name)
        if check_image_exists(image_url):
            found_images.append(image_url)
    return found_images

if __name__ == "__main__":
    # Define the range for image names
    start_number = 1707131000
    end_number = 1707331100

    # Scrape the website and find existing images
    print("Checking for existing images in the specified range...")
    existing_images = scrape_website_for_images(base_url, image_dir, start_number, end_number)
    
    if existing_images:
        print("\nFound the following images:")
        for img_url in existing_images:
            print(img_url)
    else:
        print("No images found in the specified range.")
