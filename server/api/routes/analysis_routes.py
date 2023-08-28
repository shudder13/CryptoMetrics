from flask import Blueprint, current_app
from service.services import find_optimal_date_offset_for_logarithmic_regression, get_logarithmic_regression_function
from service.services import get_logarithmic_regression_results
from service.services import get_crypto_price_history, get_sharpe_ratio

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import dateutil

analysis_blueprint = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_blueprint.route('/logarithmic-regression/<symbol>', methods=['GET'])
def logarithmic_regression(symbol: str):
    cryptocompare_api_key = current_app.config['CRYPTOCOMPARE_API_KEY']
    logarithmic_regression_results = get_logarithmic_regression_results(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)
    return logarithmic_regression_results


@analysis_blueprint.route('/modern-portfolio-analysis', methods=['GET'])
def modern_portfolio_analysis():
    cryptocompare_api_key = current_app.config['CRYPTOCOMPARE_API_KEY']
    BTC_price_history = pd.DataFrame.from_dict(get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol='BTC'), orient='index')
    ETH_price_history = pd.DataFrame.from_dict(get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol='ETH'), orient='index')

    BTC_logarithmic_function = get_logarithmic_regression_function(cryptocompare_api_key=cryptocompare_api_key, symbol='BTC')
    BTC_date_offset = find_optimal_date_offset_for_logarithmic_regression(cryptocompare_api_key=cryptocompare_api_key, symbol='BTC')

    ETH_logarithmic_function = get_logarithmic_regression_function(cryptocompare_api_key=cryptocompare_api_key, symbol='ETH')
    ETH_date_offset = find_optimal_date_offset_for_logarithmic_regression(cryptocompare_api_key=cryptocompare_api_key, symbol='ETH')

    BTC_first_date = BTC_price_history.index[0]
    current_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    days_difference = (dateutil.parser.parse(current_date) - dateutil.parser.parse(BTC_first_date)).days
    BTC_365_days_later_offset = days_difference + BTC_date_offset + 365
    BTC_expected_price_365_days_later = BTC_logarithmic_function(BTC_365_days_later_offset)
    BTC_current_price = BTC_price_history.loc[current_date, 'close']
    BTC_365_days_expected_return = ((BTC_expected_price_365_days_later - BTC_current_price) / BTC_current_price)

    ETH_first_date = ETH_price_history.index[0]
    ETH_days_difference = (dateutil.parser.parse(current_date) - dateutil.parser.parse(ETH_first_date)).days
    ETH_365_days_later_offset = ETH_days_difference + ETH_date_offset + 365
    ETH_expected_price_365_days_later = ETH_logarithmic_function(ETH_365_days_later_offset)
    ETH_current_price = ETH_price_history.loc[current_date, 'close']
    ETH_365_days_expected_return = ((ETH_expected_price_365_days_later - ETH_current_price) / ETH_current_price)

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
