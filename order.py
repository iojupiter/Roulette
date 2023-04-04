import requests
import json

def place_order_kraken(signature, nonce, order_type, volume):
    headers = {
        'API-Key': 'API KEY HERE',
        'API-Sign': signature,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }
    nonce_str = str(nonce)
    data = {
        "nonce": nonce_str,
        "ordertype": "market",
        "pair": "XBTUSD",
        "type": order_type,
        "volume": volume
    }

    response = requests.post('https://api.kraken.com/0/private/AddOrder', headers=headers, data=data)

    if response.status_code != 200:
        raise Exception("Failed to execute the order. Response: %s" % response.text)

    return response.json()
