import requests
import multiprocessing
import time

# URL of the website or API endpoint you want to fetch data from
url = "https://yellamispeaks.com/"

def fetch_data(url):
    while True:
        try:
            # Make a GET request to fetch the data
            response = requests.get(url)
            # time.sleep(1)
            # Check if the request was successful
            if response.status_code == 200:
                # Log the raw response content for debugging
                print("Raw response content:", response.content)
                
                # Check if the response content is not empty
                if response.content.strip():
                    try:
                        # Parse the JSON data
                        data = response.json()
                        
                        # Print the fetched data
                        for post in data:
                            print(f"Title: {post['title']}")
                            print(f"Body: {post['body']}\n")
                    except ValueError as e:
                        print(f"Failed to parse JSON: {e}")
                else:
                    print("Response content is empty.")
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    # Number of processes to spawn
    num_processes = 20

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=fetch_data, args=(url,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
