from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    CORS(app,
        origins=[
         'http://localhost',
         'http://localhost/admin/auth',
         'http://localhost/store',
         'https://sportsstoreapi.herokuapp.com'],
        supports_credentials=True)
    # app.config['CORS_HEADERS'] = 'Content-Type'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
