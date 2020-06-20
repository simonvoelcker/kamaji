import os

from flask import Flask
from flask_cors import CORS

from client import api_blueprint, client_blueprint


class Config:
    TESTING = False
    PRODUCTION = False


app = Flask(__name__)
# TODO cors config, or go without cors
CORS(app)

app.register_blueprint(api_blueprint)
app.register_blueprint(client_blueprint)
app.config.from_object(Config)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'Unsafe Secret')

app.run(host='localhost', port=8000, debug=False)
