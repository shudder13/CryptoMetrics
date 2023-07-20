from flask import Blueprint, current_app
from service import services


price_history_blueprint = Blueprint('price_history', __name__, url_prefix='/price-history')
crypto_price_history_blueprint = Blueprint('crypto_price_history', __name__, url_prefix = '/crypto')
price_history_blueprint.register_blueprint(crypto_price_history_blueprint)


@crypto_price_history_blueprint.route('/<symbol>', methods=['GET'])
def get_crypto_price_history(symbol: str):
    cryptocompare_api_key = current_app.config['CRYPTOCOMPARE_API_KEY']
    price_history = services.get_crypto_price_history(cryptocompare_api_key=cryptocompare_api_key, symbol=symbol)
    return price_history  # TODO
