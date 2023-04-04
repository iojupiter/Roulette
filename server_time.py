import requests

def get_kraken_server_time():
    # Get the Kraken server time
    url = 'https://api.kraken.com/0/public/Time'
    time_response = requests.get(url).json()
    server_time_unix = time_response['result']['unixtime']

    return server_time_unix
