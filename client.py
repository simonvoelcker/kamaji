from flask import Blueprint

blueprint = Blueprint('client', __name__, static_folder='static')


@blueprint.route('/')
def index():
    return blueprint.send_static_file('index.html')
