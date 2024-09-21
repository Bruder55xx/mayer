# Major Bot

A Python bot for interacting with the Major Telegram Bot API. This bot can perform various tasks such as checking in, managing tasks, holding coins, spinning, and retrieving user information.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [TWITTER](https://x.com/itsjaw_real)

## Register

To use this bot, you need to register it with the Major Telegram Bot. 

1. Open the [Major Telegram Bot](https://t.me/major/start?startapp=1396812260)
2. Click on the "Start App" or "Open App" button
3. Install This Major Telegram Bot
4. Have Fun 🦈

## Features

- **Puzzle**: Semi-automatic Solve Durov Puzzle `NEW` add puzzle number to puzzle.txt separated with (,) coma eg: `8,1,14,11` its the " BOX NUMBER "
- **Check In**: Automatically check in and increase the visit count.
- **Task Management**: Retrieve and complete daily tasks.
- **Coin Holding**: Play the hold coin game with a random amount.
- **Spin**: Spin the roulette and handle various responses.
- **Swipe Coin**: Swipe coin on the screen and claim coin rewards.
- **User Info**: Retrieve user information including balance and position.

## Requirements

- Python 3.8+

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/jawikas/major-bot.git
    ```

2. **Navigate to the project directory**

    ```bash
    cd major-bot
    ```

3. **Create a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `config.json` file**

    The `config.json` file should be in the root directory of the project. Here is a sample configuration:

    ```json
    {
    "use_proxies": true,
    "auto_complete_task": true,
    "auto_play_game": true,
    "account_delay": 5,
    "game_delay": 3,
    "wait_time": 3600,
    "data_file": "data.txt"
    }

    ```

    - `auto_complete_task`: Whether to automatically complete tasks.
    - `auto_play_game`: Whether to automatically play the All Game.
    - `account_delay`: Delay between processing each account (in seconds).
    - `wait_time`: Delay between processing all accounts (in seconds).
    - `game_delay`: Delay between processing for Each Game (in seconds)
    - `data_file`: File containing account data.

2. **Create a `proxies.txt` file**

    The `proxies.txt` file should be in the root directory and contain a list of proxies in the format `username:password@host:port`.

    Example:

    ```
    user1:pass1@ip1:port1
    user2:pass2@ip2:port2
    ```

3. **Create a `data.txt` file**

    The `data.txt` file should be in the root directory and contain one account per line.

    Example:

    ```
    query1
    query2
    ```

## Usage

To run the bot, execute the following command:

```bash
python bot.py
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact [ https://t.me/DeeplChainSup ]