import requests
from concurrent.futures import ThreadPoolExecutor

# Configuration
url = "https://dailyreadbible.vip"  # Your website URL
concurrency = 10  # Number of concurrent threads to simulate multiple users

# Function to send a request
def send_request():
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Main function to run the unlimited stress test without delay
def stress_test():
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        while True:  # Infinite loop to send requests continuously
            futures = [executor.submit(send_request) for _ in range(concurrency)]
            
            # Check for any exceptions in completed requests
            for future in futures:
                future.result()

if __name__ == "__main__":
    stress_test()
