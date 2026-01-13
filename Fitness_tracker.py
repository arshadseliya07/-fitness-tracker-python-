import csv
import os
from datetime import date
import pandas as pd
import numpy as np


PROFILE_FILE = "profiles.csv"
LOG_FILE = "fitness_logs.csv"

def show_menu():
    print("\n========== Fitness Tracker ==========")
    print("1. Enter / Update User Profile")
    print("2. Add Daily Fitness Data")
    print("3. View Fitness Summary")
    print("4. Analyze Fitness Data")
    print("5. Get AI Health Suggestions")
    print("6. Download My Fitness Report")
    print("7. Exit")
    print("====================================")

# creating a profiles file
def initialize_profile_file():
    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "name", "age", "gender", "height", "weight"])

# creating a fitness_logs file
def initialize_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "date", "steps", "calories", "sleep", "water"])

# opening a profile file to write  
def load_profiles():
    profiles = []
    with open(PROFILE_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            profiles.append(row)
    return profiles

# Takes a list of profile dictionaries and saves them into a CSV file.
def save_profiles(profiles):
    with open(PROFILE_FILE, "w", newline="") as f:
        fieldnames = ["user_id", "name", "age", "gender", "height", "weight"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in profiles:
            writer.writerow(p)

#  It checks whether a given user_id already exists in the profiles data.
def user_exists(user_id):
    profiles = load_profiles()
    for p in profiles:
        if p["user_id"] == user_id:
            return True
    return False

#   Takes a user_id and checks whether it already exists in the profiles file.
def create_or_update_profile():
    profiles = load_profiles()
    user_id = input("Enter User ID: ").strip()

    for p in profiles:
        if p["user_id"] == user_id:
            print("\nProfile found:")
            print(p)

            choice = input("Do you want to update age and weight? (y/n): ").strip().lower()
            if choice == "y":
                p["age"] = input("Enter new age: ").strip()
                p["weight"] = input("Enter new weight: ").strip()
                print("Profile updated.")
                save_profiles(profiles)
            else:
                print("No changes made.")
            return

    print("\nNo profile found. Please Create new profile.")
    new_profile = {
        "user_id": user_id,
        "name": input("Enter name: ").strip().title(),
        "age": input("Enter age: ").strip(),
        "gender": input("Enter gender: ").strip().title(),
        "height": input("Enter height (cm): ").strip(),
        "weight": input("Enter weight (kg): ").strip()
    }
    profiles.append(new_profile)
    save_profiles(profiles)
    print("New profile created.")

# Defines a function to collect and store daily fitness details for a user.
def add_daily_fitness_data():
    user_id = input("Enter User ID: ").strip()

    if not user_exists(user_id):
        print("\n User not found.")
        print("Please create the user profile first using Option 1.\n")
        input("Press Enter to return to main menu...")
        return


    log = {
    "user_id": user_id,
    "date": date.today().isoformat(),
    "steps": input("Enter steps walked: ").strip(),
    "calories": input("Enter calories burned: ").strip(),
    "sleep": input("Enter sleep hours: ").strip(),
    "water": input("Enter water intake (litres): ").strip()
}


    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=log.keys())
        writer.writerow(log)

    print("Daily fitness data saved.")

def load_logs():
    logs = []
    with open(LOG_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append(row)
    return logs

# Defines a function to load fitness logs from the CSV file.

def view_fitness_summary():
    user_id = input("Enter User ID: ").strip()

    if not user_exists(user_id):
        print("\n User not found.")
        input("Press Enter to return to main menu...")
        return

    logs = load_logs()

    user_logs = []
    for log in logs:
        if log["user_id"] == user_id:
            user_logs.append(log)

    if len(user_logs) == 0:
        print("\nNo fitness data found for this user.")
        input("Press Enter to return to main menu...")
        return

    total_steps_walked = 0
    total_sleep = 0
    total_water = 0

    for log in user_logs:
        total_steps_walked += int(log["steps"])
        total_sleep += float(log["sleep"])
        total_water += float(log["water"])

    days = len(user_logs)

    print("\n========== Fitness Summary ==========")
    print("User ID:", user_id)
    print("Days logged:", days)
    print("Total steps walked:", total_steps_walked)
    print("Average sleep:", round(total_sleep / days, 2), "hours")
    print("Average water:", round(total_water / days, 2), "litres")
    print("====================================")

    input("Press Enter to return to main menu...")

# option 4 Analyze Fitness Data

def analyze_fitness_data():
    user_id = input("Enter User ID: ").strip()

    if not user_exists(user_id):
        print("\nUser not found.")
        input("Press Enter to return to main menu...")
        return

    if not os.path.exists(LOG_FILE):
        print("\nNo fitness data file found.")
        input("Press Enter to return to main menu...")
        return

    logs = load_logs()

    user_logs = []
    for log in logs:
        if log["user_id"] == user_id:
            user_logs.append(log)

    if len(user_logs) == 0:
        print("\nNo fitness data available for this user.")
        input("Press Enter to return to main menu...")
        return

    # Extract numeric values into lists
    steps_list = []
    sleep_list = []
    calories_list = []
    water_list = []

    for log in user_logs:
        steps_list.append(int(log["steps"]))
        sleep_list.append(float(log["sleep"]))
        calories_list.append(float(log["calories"]))
        water_list.append(float(log["water"]))

    # Convert lists into NumPy arrays
    steps_array = np.array(steps_list)
    sleep_array = np.array(sleep_list)
    calories_array = np.array(calories_list)
    water_array = np.array(water_list)

    print("\n========== Fitness Analysis ==========")
    print("User ID:", user_id)
    print("Average Steps Walked:", int(np.mean(steps_array)))
    print("Maximum Steps Walked:", int(np.max(steps_array)))
    print("Minimum Sleep (hrs):", round(np.min(sleep_array), 2))
    print("Average Calories Burned:", round(np.mean(calories_array), 2))
    print("Average Water Intake:", round(np.mean(water_array), 2), "litres")
    print("Minimum Water Intake:", round(np.min(water_array), 2), "litres")
    print("====================================")
    input("Press Enter to return to main menu...")


# option 6 to download a Fitness file
def download_fitness_report():
    user_id = input("Enter User ID: ").strip()

    if not user_exists(user_id):
        print("\nUser not found.")
        input("Press Enter to return to main menu...")
        return

    if not os.path.exists(LOG_FILE):
        print("\nNo fitness data file found.")
        input("Press Enter to return to main menu...")
        return

    logs = load_logs()

    user_logs = []
    for log in logs:
        if log["user_id"] == user_id:
            user_logs.append(log)

    if len(user_logs) == 0:
        print("\nNo fitness data available for this user.")
        input("Press Enter to return to main menu...")
        return

    filename = f"fitness_report_{user_id}.csv"

    with open(filename, "w", newline="") as f:
        fieldnames = ["user_id", "date", "steps", "calories", "sleep", "water"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for log in user_logs:
            writer.writerow(log)

    print(f"\nReport downloaded successfully as '{filename}'")
    input("Press Enter to return to main menu...")

# option 5 AI Suggessions

def ai_chat():
    
    import groq

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("API key not found. Please set GROQ_API_KEY.")
        return

    client = groq.Groq(api_key=api_key)

    print("\n========== AI Health Assistant ==========")
    print("Type your question (or type 'exit' to return to menu)")
    print("========================================")

    while True:
        user_prompt = input("\nAsk AI: ").strip()
        if user_prompt.lower() == "exit":
            break

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful fitness and health assistant."},
                    {"role": "user", "content": user_prompt}
                ],
                
            )

            print("\n AI:", response.choices[0].message.content)

        except Exception as e:
            print("Error communicating with AI:", e)




def main():
    initialize_profile_file()
    initialize_log_file()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_or_update_profile()
        elif choice == "2":
            add_daily_fitness_data()
        elif choice == "3":
            view_fitness_summary()

        elif choice == "4":
            analyze_fitness_data()
        elif choice == "5":
            ai_chat()
        elif choice == "6":
            download_fitness_report()
        elif choice == "7":
            print("Thank you for using Fitness Tracker. Stay Healthy!")
            break
        else:
            print("Invalid choice. Please select between 1 and 7.")


if __name__ == "__main__":
    main()


