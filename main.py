import os
import time
import random
import logging
import threading
import re
import requests
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

LOGO = r"""
  ______ __  __ __     __     ___       __         ____     ____          
 / ___(_) /_/ // /_ __/ /    / _ |__ __/ /____    / __/__  / / /__ _    __
/ (_ / / __/ _  / // / _ \  / __ / // / __/ _ \  / _// _ \/ / / _ \ |/|/ /
\___/_/\__/_//_/\_,_/_.__/ /_/ |_\_,_/\__/\___/ /_/  \___/_/_/\___/__,__/
"""

DEFAULT_REPO_URL = "https://github.com/torvalds/linux"
DEFAULT_START_PAGE = 1
DEFAULT_SPEED_MODE = "random"

GITHUB_API = "https://api.github.com"

stop_thread = False


def listen_for_stop():
    global stop_thread
    while True:
        if input().strip().lower() == "stop":
            stop_thread = True
            break


def display_intro():
    print("--------------------------------------------------")
    print(LOGO)
    print("GitHub Auto Follow")
    print("Made by 💜 from Zigao Wang.")
    print("This project is licensed under MIT License.")
    print("GitHub Repo: https://github.com/ZigaoWang/github-auto-follow/")
    print("--------------------------------------------------")
    print("DISCLAIMER: This script may violate GitHub's community guidelines.")
    print("Use this script for educational purposes only.")
    print("To stop the script at any time, type 'stop' in the terminal.")
    print("--------------------------------------------------")


def get_user_agreement():
    agreement = input("Type 'agree' to continue: ").strip().lower()
    if agreement != "agree":
        print("You did not agree to the disclaimer. Exiting...")
        exit()


def load_token():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logging.error("GITHUB_TOKEN not found in environment variables.")
        exit(1)
    return token


def get_headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.star+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def parse_repo_url(repo_url):
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        logging.error(f"Invalid GitHub repository URL: {repo_url}")
        exit(1)
    owner, repo = match.group(1), match.group(2)
    repo = repo.removesuffix(".git")
    return owner, repo


def get_user_inputs():
    repo_url = (
        input(f"Enter the GitHub repository URL (default {DEFAULT_REPO_URL}): ").strip()
        or DEFAULT_REPO_URL
    )
    start_page = int(
        input(f"Enter the starting page (default {DEFAULT_START_PAGE}): ").strip()
        or DEFAULT_START_PAGE
    )
    speed_mode = (
        input(
            f"Enter speed mode (fast, medium, slow, random) (default {DEFAULT_SPEED_MODE}): "
        )
        .strip()
        .lower()
        or DEFAULT_SPEED_MODE
    )
    return repo_url, start_page, speed_mode


def set_delay(speed_mode):
    if speed_mode == "fast":
        return 0.1
    elif speed_mode == "medium":
        return 1
    elif speed_mode == "slow":
        return 5
    elif speed_mode == "random":
        return random.uniform(0.1, 10)
    else:
        logging.warning("Invalid speed mode. Defaulting to random.")
        return random.uniform(0.1, 10)


def get_stargazers(headers, owner, repo, page):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/stargazers?per_page=100&page={page}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        logging.error(f"Repository {owner}/{repo} not found.")
        return []
    if resp.status_code == 403:
        logging.error("API rate limit exceeded or insufficient permissions.")
        return []
    resp.raise_for_status()
    return resp.json()


def follow_user(headers, username):
    url = f"{GITHUB_API}/user/following/{username}"
    resp = requests.put(
        url, headers={**headers, "Accept": "application/vnd.github+json"}
    )
    if resp.status_code == 204:
        return True
    if resp.status_code == 403:
        logging.warning(f"Cannot follow {username}: rate limit or blocked.")
    elif resp.status_code == 404:
        logging.warning(f"User {username} not found.")
    else:
        logging.warning(f"Failed to follow {username}: HTTP {resp.status_code}")
    return False


def follow_stargazers(headers, owner, repo, page, delay, follow_count):
    stargazers = get_stargazers(headers, owner, repo, page)
    if not stargazers:
        return False, follow_count
    for entry in stargazers:
        username = entry["user"]["login"]
        if follow_user(headers, username):
            follow_count += 1
            logging.info(
                f"{follow_count}. Followed {username}: https://github.com/{username}"
            )
        else:
            logging.info(f"Skipped {username}")
        time.sleep(delay)
    return True, follow_count


def main():
    global stop_thread

    display_intro()
    get_user_agreement()
    load_dotenv()
    token = load_token()
    headers = get_headers(token)
    repo_url, start_page, speed_mode = get_user_inputs()
    owner, repo = parse_repo_url(repo_url)
    delay = set_delay(speed_mode)

    logging.info(
        f"Targeting {owner}/{repo} | Starting at page {start_page} | Speed: {speed_mode}"
    )

    stop_listener = threading.Thread(target=listen_for_stop, daemon=True)
    stop_listener.start()

    page = start_page
    follow_count = 0

    try:
        while not stop_thread:
            followed_on_page, follow_count = follow_stargazers(
                headers, owner, repo, page, delay, follow_count
            )
            if not followed_on_page:
                logging.info(f"No stargazers found on page {page}. Done.")
                break
            page += 1
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    finally:
        logging.info(f"Total users followed: {follow_count}")


if __name__ == "__main__":
    main()
