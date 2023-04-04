import requests
import json
import server_time
import urllib.parse
import hashlib
import hmac
import base64
import sign


def get_balance(coin):
    server_time_unix = server_time.get_kraken_server_time()
    urlpath = "/0/private/Balance"
    api_sec = "API SECRET HERE"
    params = {"nonce": server_time_unix}

    postdata = urllib.parse.urlencode(params)
    encoded = (str(params['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(api_sec), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    signature = sigdigest.decode()

    headers = {
        'API-Key': 'API KEY HERE',
        'API-Sign': signature,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }

    response = requests.post("https://api.kraken.com/0/private/Balance", headers=headers, data=params)
    response_json = response.json()
    balance = float(response_json["result"][coin])

    return balance


if __name__ == '__main__':
    balance = get_balance("XXBT")
    print(balance)
