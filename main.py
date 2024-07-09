import os
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
def follow_stargazers():
    driver.get("https://github.com/torvalds/linux/stargazers")
    time.sleep(3)

    # Find all follow buttons on the page
    follow_buttons = driver.find_elements(By.XPATH, "//input[@type='submit' and @name='commit' and @value='Follow']")

    for button in follow_buttons:
        try:
            button.click()
            time.sleep(1)  # Wait a bit between clicks to avoid being flagged as a bot
        except Exception as e:
            print(f"Error clicking follow button: {e}")

# Log in to GitHub and follow stargazers
github_login(github_username, github_password)
follow_stargazers()

# Close the browser
driver.quit()