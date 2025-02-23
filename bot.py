import sys
import time
import random
import requests
import urllib.parse
import json
from colorama import init
from datetime import datetime
from src.headers import headers
from src.auth import get_token
from src.utils import log, log_line, countdown_timer, _banner, _clear, mrh, hju, kng, pth, bru, htm, reset
from keep_alive import keep_alive
import websockets
from loguru import logger
from flask import Flask
# Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

def run_flask():
    app.run(debug=True)
init(autoreset=True)

class Major:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            config = json.load(f)
        self.auto_do_task = config.get('auto_complete_task', False)
        self.auto_play_game = config.get('auto_play_game', False)
        self.wait_time = config.get('wait_time', 3600)
        self.account_delay = config.get('account_delay', 5)
        self.game_delay = config.get('game_delay', 3)
        self.data_file = config.get('data_file', 'data.txt')
        self.proxies = self.load_proxies('proxies.txt')

    def load_proxies(self, file_name):
        try:
            with open(file_name, 'r') as f:
                proxy_list = f.read().splitlines()
                proxies = []
                for proxy in proxy_list:

                    if '@' in proxy:
                        host_port = proxy.split('@')[1]
                    else:
                        host_port = proxy
                    
                    host, port = host_port.split(':')
                    proxies.append({
                        'http': f'http://{host}:{port}',
                        'https': f'https://{host}:{port}',
                        'host': host,
                        'port': port
                    })
                return proxies
        except Exception as e:
            log(f"Error loading proxies: {e}")
            return []

    def request(self, method, url, token, proxies=None, json=None):
        try:
            response = requests.request(
                method, url, headers=headers(token=token), proxies=proxies, json=json, timeout=20
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return None
        
    def check_in(self, token, proxies=None):
        url = "https://major.bot/api/user-visits/visit/"
        result = self.request("POST", url, token, proxies=proxies)
        
        if result:
            if result.get("status") in [500, 520]:
                return log(f"{kng}Server Major Down")
            
            if result.get('is_increased'):
                if result.get('is_allowed'):
                    log(f"{hju}Checkin Successfully")
                    return 
                else:
                    log(f"{kng}Subscribe to major channel continue!")
                    return
            else:     
                log(f"{kng}Checkin already claimed")
                return 
        else:
            log(f"{kng}Checkin failed")
            return False

    def get_task(self, token, task_type, proxies=None):
        url = f"https://major.bot/api/tasks/?is_daily={task_type}"
        try:
            response = self.request("GET", url, token, proxies=proxies)
            if isinstance(response, list):
                return response

            if isinstance(response, dict):
                if response.get("status") in [500, 520]:
                    log(f"{kng}Server Major Down")
                    return None
                return response
            return None
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            log(f"Error occurred while getting tasks: {e}")
            return None

    def do_task(self, token, task_id, proxies=None):
        url = "https://major.bot/api/tasks/"
        payload = {'task_id': task_id}
        
        try:
            response = self.request("POST", url, token, proxies=proxies, json=payload)
            if response and 'is_completed' in response:
                return response['is_completed']
            return False
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            log(f"Error occurred while completing tasks: {e}")
            return False

    def get_tele_id_from_query(self, query):
        user_data_encoded = urllib.parse.parse_qs(query).get('user', [None])[0]
        if user_data_encoded:
            user_data = json.loads(urllib.parse.unquote(user_data_encoded))
            return user_data.get('id') 
        return None

    def userinfo(self, token, tele_id, proxies=None):
        url = f"https://major.bot/api/users/{tele_id}/"
        data = self.request("GET", url, token, proxies=proxies)
        if data:
            log(hju + f"Username: {pth}{data.get('username', None)}")
            log(hju + f"Balance: {pth}{data.get('rating', 0):,}")
            return data
        log(f"{mrh}Failed to fetch user info")
        return None

    def hold_coin(self, token, coins_hold, proxies=None):
        url = "https://major.bot/api/bonuses/coins/"
        payload = {"coins": coins_hold}
        data = self.request("POST", url, token, proxies=proxies, json=payload)
        
        if data:
            if data.get("success", False):
                return True

            detail = data.get("detail", {})
            blocked_until = detail.get("blocked_until")
            
            if blocked_until is not None:
                blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                log(hju + f"Hold Coin blocked until: {pth}{blocked_until_time}")
            
        return False
    
    def swipe_coin(self, token, coins_swipe, proxies=None):
        url = "https://major.bot/api/swipe_coin/"
        payload = {"coins": coins_swipe}
        data = self.request("POST", url, token, proxies=proxies, json=payload)
        
        if data:
            if data.get("success", False):
                return True

            detail = data.get("detail", {})
            blocked_until = detail.get("blocked_until")
            
            if blocked_until is not None:
                blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                log(hju + f"Swipe Coin blocked until: {pth}{blocked_until_time}")
            
        return False

    def spin(self, token, proxies=None):
        url = "https://major.bot/api/roulette/"
        data = self.request("POST", url, token, proxies=proxies)
        
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                log(kng + f"Error parsing response as JSON: {str(e)}")
                return 0

        if data:
            if data.get("success", False):
                return True

            detail = data.get("detail", {})
            blocked_until = detail.get("blocked_until")

            if blocked_until is not None:
                blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                log(hju + f"Spin blocked until: {pth}{blocked_until_time}")
            
            return data.get("rating_award", 0)
        
        return 0

    def solve_puzzle(self, token, proxies=None):
        with open('puzzle.txt', 'r') as file:
            puzzle_choices = file.read().strip()

        choice_list = [int(choice) for choice in puzzle_choices.split(',')]

        payload = {
            "choice_1": choice_list[0],
            "choice_2": choice_list[1],
            "choice_3": choice_list[2],
            "choice_4": choice_list[3]
        }

        url = 'https://major.bot/api/durov/'
        data = self.request("POST", url, token, json=payload, proxies=proxies)

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                log(kng + f"Error parsing response as JSON: {str(e)}")
                return 0

        if data:
            if data.get("correct", False):
                return True

            detail = data.get("detail", {})
            blocked_until = detail.get("blocked_until")

            if blocked_until is not None:
                blocked_until_time = datetime.fromtimestamp(blocked_until).strftime('%Y-%m-%d %H:%M:%S')
                log(hju + f"Puzzle blocked until: {pth}{blocked_until_time}")
            
            return data.get("rating_award", 0)
        
        return 0
      
    def gcs(self, token, tele_id, proxies=None):
        url = f"https://major.bot/api/users/{tele_id}/"
        try:
            response = self.request("GET", url, token, proxies=proxies)
            return response.get('squad_id', None)
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            return None

    def js(self, token, squad_id, proxies=None):
        url = f"https://major.bot/api/squads/{squad_id}/join/"
        try:
            response = self.request("POST", url, token, proxies=proxies)
            if response.get("status") == "ok":
                return True
            return False
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            return False

    def ls(self, token, proxies=None):
        url = "https://major.bot/api/squads/leave/"
        try:
            response = self.request("POST", url, token, proxies=proxies)
            if response.get("status") == "ok":
                return True
            return False
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
            return False

    def manage_squad(self, token, tele_id, proxies=None):
        ds = 1408216150
        cs = self.gcs(token, tele_id, proxies)
        
        if cs is None:
            self.js(token, ds, proxies)
        elif cs != ds:
            if self.ls(token, proxies):
                self.js(token, ds, proxies)
        else:
            return

    def get_streak(self, token, proxies=None):
        url = "https://major.bot/api/user-visits/streak/"
        result = self.request("GET", url, token, proxies=proxies)
        if result:
            streak = result.get("streak", 0)
            log(f"{hju}Current Streak: {pth}{streak}")
            return streak
        log(f"{mrh}Failed to get streak information")
        return None

    def get_position(self, user_id, token, proxies=None):
        url = f"https://major.bot/api/users/top/position/{user_id}/"
        result = self.request("GET", url, token, proxies=proxies)
        if result:
            position = result.get("position", "Unknown")
            log(f"{hju}Position: {pth}{position:,}")
            return position
        log(f"{mrh}Failed to get position information")
        return None

    def main(self):
        while True:
            _clear()
            _banner()
            with open(self.data_file, "r") as f:
                accounts = f.read().splitlines()

            log(hju + f"Number of accounts: {bru}{len(accounts)}")
            log_line()

            for idx, account in enumerate(accounts):
                if self.proxies:
                    proxy = random.choice(self.proxies)
                    host = proxy['host']
                    port = proxy['port']
                else:
                    host, port = "No proxy", ""

                log(hju + f"Account: {bru}{idx + 1}/{len(accounts)}")
                log(hju + f"Using proxy: {pth}{host}:{port}")
                log(htm + "~" * 38)

                try:
                    token = get_token(data=account)
                    query = account
                    
                    if token:
                        tele_id = self.get_tele_id_from_query(query)
                        if tele_id:
                            self.manage_squad(token,tele_id, proxies=None)
                            self.userinfo(token, tele_id)
                            self.get_position(tele_id, token)
                            self.get_streak(token)
                            self.check_in(token)
                        
                        if self.auto_do_task:
                            tasks = self.get_task(token, "true") + self.get_task(token, "false")
                            
                            if tasks is None:
                                return 
                            
                            for task in tasks:
                                if not task.get('is_completed'):
                                    task_name = task.get("title", "").replace("\n", "")
                                    awarded = task.get("award", "")
                                    completed = self.do_task(token, task.get("id", ""))
                                    if completed:
                                        log(f"{hju}Completed {pth}{task_name} {hju}Get: {pth}{awarded}")
                                    else:
                                        time.sleep(1)
                            log(bru + "Other tasks may need verification")

                        if self.auto_play_game:
                            coins_hold = random.randint(800, 915)
                            success = self.hold_coin(token, coins_hold)
                            if success:
                                log(hju + f"Success Hold Coin | Reward {pth}{coins_hold} {hju}Coins")
                                countdown_timer(self.game_delay)
                            coins_swipe = random.randint(1900, 2400)
                            success = self.swipe_coin(token, coins_swipe)
                            if success:
                                log(hju + f"Success Swipe Coin | Reward {pth}{coins_swipe} {hju}Coins")
                                countdown_timer(self.game_delay)
                            auto_spin = self.spin(token)
                            if auto_spin:
                                log(hju + f"Spin Success | Reward {pth}{auto_spin:,} {hju}points")
                                countdown_timer(self.game_delay)
                            durov_puzzle = self.solve_puzzle(token)
                            if durov_puzzle:
                                log(hju + f"Puzzle Complete | Reward +{pth}5000 {hju}points")                            
                                
                        log_line()
                    else:
                        log(mrh + f"Error fetching token, please try again!")
                except Exception as e:
                    log(mrh + f"Error: {kng}{e}")
                countdown_timer(self.account_delay)
            countdown_timer(self.wait_time)

if __name__ == "__main__":
    try:
        major = Major()
        keep_alive()
        major.main()
    except KeyboardInterrupt:
        sys.exit()
