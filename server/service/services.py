import requests
import datetime
import time
import json
from utils.redis_connection import redis_client
import numpy as np
from scipy.optimize import curve_fit
import yfinance as yf


def get_crypto_price_history(cryptocompare_api_key: str, symbol: str):
    price_history_redis = redis_client.get(symbol)
    if price_history_redis is not None:
        return json.loads(price_history_redis)
    else:
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
        
        redis_client.set(symbol, json.dumps(price_history), ex=3600)

        return price_history


def get_logarithmic_regression(cryptocompare_api_key: str, symbol: str, date_offset: int = 250):
    price_history = get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)
    
    dates = list(map(lambda date: datetime.datetime.strptime(date, r"%Y-%m-%d"), price_history.keys()))
    prices = np.array([data['close'] for data in price_history.values()])

    def logarithmic_function(x, a, b):
        return a * np.log(x) + b
    
    x_data = np.array([x + date_offset for x in range(len(dates))])
    y_data = np.log(prices)

    (a, b), _ = curve_fit(logarithmic_function, x_data, y_data, p0 = (10, 0))

    return {
        'date_offset': date_offset,
        'function': lambda date_offset: np.exp(logarithmic_function(date_offset, a, b))
    }


def get_risk_free_rate():
    risk_free_rate_redis = redis_client.get('risk_free_rate')
    if risk_free_rate_redis is not None:
        return float(risk_free_rate_redis)

    bond_ticker = '^TNX'
    bond_data = yf.download(bond_ticker)
    latest_yield = bond_data['Close'].iloc[-1] / 100

    redis_client.set('risk_free_rate', latest_yield, ex=3600)
    return latest_yield



def get_sharpe_ratio(portfolio_expected_return, portfolio_volatility):
    risk_free_rate = get_risk_free_rate()

    return (portfolio_expected_return - risk_free_rate) / portfolio_volatility
