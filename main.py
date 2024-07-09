import os
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get GitHub credentials from environment variables
github_username = os.getenv("GITHUB_USERNAME")
github_password = os.getenv("GITHUB_PASSWORD")

# Create a new Chrome session
driver = webdriver.Chrome()


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
def follow_stargazers(page):
    driver.get(f"https://github.com/torvalds/linux/stargazers?page={page}")
    time.sleep(3)

    # Find all follow buttons on the page
    follow_buttons = driver.find_elements(By.XPATH, "//input[@type='submit' and @name='commit' and @value='Follow']")

    if not follow_buttons:
        return False  # No follow buttons found, likely end of pages

    threads = []
    for button in follow_buttons:
        thread = threading.Thread(target=click_follow_button, args=(button,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return True


# Function to click a follow button
def click_follow_button(button):
    try:
        button.click()
    except Exception as e:
        print(f"Error clicking follow button: {e}")


# Log in to GitHub
github_login(github_username, github_password)

# Loop through pages and follow stargazers
page = 1
while follow_stargazers(page):
    page += 1

# Close the browser
driver.quit()