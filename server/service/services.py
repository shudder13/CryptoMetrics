import requests
import datetime
import time
import json
from utils.redis_connection import redis_client
import numpy as np
from scipy.optimize import curve_fit
import yfinance as yf
from sklearn.metrics import mean_absolute_percentage_error
import pandas as pd
from scipy.optimize import minimize_scalar
import dateutil.parser


def get_crypto_price_history(cryptocompare_api_key: str, symbol: str):
    redis_key = f'price_history_{symbol}'
    price_history_redis = redis_client.get(redis_key)
    if price_history_redis is not None:
        return json.loads(price_history_redis)
    
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
    
    redis_client.set(redis_key, json.dumps(price_history), ex=3600)

    return price_history


def find_optimal_date_offset_for_logarithmic_regression(cryptocompare_api_key: str, symbol: str):
    def objective_function(date_offset: float, cryptocompare_api_key: str, symbol: str):
        logarithmic_regression_function = get_logarithmic_regression_function(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)
        price_history = get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)

        result = {}

        first_date = min(price_history.keys(), key=dateutil.parser.parse)
        for date in price_history.keys():
            days_difference = (dateutil.parser.parse(date) - dateutil.parser.parse(first_date)).days
            result[date] = logarithmic_regression_function(days_difference + date_offset)

        number_of_days_for_prediction = int(0.5 * len(result))
        last_date = max(price_history.keys(), key=dateutil.parser.parse)
        for i in range(1, 1 + number_of_days_for_prediction):
            future_date = (dateutil.parser.parse(last_date) + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            days_difference = (dateutil.parser.parse(future_date) - dateutil.parser.parse(first_date)).days
            result[future_date] = logarithmic_regression_function(days_difference + date_offset)
        
        mape_score = compute_mean_absolute_percentage_error(price_history, result)
        return mape_score
    
    result = minimize_scalar(
        objective_function,
        bounds=(200, 500),
        method='bounded',
        args=(cryptocompare_api_key, symbol),
        options = {'xatol': 0.9}
    )
    return int(result.x)


def get_logarithmic_regression_results(cryptocompare_api_key: str, symbol: str):
    redis_key = f'logarithmic_regression_results_{symbol}'
    logarithmic_regression_results_redis = redis_client.get(redis_key)
    if logarithmic_regression_results_redis is not None:
        return json.loads(logarithmic_regression_results_redis)

    date_offset = find_optimal_date_offset_for_logarithmic_regression(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)
    logarithmic_regression_function = get_logarithmic_regression_function(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol, date_offset=date_offset)
    price_history = get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)

    result = {}

    first_date = min(price_history.keys(), key=dateutil.parser.parse)
    for date in price_history.keys():
        days_difference = (dateutil.parser.parse(date) - dateutil.parser.parse(first_date)).days
        result[date] = logarithmic_regression_function(days_difference + date_offset)

    number_of_days_for_prediction = int(0.5 * len(result))
    last_date = max(price_history.keys(), key=dateutil.parser.parse)
    for i in range(1, 1 + number_of_days_for_prediction):
        future_date = (dateutil.parser.parse(last_date) + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        days_difference = (dateutil.parser.parse(future_date) - dateutil.parser.parse(first_date)).days
        result[future_date] = logarithmic_regression_function(days_difference + date_offset)
    
    redis_client.set(redis_key, json.dumps(result), ex=3600)

    return result


def get_logarithmic_regression_function(cryptocompare_api_key: str, symbol: str, date_offset: int = 250):
    price_history = get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)
    
    dates = list(map(lambda date: datetime.datetime.strptime(date, r"%Y-%m-%d"), price_history.keys()))
    prices = np.array([data['close'] for data in price_history.values()])

    def logarithmic_function(x, a, b):
        return a * np.log(x) + b
    
    x_data = np.array([x + date_offset for x in range(len(dates))])
    y_data = np.log(prices)

    (a, b), _ = curve_fit(logarithmic_function, x_data, y_data, p0 = (10, 0))

    return lambda date_offset: np.exp(logarithmic_function(date_offset, a, b))


def get_risk_free_rate():
    redis_key = 'risk_free_rate'
    risk_free_rate_redis = redis_client.get(redis_key)
    if risk_free_rate_redis is not None:
        return float(risk_free_rate_redis)

    bond_ticker = '^TNX'
    bond_data = yf.download(bond_ticker)
    latest_yield = bond_data['Close'].iloc[-1] / 100

    redis_client.set(redis_key, latest_yield, ex=3600)
    return latest_yield


def get_sharpe_ratio(portfolio_expected_return, portfolio_volatility):
    risk_free_rate = get_risk_free_rate()

    return (portfolio_expected_return - risk_free_rate) / portfolio_volatility


def compute_mean_absolute_percentage_error(price_history: dict, predicted_price: dict):
    actual_price_df = pd.DataFrame({
        'date': sorted(price_history.keys()),
        'actual_price': [price_history[date]['close'] for date in sorted(price_history.keys())]
    })
    predicted_price_df = pd.DataFrame({
        'date': sorted(price_history.keys()),
        'predicted_price': [predicted_price[date] for date in sorted(price_history.keys())]
    })
    merged_df = actual_price_df.merge(predicted_price_df, on='date', how='inner')

    return mean_absolute_percentage_error(merged_df['actual_price'], merged_df['predicted_price'])
