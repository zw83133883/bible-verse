import requests
import concurrent.futures

url = 'http://127.0.0.1:5000/random_verse'

def make_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")

# Create a pool of threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit the tasks
    futures = [executor.submit(make_request, url) for _ in range(100)]

    # Wait for all the tasks to complete
    for future in concurrent.futures.as_completed(futures):
        pass  # Do nothing, just wait for completion
