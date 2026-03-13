import requests
import json
import time

# GET REQUEST

INFO_URL = 'https://sg-public-api.hoyolab.com/event/luna/os/info?act_id=e202303301540311&lang=en-us'
CHECK_IN_URL = 'https://sg-public-api.hoyolab.com/event/luna/os/sign'
CODE_REEDEM_URL = 'https://sg-hk4e-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkeyHkrpg'

class ApiService:
    def __init__(self):
    
        with open("../config.json") as f:
            self.config = json.load(f)
        self.cookie = self.config["hoyolab"]["cookie"]
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
        params = {"cdkey": code, "game_biz": "hkrpg_global", "lang": "en", "region": "prod_official_usa", "t": time.time(), "uid": self.uid }
        response = requests.get(CODE_REEDEM_URL, headers={"Cookie": self.cookie}, params = params )
        data = response.json()
        if data["retcode"] == 0:
                return True
        else:
            print(f"Error posting to check in")
            return False

def main():
    api_service = ApiService()
    api_service.do_check_in()

if __name__ == "__main__":
    main()

        

