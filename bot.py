import requests
import json
from colorama import init, Fore, Style
import time
import datetime
import random
from keep_alive import keep_alive
import websockets
from loguru import logger
from flask import Flask

init(autoreset=True)

# Define color variables
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
MAGENTA = Fore.MAGENTA + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT
 # Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

def run_flask():
    app.run(debug=True)

def get_headers(access_token=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": "https://major.glados.app/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    if access_token:
        headers["authorization"] = f"Bearer {access_token}"
    return headers

def auth(init_data, retries=3, delay=2):
    url = "https://major.glados.app/api/auth/tg/"
    headers = get_headers()
    body = {
        "init_data": init_data
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}Error: QUERY INVALID / MATI", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            print(f"{RED}Error getting token: {e}", flush=True)
            if attempt < retries - 1:
                print(f"{YELLOW}Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None

def user_detail(access_token, user_id,retries=3,delay=2):
    url = f"https://major.glados.app/api/users/{user_id}/"
    headers = get_headers(access_token)
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}[ Balance ] : Error: Gagal mendapatkan balance", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                print(f"{YELLOW}[ Balance] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
    
def daily_login(access_token,retries=3,delay=2):
    url = f"https://major.glados.app/api/user-visits/streak/"
    headers = get_headers(access_token)
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}[ Daily Streak ] : Error: Gagal mendapatkan data", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            if attempt < retries - 1:
                print(f"{RED}[ Daily Streak ] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
     
def spin(access_token, retries=3, delay=2):
    url = f"https://major.glados.app/api/roulette"
    headers = get_headers(access_token)
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers)
            response_json = response.json()  # Parse JSON response before raising for status
            if response.status_code == 201:
                return response_json, response.status_code
            elif response.status_code == 400:
                return response_json, response.status_code
            else:
                print(f"{RED}[ Spin ] : Error: Gagal mendapatkan data", flush=True)
                return None, None
        except (requests.RequestException, ValueError) as e:
            # print(f"{RED}Error spin: {e}", flush=True)
            if attempt < retries - 1:
                print(f"{RED}[ Spin ] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None, None

def join_ghalz(access_token, retries=3, delay=2):
    url = f"https://major.glados.app/api/squads/2184271295/join/"
    headers = get_headers(access_token)
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers)
            response_json = response.json()  # Parse JSON response before raising for status
            if response.status_code == 201:
                return response_json, response.status_code
            elif response.status_code == 400:
                return response_json, response.status_code
            else:
                print(f"{RED}[ Squad ] : Error: Gagal mendapatkan data", flush=True)
                return None, None
        except (requests.RequestException, ValueError) as e:
            # print(f"{RED}Error spin: {e}", flush=True)
            if attempt < retries - 1:
                print(f"{RED}[ Squad ] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None, None

def check_in(access_token, retries=3, delay=2):
    url = f"https://major.glados.app/api/user-visits/visit/"
    headers = get_headers(access_token)
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers)
            response_json = response.json()  # Parse JSON response before raising for status
            if response.status_code == 200:
                return response_json
            elif response.status_code == 400:
                return response_json
            else:
                print(f"{RED}[ Check-in ] : Error: Gagal mendapatkan data", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            # print(f"{RED}Error spin: {e}", flush=True)
            if attempt < retries - 1:
                print(f"{RED}[ Check-in ] : Error Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
    
def hold_ghalibie(access_token,coins,retries=3,delay=2):
    url = f"https://major.glados.app/api/bonuses/coins/"
    headers = get_headers(access_token)
    body = {
        "coins": coins 
    }
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response_json = response.json()  # Parse JSON response before raising for status
            if response.status_code == 201:
                return response_json, response.status_code
            elif response.status_code == 400:
                return response_json, response.status_code
            else:
                print(f"{RED}[ Hold ] Error: Gagal mendapatkan data", flush=True)
                return None, None
        except (requests.RequestException, ValueError) as e:
            print(f"{RED}[ Hold ] Error hold: {e}", flush=True)
            if attempt < retries - 1:
                print(f"{RED}[ Hold ] : Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None, None
    
def get_tasks(access_token, is_daily,retries=3,delay=2):
    url = f"https://major.glados.app/api/tasks/?is_daily={str(is_daily).lower()}"
    headers = get_headers(access_token)
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}[ Task ] : Error: Gagal mendapatkan data", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            # print(f"{RED}[ Task ] : Error daily_login: {e}", flush=True)
            if attempt < retries - 1:
                print(f"{RED}[ Task ] : Error  Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
            
def get_squad(access_token, squad_id,retries=3,delay=2):
    url = f"https://major.glados.app/api/squads/2184271295/{squad_id}"
    headers = get_headers(access_token)
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                print(f"{RED}[ Squad ] : Error: Gagal mendapatkan data", flush=True)
                return None
        except (requests.RequestException, ValueError) as e:
            # print(f"{RED}[ Task ] : Error daily_login: {e}", flush=True)
            if attempt < retries - 1:
                print(f"{RED}[ Squad ] : Error  Retrying... ({attempt + 1}/{retries})", end="\r", flush=True)
                time.sleep(delay)
            else:
                return None
        
   
def process_task(access_token, task_id,retries=3,delay=2):
    url = "https://major.glados.app/api/tasks/"
    headers = get_headers(access_token)
    body = json.dumps({"task_id": task_id})
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=body)
            response_json = response.json()  # Parse JSON response before raising for status
            if response.status_code == 201:
                return response_json, response.status_code
            elif response.status_code == 400:
        
                return response_json, response.status_code
            else:
                print(f"{RED}[ Clear Task ] : Error: Gagal mendapatkan data", flush=True)
                return None, None
        except (requests.RequestException, ValueError) as e:
            print(f"{RED}[ Clear Task ] Error : {e}", flush=True)
            if attempt < retries - 1:
                print(f"{RED}[ Clear Task ] : Retrying... ({attempt + 1}/{retries})",end="\r",  flush=True)
                time.sleep(delay)
            else:
                return None, None
 
def print_welcome_message():
    print(Fore.WHITE + r"""
          
🆂🅸🆁🅺🅴🅻
          
█▀▀ █▀▀ █▄░█ █▀▀ █▀█ █▀█ █░█ █▀
█▄█ ██▄ █░▀█ ██▄ █▀▄ █▄█ █▄█ ▄█
          """)
    print(Fore.GREEN + Style.BRIGHT + "Major BOT")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n")      

def main():
    print_welcome_message()
    keep_alive()
    mode = 'n'
    if mode != 'Y':
        print(Fore.YELLOW + f"Select Hold Coin Mode: ")
        print(Fore.GREEN + Style.BRIGHT + f"1. Max Coin (915 Coin)")
        print(Fore.CYAN + Style.BRIGHT + f"2. Random 700-800 Coin")
        print(Fore.MAGENTA + Style.BRIGHT + f"3. Random 800-915 Coin")
        while True:
            try:
                select_score = 1
                if 1 <= select_score <= 3:
                    break
                else:
                    print(Fore.RED + Style.BRIGHT + "Masukan harus antara 1 dan 3.")
            except ValueError:
                print(Fore.RED + Style.BRIGHT + "Masukan harus berupa angka.")
    while True:                
        total_balance = 0 
        # Read data from query.txt and perform authentication for each line
        with open('query.txt', 'r') as file:
            init_data_lines = file.readlines()
        
        for index, init_data in enumerate(init_data_lines, start=1):
            init_data = init_data.strip()  # Remove any extra whitespace
            if not init_data:
                continue
            print(f"{YELLOW}Getting access token...", end="\r", flush=True)
            ghalibie = auth(init_data)
            time.sleep(1)
            if ghalibie is not None:
                access_token = ghalibie.get('access_token')
                user_data = ghalibie.get('user', {})
                user_id = user_data.get('id')
                username = user_data.get('username')
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')
                # rating = user_data.get('rating')

                print(f"{CYAN}====== Akun ke - {index} | {username} =======            ", flush=True)
                print(f"{CYAN}[ ID ] : {user_id}", flush=True)
                print(f"{CYAN}[ Name ] : {first_name} {last_name}", flush=True)


                print(f"{YELLOW}[ Balance ] : Getting balance...", end="\r", flush=True)
                ghalibie = user_detail(access_token,user_id)
                time.sleep(1)
                if ghalibie is not None:
                    rating = ghalibie.get('rating')
                    squad = ghalibie.get('squad_id')
                    total_balance += rating
                    if squad is not None:
                        cek_sq = get_squad(access_token, squad)
                        if cek_sq is not None:
                            name = cek_sq.get('name')
                            print(f"{GREEN}[ Squad ] : {name}                   ", flush=True)
                    else:
                        print(f"{YELLOW}[ Squad ] : Try to joinin Sirkel Ghalibie..", end="\r", flush=True)
                        join_sq, status_code = join_ghalz(access_token)  # Unpack the tuple here
                        time.sleep(1)
                        if join_sq is not None:
                            if status_code == 201:
                                print(f"{GREEN}[ Squad ] : Join Sirkel Ghalibie Success!                   ", flush=True)
                            else:
                                error = join_sq.get('detail')
                                print(f"{RED}[ Squad ] : {error}               ", flush=True)
                    print(f"{GREEN}[ Balance ] : {rating}                         ", flush=True)
                    
                if mode == 'Y':
                    continue
                print(f"{YELLOW}[ Check-in ] : Try to check-in...", end="\r", flush=True)
                ghalibie = check_in(access_token)
                time.sleep(1)
                if ghalibie is not None:
                    status = ghalibie['is_increased']
                    day = ghalibie['streak']
                    if status:
                        print(f"{GREEN}[ Check-in ] : Success | Day {day}                              ", flush=True)
                    else:
                        print(f"{RED}[ Check-in ] : Already | Day {day}                              ", flush=True)

                print(f"{YELLOW}[ Daily Streak ] : Getting info...", end="\r", flush=True)
                time.sleep(1)
                ghalibie = daily_login(access_token)
                if ghalibie is not None:
                    streak = ghalibie.get('streak')
                    print(f"{GREEN}[ Daily Streak ] : {streak}                             ", flush=True)
                print(f"{YELLOW}[ Spin ] : Getting info...", end="\r", flush=True)
                ghalibie, status_code = spin(access_token) if spin(access_token) else (None, None)  # Handle None case
                time.sleep(1)
                if ghalibie is not None:
                    if status_code == 201:
                        result = ghalibie.get('result')
                        rating_rewards = ghalibie.get('rating_reward')
                        print(f"{GREEN}[ Spin ] : Result {result} | Rating {rating_rewards}                       ", flush=True)
                    elif status_code == 400:
                        waktu = ghalibie.get('detail', {}).get('blocked_until')
                        if waktu:
                            waktu_diff = waktu - time.time()
                            hours = int(waktu_diff // 3600)
                            minutes = int((waktu_diff % 3600) // 60)
                            print(f"{RED}[ Spin ] : Already Spin. Next in {hours} hours {minutes} minutes.  ", flush=True)
                else:
                    print(f"{RED}[ Spin ] : Error: Gagal mendapatkan data", flush=True)
                
                if select_score == 1:
                    coins = 915
                elif select_score == 2:
                    coins = random.randint(700,800)
                elif select_score == 3:
                    coins = random.randint(800,915)
                
                ghalibie, status_code = hold_ghalibie(access_token,coins)  # Unpack the tuple here
                print(f"{YELLOW}[ Hold ] : Getting info...", end="\r", flush=True)
                time.sleep(1)
                if ghalibie is not None:
                    if status_code == 201:
                        print(f"{GREEN}[ Hold ] : You Got 915 Rating                      ", flush=True)
                    elif status_code == 400:
                        waktu = ghalibie.get('detail', {}).get('blocked_until')
                        if waktu:
                            waktu_diff = datetime.datetime.fromtimestamp(waktu) - datetime.datetime.now()
                            hours = int(waktu_diff.total_seconds() // 3600)
                            minutes = int((waktu_diff.total_seconds() % 3600) // 60)
                            print(f"{RED}[ Hold ] : Already Hold. Next in {hours} hours {minutes} minutes.  ", flush=True)
                ghalibie = get_tasks(access_token, True)
                print(f"{YELLOW}[ Daily Task ] : Getting info...", end="\r", flush=True)
                time.sleep(1)
                if ghalibie is not None:
                    print(f"{YELLOW}[ Daily Task ] : List Task                  ", flush=True)
                    for task in ghalibie:
                        task_id = task.get('id')
                        title = task.get('title')
                        award = task.get('award')
                    # Skip specific tasks
                        if title in ["Stars Purchase", "Extra Stars Purchase","Promote TON blockchain","Boost Major channel","Donate rating"]:
                            print(f"{YELLOW}    -> {title} - {Style.RESET_ALL}{Fore.YELLOW}Award: {award} {MAGENTA}Skipped {Style.RESET_ALL}          ", flush=True)
                            continue
        
                        # Process other tasks
                        ghalibie, status_code = process_task(access_token, task_id)
                        print(f"{YELLOW}    -> {title} - Award: {award} Clearing...{Style.RESET_ALL} ", end="\r", flush=True)
                        time.sleep(1)
                        
                        if ghalibie is not None:
                            # print(task_id,status_code)
                            if status_code == 201:
                                # print(ghalibie)
                                complete = ghalibie['is_completed']
                                if not complete:
                                    print(f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {RED}Failed{Style.RESET_ALL}                 ", flush=True)
                                else:
                                    print(f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {GREEN}Completed{Style.RESET_ALL}           ", flush=True)
                            elif status_code == 400:
                                complete = ghalibie['detail']
                                if complete == 'Task is already completed':
                                    print( f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {GREEN}Completed{Style.RESET_ALL}                 ", flush=True)
                                else:
                                    print( f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {RED}{ghalibie}{Style.RESET_ALL}                 ", flush=True)
                ghalibie = get_tasks(access_token, False)
                print(f"{YELLOW}[ Basic Task ] : Getting info...", end="\r", flush=True)
                time.sleep(1)
                if ghalibie is not None:
                    print(f"{YELLOW}[ Basic Task ] : List Task                  ", flush=True)
            
                    for task in ghalibie:
                        task_id = task.get('id')
                        title = task.get('title')
                        award = task.get('award')
                    # Skip specific tasks
                        if task_id in [26,33,21,20]:
                            print(f"{YELLOW}    -> {title} - {Style.RESET_ALL}{Fore.YELLOW}Award: {award} {MAGENTA}Skipped {Style.RESET_ALL}          ", flush=True)
                            continue
        
                        # Process other tasks
                        ghalibie, status_code = process_task(access_token, task_id)
                        print(f"{YELLOW}    -> {title} - Award: {award} Clearing...{Style.RESET_ALL} ", end="\r", flush=True)
                        time.sleep(1)
                        
                        if ghalibie is not None:
                            # print(task_id,status_code)
                            if status_code == 201:
                                # print(ghalibie)
                                complete = ghalibie['is_completed']
                                if not complete:
                                    print(f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {RED}Failed{Style.RESET_ALL}                 ", flush=True)
                                else:
                                    print(f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {GREEN}Completed{Style.RESET_ALL}           ", flush=True)
                            elif status_code == 400:
                                complete = ghalibie['detail']
                                if complete == 'Task is already completed':
                                    print( f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {GREEN}Completed{Style.RESET_ALL}                 ", flush=True)
                                else:
                                    print( f"{YELLOW}    -> {title} -{Style.RESET_ALL}{Fore.YELLOW} Award: {award} {RED}{ghalibie}{Style.RESET_ALL}                 ", flush=True)

            else:
                continue

        print(f"{GREEN}Total Balance from all accounts: {total_balance}{Style.RESET_ALL}")
        print(Fore.BLUE + Style.BRIGHT + f"\n==========SEMUA AKUN TELAH DIPROSES==========\n", flush=True)
        animated_loading(30000)

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rMenunggu waktu claim berikutnya {frame} - Tersisa {remaining_time} detik         ", end="", flush=True)
            time.sleep(0.25)
    print("\rMenunggu waktu claim berikutnya selesai.                            ", flush=True)
# Execute the main function
if __name__ == "__main__":
    main()
