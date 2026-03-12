import requests
import json

# GET REQUEST

url = 'https://sg-public-api.hoyolab.com/event/luna/os/info?act_id=e202303301540311&lang=en-us'

with open("../config.json") as f:
    config = json.load(f)

cookie = config["hoyolab"]["cookie"]

response = requests.get(url, headers={"Cookie": cookie})

print(f"Status Code: {response.status_code}")

print(f"Response Text: {response.text}")

if response.status_code == 200 and 'json' in response.headers.get('Content-Type',''):
    data = response.json()
    print(f"parsed JSON keys: {data.keys()}")