import requests
import time

url = "http://127.0.0.1:5000/random_verse"
requests_per_minute = 200
interval_seconds = 60 / requests_per_minute

def make_request():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        #print(response.json())  # Optionally print the response data
    except requests.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    while True:
        make_request()
        time.sleep(interval_seconds) 