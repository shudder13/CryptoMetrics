from flask import Flask
from flask_cors import CORS

from .routes.analysis_routes import analysis_blueprint
from .routes.api_routes import api_blueprint
from .routes.price_routes import price_history_blueprint

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

CORS(app)

api_blueprint.register_blueprint(price_history_blueprint)
api_blueprint.register_blueprint(analysis_blueprint)

app.register_blueprint(api_blueprint)
