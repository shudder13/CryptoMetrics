import requests
import datetime
import time
import json
import dateutil.parser
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import curve_fit
from scipy.optimize import minimize_scalar
from sklearn.metrics import mean_absolute_percentage_error
from typing import Callable
from utils.redis_connection import redis_client


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
    
    redis_client.set(redis_key, json.dumps(price_history), ex=18000)

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
        bounds=(250, 252),
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
    
    redis_client.set(redis_key, json.dumps(result), ex=18000)

    return result


def get_logarithmic_regression_function(cryptocompare_api_key: str, symbol: str, date_offset: int = 250):
    price_history = get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)
    
    dates = list(map(lambda date: datetime.datetime.strptime(date, r"%Y-%m-%d"), price_history.keys()))
    prices = np.array([data['close'] for data in price_history.values()])

    def log_function(x, a, b):
        return a * np.log(x) + b
    
    x_data = np.array([x + date_offset for x in range(len(dates))])
    y_data = np.log(prices)

    (a, b), _ = curve_fit(log_function, x_data, y_data, p0 = (10, 0))

    return lambda date_offset: np.exp(log_function(date_offset, a, b))


def compute_moving_average(price_history: pd.DataFrame, length: int):
    moving_average = price_history.copy()
    moving_average[f'moving_average_{length}'] = price_history['price'].rolling(length).mean().dropna()
    moving_average = moving_average.drop(f'price', axis=1).dropna()
    return moving_average


def get_bitcoin_pi_cycle_tops_results(cryptocompare_api_key: str):
    price_history = get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol='BTC')
    price_history_df = pd.DataFrame({
        'date': sorted(price_history.keys()),
        'price': [price_history[date]['close'] for date in sorted(price_history.keys())]
    })
    daily_moving_average_111_days = compute_moving_average(price_history=price_history_df, length=111)
    daily_moving_average_350_days = compute_moving_average(price_history=price_history_df, length=350)
    daily_moving_average_350_days_doubled = daily_moving_average_350_days.copy()
    daily_moving_average_350_days_doubled['moving_average_350'] *= 2

    golden_cross_dates = []

    prev_crossing = False
    first_crossing_occurred = False
    for date, row in daily_moving_average_111_days.iterrows():
        ma111_value = row['moving_average_111']
        
        if date in daily_moving_average_350_days_doubled.index:
            ma350_doubled_value = daily_moving_average_350_days_doubled.loc[date, 'moving_average_350']
            current_crossing = ma111_value > ma350_doubled_value

            if current_crossing and not prev_crossing and first_crossing_occurred:
                golden_cross_dates.append(daily_moving_average_111_days.loc[date, "date"])

            prev_crossing = current_crossing

            if current_crossing and not first_crossing_occurred:
                first_crossing_occurred = True

    return {
        'daily_MA_111_days': daily_moving_average_111_days.set_index('date')['moving_average_111'].to_dict(),
        'daily_MA_350_days_doubled': daily_moving_average_350_days_doubled.set_index('date')['moving_average_350'].to_dict(),
        'tops': golden_cross_dates
    }


def get_risk_free_rate():
    redis_key = 'risk_free_rate'
    risk_free_rate_redis = redis_client.get(redis_key)
    if risk_free_rate_redis is not None:
        return float(risk_free_rate_redis)

    bond_ticker = '^TNX'
    bond_data = yf.download(bond_ticker)
    latest_yield = bond_data['Close'].iloc[-1] / 100

    redis_client.set(redis_key, latest_yield, ex=18000)
    return latest_yield


def get_sharpe_ratio(portfolio_expected_return: float, portfolio_volatility: float):
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


def compute_expected_return(price_history: pd.DataFrame, log_function: Callable, date_offset: int) -> float:
    current_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    price_first_date = price_history.index[0]
    days_difference = (dateutil.parser.parse(current_date) - dateutil.parser.parse(price_first_date)).days
    date_offset_365_days_later = days_difference + date_offset + 365
    expected_price_365_days_later = log_function(date_offset_365_days_later)
    current_price = price_history.loc[current_date, 'close']
    expected_365_days_return = (expected_price_365_days_later - current_price) / current_price
    return expected_365_days_return


def get_modern_portfolio_analysis(cryptocompare_api_key: str):
    BTC_price_history = pd.DataFrame.from_dict(get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol='BTC'), orient='index')
    ETH_price_history = pd.DataFrame.from_dict(get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol='ETH'), orient='index')
    
    BTC_date_offset = find_optimal_date_offset_for_logarithmic_regression(cryptocompare_api_key=cryptocompare_api_key, symbol='BTC')
    BTC_log_function = get_logarithmic_regression_function(cryptocompare_api_key=cryptocompare_api_key, symbol='BTC', date_offset=BTC_date_offset)
    ETH_date_offset = find_optimal_date_offset_for_logarithmic_regression(cryptocompare_api_key=cryptocompare_api_key, symbol='ETH')
    ETH_log_function = get_logarithmic_regression_function(cryptocompare_api_key=cryptocompare_api_key, symbol='ETH', date_offset=ETH_date_offset)
    
    BTC_365_days_expected_return = compute_expected_return(BTC_price_history, BTC_log_function, BTC_date_offset)
    ETH_365_days_expected_return = compute_expected_return(ETH_price_history, ETH_log_function, ETH_date_offset)

    asset_returns = pd.concat([BTC_price_history['close'].pct_change(), ETH_price_history['close'].pct_change()], axis=1).dropna()
    annual_covariance_matrix = asset_returns.cov() * 365

    number_of_portfolio_simulations = 300
    portfolio_simulations = []

    max_sharpe_ratio = -1
    max_sharpe_btc_weight = 0
    max_sharpe_eth_weight = 0
    max_sharpe_portfolio_expected_return = 0
    max_sharpe_volatility = 0
    
    for i in range(number_of_portfolio_simulations):
        btc_weight = i / (number_of_portfolio_simulations - 1)
        eth_weight = 1 - btc_weight

        weights = np.array([btc_weight, eth_weight])
        portfolio_expected_return = np.dot(weights, [BTC_365_days_expected_return, ETH_365_days_expected_return])
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(annual_covariance_matrix, weights)))
        portfolio_sharpe_ratio = get_sharpe_ratio(portfolio_expected_return=portfolio_expected_return, portfolio_volatility=portfolio_volatility)
        if portfolio_sharpe_ratio > max_sharpe_ratio:
            max_sharpe_ratio = portfolio_sharpe_ratio
            max_sharpe_btc_weight = btc_weight
            max_sharpe_eth_weight = eth_weight
            max_sharpe_portfolio_expected_return = portfolio_expected_return
            max_sharpe_volatility = portfolio_volatility

        portfolio_simulations.append({
            'BTC_weight': btc_weight,
            'ETH_weight': eth_weight,
            'expected_return': portfolio_expected_return,
            'volatility': portfolio_volatility
        })

    return {
        'max_sharpe_ratio': {
            'BTC_weight': max_sharpe_btc_weight,
            'ETH_weight': max_sharpe_eth_weight,
            'sharpe_ratio': max_sharpe_ratio,
            'expected_return': max_sharpe_portfolio_expected_return,
            'volatility': max_sharpe_volatility
        },
        'portfolio_simulations': portfolio_simulations
    }
