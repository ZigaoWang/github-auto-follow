import os
import threading
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Logo and information
logo = r"""
  ______ __  __ __     __     ___       __         ____     ____          
 / ___(_) /_/ // /_ __/ /    / _ |__ __/ /____    / __/__  / / /__ _    __
/ (_ / / __/ _  / // / _ \  / __ / // / __/ _ \  / _// _ \/ / / _ \ |/|/ /
\___/_/\__/_//_/\_,_/_.__/ /_/ |_\_,_/\__/\___/ /_/  \___/_/_/\___/__,__/
"""
print("--------------------------------------------------")
print(logo)
print("GitHub Auto Follow")
print("Made by 💜 from Zigao Wang.")
print("This project is licensed under MIT License.")
print("GitHub Repo: https://github.com/ZigaoWang/github-auto-follow/")
print("--------------------------------------------------")

# Disclaimer
print("DISCLAIMER: This script may violate GitHub's community guidelines.")
print("Use this script for educational purposes only.")
print("To stop the script at any time, type 'stop' in the terminal.")
print("--------------------------------------------------")

# Ensure the user reads and agrees to the disclaimer
agreement = input("Type 'agree' to continue: ").strip().lower()
if agreement != 'agree':
    print("You did not agree to the disclaimer. Exiting...")
    exit()

# Load environment variables from .env file
load_dotenv()

# Get GitHub credentials from environment variables
github_username = os.getenv("GITHUB_USERNAME")
github_password = os.getenv("GITHUB_PASSWORD")


# Function to log in to GitHub
def github_login(username, password):
    driver.get("https://github.com/login")
    time.sleep(2)

    username_input = driver.find_element(By.ID, "login_field")
    password_input = driver.find_element(By.ID, "password")
    sign_in_button = driver.find_element(By.NAME, "commit")

    username_input.send_keys(username)
    password_input.send_keys(password)
    sign_in_button.click()
    time.sleep(2)


# Function to follow users on the stargazers page
def follow_stargazers(page, delay):
    driver.get(f"https://github.com/torvalds/linux/stargazers?page={page}")
    time.sleep(3)

    # Find all follow buttons on the page
    follow_buttons = driver.find_elements(By.XPATH, "//input[@type='submit' and @name='commit' and @value='Follow']")

    if not follow_buttons:
        return False  # No follow buttons found, likely end of pages

    threads = []
    for button in follow_buttons:
        thread = threading.Thread(target=click_follow_button, args=(button, delay))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return True


# Function to click a follow button with a delay
def click_follow_button(button, delay):
    try:
        button.click()
        time.sleep(delay)
    except Exception as e:
        print(f"Error clicking follow button: {e}")


# Prompt the user for the starting page and speed mode
start_page = int(input("Enter the starting page: "))
speed_mode = input("Enter speed mode (fast, medium, random): ").strip().lower()

# Set delay based on speed mode
if speed_mode == "fast":
    delay = 0.1
elif speed_mode == "medium":
    delay = 1
elif speed_mode == "random":
    delay = random.uniform(1, 3)
else:
    print("Invalid speed mode. Defaulting to random.")
    delay = random.uniform(1, 3)

print("Starting now")

# Create a new Chrome session
driver = webdriver.Chrome()

# Log in to GitHub
github_login(github_username, github_password)

# Loop through pages and follow stargazers
page = start_page
users_followed = 0
try:
    while True:
        if follow_stargazers(page, delay):
            users_followed += 1
            page += 1
        else:
            break
        # Check for stop command
        if input().strip().lower() == "stop":
            break
except KeyboardInterrupt:
    print("Program interrupted by user.")

# Output the number of users followed
print(f"Total users followed: {users_followed}")

# Close the browser
driver.quit()