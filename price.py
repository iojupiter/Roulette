import requests

def get_xbtusd_price():
    # Get the XBT USD price
    ticker_url = 'https://api.kraken.com/0/public/Ticker?pair=XBTUSD'
    ticker_response = requests.get(ticker_url).json()
    xbt_usd_price = ticker_response['result']['XXBTZUSD']['c'][0]
    xbt_usd_price = float(xbt_usd_price)

    return xbt_usd_price
