import urllib.parse
import hashlib
import hmac
import base64
import requests
import time

def get_kraken_signature(endpoint, nonce, order_type, volume):

    urlpath = "/0/private/" + endpoint
    api_sec = "API SECRET HERE"
    nonce_str = str(nonce)
    data = {
        "nonce": nonce_str,
        "ordertype": "market",
        "pair": "XBTUSD",
        "type": order_type,
        "volume": volume
    }

    postdata = urllib.parse.urlencode(data)
    encoded = (nonce_str + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(api_sec), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())

    return sigdigest.decode()
