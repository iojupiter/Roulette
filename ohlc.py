import requests
import time
import datetime
import json

def get_OHLC():
    # Make a request to the Kraken API to get the latest 15 minute XBT/USD candle
    url = "https://api.kraken.com/0/public/OHLC?pair=XBTUSD&interval=15"
    response = requests.get(url).json()

    # Extract the OHLC and volume data from the API response
    ohlcs = response["result"]["XXBTZUSD"]
    latest_candle = ohlcs[-2]
#    json_string = json.dumps(latest_candle, indent=4)
#    print(json_string)
    open_price = latest_candle[1]
    high_price = latest_candle[2]
    low_price = latest_candle[3]
    close_price = latest_candle[4]
    timestamp = latest_candle[0]
    quote_volume = format(float(latest_candle[5])*float(latest_candle[6]), '.2f')
    base_volume = format(float(latest_candle[6]), '.2f')

    # Convert the Unix time to the desired format
    t = time.strftime('%Y-%m-%d %H:%M', time.gmtime(timestamp))

    # Open the CSV file for appending
    with open('btcusd-15m.csv', 'a') as f:
        f.write("\n")
        f.write(f"KRAKEN,XBT,USD,{t},{open_price},{high_price},{low_price},{close_price},{quote_volume},{base_volume}")

    print("New Candle Fetched @ " + t)

    return float(close_price)
