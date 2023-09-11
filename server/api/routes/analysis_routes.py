from flask import Blueprint, current_app
from service.services import *

analysis_blueprint = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_blueprint.route('/logarithmic-regression/<symbol>', methods=['GET'])
def logarithmic_regression(symbol: str):
    cryptocompare_api_key = current_app.config['CRYPTOCOMPARE_API_KEY']
    return get_logarithmic_regression_results(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)


@analysis_blueprint.route('/Bitcoin-pi-cycle-tops', methods=['GET'])
def bitcoin_pi_cycle_tops():
    cryptocompare_api_key = current_app.config['CRYPTOCOMPARE_API_KEY']
    return get_bitcoin_pi_cycle_tops_results(cryptocompare_api_key=cryptocompare_api_key)


@analysis_blueprint.route('/modern-portfolio-analysis', methods=['GET'])
def modern_portfolio_analysis():
    cryptocompare_api_key = current_app.config['CRYPTOCOMPARE_API_KEY']
    return get_modern_portfolio_analysis(cryptocompare_api_key)
