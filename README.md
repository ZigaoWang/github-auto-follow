# GitHub Auto Follow

## Description

GitHub Auto Follow is a script that automatically follows users who have starred a specified GitHub repository. **Use this script for educational purposes only.** Note that this script may violate GitHub's community guidelines.

## Features

- Automatically follows users who starred a specified GitHub repository.
- Configurable speed mode (fast, medium, slow, random).
- Resumable from a specified starting page.
- Uses environment variables for secure credential management.

## Disclaimer

**DISCLAIMER:** This script may violate GitHub's community guidelines. Use this script for educational purposes only. The author is not responsible for any misuse or consequences resulting from the use of this script.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ZigaoWang/github-auto-follow.git
    cd github-auto-follow
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your GitHub credentials:

    ```plaintext
    GITHUB_USERNAME=your_github_username
    GITHUB_PASSWORD=your_github_password
    ```

## Usage

1. Run the script:

    ```bash
    python main.py
    ```

2. Follow the prompts to enter the repository URL, starting page, and speed mode.

3. To stop the script at any time, type `stop` in the terminal.

## Example

```plaintext
--------------------------------------------------

  ______ __  __ __     __     ___       __         ____     ____          
 / ___(_) /_/ // /_ __/ /    / _ |__ __/ /____    / __/__  / / /__ _    __
/ (_ / / __/ _  / // / _ \  / __ / // / __/ _ \  / _// _ \/ / / _ \ |/|/ /
\___/_/\__/_//_/\_,_/_.__/ /_/ |_\_,_/\__/\___/ /_/  \___/_/_/\___/__,__/

GitHub Auto Follow
Made by 💜 from Zigao Wang.
This project is licensed under MIT License.
GitHub Repo: https://github.com/ZigaoWang/github-auto-follow/
--------------------------------------------------
DISCLAIMER: This script may violate GitHub's community guidelines.
Use this script for educational purposes only.
To stop the script at any time, type 'stop' in the terminal.
--------------------------------------------------
Type 'agree' to continue: agree
Enter the GitHub repository URL (default https://github.com/torvalds/linux): 
Enter the starting page (default 1): 11
Enter speed mode (fast, medium, slow, random) (default random): medium
Starting now
...
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

Made by 💜 from Zigao Wang.