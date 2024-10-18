import sqlite3
import uuid
import os
from datetime import datetime, timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, 'bible.db')
conn = sqlite3.connect('bible.db')
cursor = conn.cursor()
# Function to prompt for subscription type
def prompt_subscription_type():
    print("Select Subscription Type to Generate or Renew:")
    print("1 - Daily")
    print("2 - Weekly")
    print("3 - Monthly")
    print("4 - Yearly")
    choice = input("Enter your choice (1-4): ")

    subscription_types = {
        "1": "daily",
        "2": "weekly",
        "3": "monthly",
        "4": "yearly"
    }

    return subscription_types.get(choice, None)

# Function to prompt for the number of UUIDs to generate
def prompt_number_of_uuids():
    try:
        count = int(input("Enter the number of UUIDs to generate: "))
        return count
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

# Function to calculate the expiration date based on the subscription type
def calculate_expiration_date(subscription_type):
    current_date = datetime.now()
    
    if subscription_type == "daily":
        expiration_date = current_date + timedelta(days=1)
    elif subscription_type == "weekly":
        expiration_date = current_date + timedelta(weeks=1)
    elif subscription_type == "monthly":
        expiration_date = current_date + timedelta(days=30)
    elif subscription_type == "yearly":
        expiration_date = current_date + timedelta(days=365)
    
    # Format expiration date to avoid float/fractional seconds
    return expiration_date.strftime('%Y-%m-%d %H:%M:%S')

# Function to generate, insert, and print UUIDs
def generate_and_insert_uuids(tier, count):


    print(f"\nGenerating {count} UUID(s) for {tier.capitalize()} subscription:")
    
    generated_uuids = []  # To store generated UUIDs for printing later

    for _ in range(count):
        new_uuid = f"{tier.upper()}-{uuid.uuid4()}"  # Generate UUID with prefix
        expiration_date = calculate_expiration_date(tier)  # Calculate expiration date
        # Insert UUID into the database with issued set to 1 (true)
        cursor.execute('INSERT INTO subscription_uuids (uuid, tier, issued, expiration_date) VALUES (?, ?, 1, ?)', (new_uuid, tier, expiration_date))
        generated_uuids.append(new_uuid)

    conn.commit()
    conn.close()

    # Print generated UUIDs to provide to the user
    print("\nGenerated UUIDs:")
    for idx, uuid_str in enumerate(generated_uuids, 1):
        print(f"{idx}. {uuid_str}")

    print(f"\n{count} UUID(s) for {tier.capitalize()} subscription generated, marked as issued, and inserted successfully.")

# Function to renew an existing user's subscription by username
def renew_subscription_by_username(username, subscription_type):
    conn = sqlite3.connect('bible.db')
    cursor = conn.cursor()

    # Check if the username exists
    cursor.execute('SELECT username, expiration_date FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        new_expiration_date = calculate_expiration_date(subscription_type)
        cursor.execute('UPDATE users SET expiration_date = ? WHERE username = ?', (new_expiration_date, username))
        conn.commit()
        print(f"Subscription for {username} has been renewed. New expiration date: {new_expiration_date}")
    else:
        print(f"Username {username} not found in the database.")

    conn.close()

# Function to prompt for renewal or generation
def prompt_action():
    print("Select action:")
    print("1 - Generate new subscription UUIDs")
    print("2 - Renew existing subscription")
    choice = input("Enter your choice (1-2): ")
    return choice

# Main script to handle both generation and renewal
def main():
    action = prompt_action()

    if action == "1":
        # Generate new subscription UUIDs
        tier = prompt_subscription_type()
        if not tier:
            print("Invalid selection. Please run the script again and select a valid option.")
            return

        count = prompt_number_of_uuids()
        if count is None or count <= 0:
            print("Invalid number. Please run the script again and enter a valid number.")
            return

        generate_and_insert_uuids(tier, count)

    elif action == "2":
        # Renew an existing subscription by username
        username = input("Enter the username to renew: ")
        tier = prompt_subscription_type()
        if not tier:
            print("Invalid selection. Please run the script again and select a valid option.")
            return

        renew_subscription_by_username(username, tier)

    else:
        print("Invalid action. Please run the script again and select a valid option.")

if __name__ == "__main__":
    main()
