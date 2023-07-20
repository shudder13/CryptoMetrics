from flask import Blueprint

analysis_blueprint = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_blueprint.route('/bitcoin-logarithmic-regression', methods=['GET'])
def bitcoin_logarithmic_regression():
    pass
