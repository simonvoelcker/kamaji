import os

from flask import Flask

from api import blueprint as api_blueprint
from client import blueprint as client_blueprint


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    app.register_blueprint(api_blueprint)
    app.register_blueprint(client_blueprint)

    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'Unsafe Secret')
    app.config['TESTING'] = testing
    app.config['GHIBLI_API_HOST'] = os.environ.get(
        'GHIBLI_API_HOST',
        'https://ghibliapi.herokuapp.com'
    )
    return app
