import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import signal
import sys

output_file = os.path.join(os.path.dirname(__file__), "top_verses.txt")
verses = set()  # Use a set to avoid duplicates

# Open the file before launching the browser
file = open(output_file, 'a')

def write_to_file(verse):
    file.write(verse + '\n')
    file.flush()
    print(f"Appended verse: {verse}")

def signal_handler(sig, frame):
    global driver
    print("Stopping WebDriver service...")
    if driver:
        driver.quit()
    file.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_top_verses():
    global driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.topverses.com/bible")
    time.sleep(2)  # Wait for the initial content to load

    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Parse div with id "content"
        content_div = soup.find('div', id='content')
        if not content_div:
            print("No div with id 'content' found.")
            break

        # Parse div with id "verse-container"
        verse_container_div = content_div.find('div', id='verse-container')
        if not verse_container_div:
            print("No div with id 'verse-container' found.")
            break

        # Loop through each div with class "container"
        container_divs = verse_container_div.find_all('div', class_='container')
        for container_div in container_divs:
            for div in container_div.find_all('div'):
                # Find the h2 tag inside each div
                h2_tag = div.find('h2')
                if not h2_tag:
                    continue

                # Find the a tag inside the h2 tag
                a_tag = h2_tag.find('a')
                if not a_tag:
                    continue

                # Get the text value of the a tag
                href_text = a_tag.text.strip()

                # If the verse is new, add to the set and write to the file
                if href_text and href_text not in verses:
                    verses.add(href_text)
                    write_to_file(href_text)

        # Scroll down to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time to balance speed and reliability

    driver.quit()

get_top_verses()
file.close()

if not verses:
    print("No verses were found.")
else:
    print(f"Successfully fetched {len(verses)} verses.")
