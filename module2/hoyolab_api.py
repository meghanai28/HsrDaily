import requests
import json
import time
from bs4 import BeautifulSoup

# GET REQUEST

INFO_URL = 'https://sg-public-api.hoyolab.com/event/luna/os/info?act_id=e202303301540311&lang=en-us'
CHECK_IN_URL = 'https://sg-public-api.hoyolab.com/event/luna/os/sign'
CODE_REEDEM_URL = 'https://public-operation-hkrpg.hoyoverse.com/common/apicdkey/api/webExchangeCdkeyRisk'
LATEST_CODES_URL = 'https://game8.co/games/Honkai-Star-Rail/archives/410296'

class ApiService:
    def __init__(self):
    
        with open("../config.json") as f:
            self.config = json.load(f)
        self.cookie = self.config["hoyolab"]["cookie"]
        self.redeem_cookie = self.config["hoyolab"]["redeem_cookie"]
        self.uid = self.config["hoyolab"]["uid"]

    def get_check_in_info(self):
        response = requests.get(INFO_URL, headers={"Cookie": self.cookie})
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        data = None
        if response.status_code == 200 and 'json' in response.headers.get('Content-Type',''):
            data = response.json()
            print(f"parsed JSON keys: {data.keys()}")
        return data

    def check_is_sign(self):
        data = self.get_check_in_info()
        if data:
            print(data['data']['is_sign'])
            return data['data']['is_sign']
        return False
    
    def do_check_in(self):
        if not self.check_is_sign():
            response = requests.post(CHECK_IN_URL, headers={"Cookie": self.cookie}, json={"act_id": "e202303301540311", "lang": "en-us"})
            data = response.json()
            if data["retcode"] == 0:
                return True
            else:
                print(f"Error posting to check in")
                return False
        else:
            print("Already Checked In")
            return False

    def redeem_code(self,code):
        params = {"cdkey": code,"game_biz": "hkrpg_global","lang": "en","platform": "4","region": "prod_official_usa","t": int(time.time() * 1000),"uid": self.uid,}
        response = requests.post(CODE_REEDEM_URL, headers={"Cookie": self.redeem_cookie}, params = params )
        print(response.status_code)
        print(response.text)
        data = response.json()
        if data["retcode"] == 0:
                return True
        else:
            print(f"Error posting to redeem")
            return False
        
    def redeem_all_codes(self):
        response = requests.get("https://game8.co/games/Honkai-Star-Rail/archives/410296")
        soup = BeautifulSoup(response.text, "html.parser")
        all_codes = soup.find_all("input", class_ = "a-clipboard__textInput")

        for tag in all_codes:
            print(tag["value"])
            self.redeem_code(tag["value"])
            time.sleep(6)

def main():
    api_service = ApiService()
    api_service.do_check_in()
    api_service.redeem_all_codes()

if __name__ == "__main__":
    main()

        

