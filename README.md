## Overview
This app checks for new grades posted on the gibz grade website and sends notifications to a Discord channel using webhooks.

## Setup

1. Ensure Python 3 is installed on your system.
2. Clone or download this repository to your local machine.
3. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
4. Update the `config.json` file with your credentials, Discord webhook URL, and other configuration details.
> [!IMPORTANT]
> The OTP code cannot contain spaces. Just delete any spaces

5. Run the main script to start checking for grades:
   ```
   python main.py
   ```

## Usage

- The script will perform an initial login and then check for new grades every 60 seconds.
- If new grades are detected, a notification is sent to the configured Discord webhook URL.
- Notifications for a grade are sent only once.
- The system maintains a record of sent notifications in `sent_grades.json`.
