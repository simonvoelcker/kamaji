from flask import Blueprint, render_template
from flask_restplus import Api

from api import api as movies_api

client_blueprint = Blueprint(
    'client_app',
    __name__,
    url_prefix='',
    static_url_path='static',
    static_folder='static',
    template_folder='templates',
)


@client_blueprint.route('/')
def index():
    return render_template('index.html')


# TODO it should be possible to go without blueprints
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_blueprint, title='Movies API', version='1.0.0', description='Movies API', doc='/doc/')
api.add_namespace(movies_api, path='/movies')
