import time
import price
import sign
import server_time
import order
import balance
import sys
import csv

def close():
    xbt_usd_price = price.get_xbtusd_price()
    print("Closing position @ "+ str(xbt_usd_price) + " usd")
    xbt_balance = balance.get_balance("XXBT")
    nonce = server_time.get_kraken_server_time()
    signature = sign.get_kraken_signature("AddOrder", nonce, "sell", xbt_balance)
    sell_order = order.place_order_kraken(signature, nonce, "sell", xbt_balance)
    if sell_order['error']:
        print('Sell order failed:', sell_order['error'])
        sys.exit()
    else:
        print('Sell order placed successfully, ID:', sell_order['result']['txid'][0])
    print("\n")

    return

def open(size):
    xbt_usd_price = price.get_xbtusd_price()
    print("\n")
    print("Opening position @ "+ str(xbt_usd_price) + " usd")
    volume = size / xbt_usd_price
    nonce = server_time.get_kraken_server_time()
    signature = sign.get_kraken_signature("AddOrder", nonce, "buy", volume)
    buy_order = order.place_order_kraken(signature, nonce, "buy", volume)
    if buy_order['error']:
        print('Buy order failed:', buy_order['error'])
        sys.exit()
    else:
        print('Buy order placed successfully, ID:', buy_order['result']['txid'][0])

    return
