import requests
import datetime
import time


def get_crypto_price_history(cryptocompare_api_key: str, symbol: str):
    price_history = {}
    earliest_timestamp = 1279324800
    timestamp = earliest_timestamp
    while True:
        timestamp += 86400 * 2000
        request_url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={symbol}&tsym=USD&limit=2000&toTs={timestamp}&api_key={cryptocompare_api_key}'
        response = requests.get(request_url).json()
        time_to = response['Data']['TimeTo']
        response_price_history = response['Data']['Data']
        new_price_history = {}
        for day_price in response_price_history:
            if day_price['high'] == 0:
                continue
            day_timestamp = day_price['time']
            date = datetime.datetime.fromtimestamp(day_timestamp).strftime('%Y-%m-%d')
            new_price_history[date] = {
                'open': day_price['open'],
                'high': day_price['high'],
                'low': day_price['low'],
                'close': day_price['close'],
                'volume': day_price['volumefrom']
            }
        price_history.update(new_price_history)
        if time.time() - time_to < 86400:
            break
    return price_history
