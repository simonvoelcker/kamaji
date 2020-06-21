from flask import Blueprint

blueprint = Blueprint('client', __name__, static_folder='static')


@blueprint.route('/movies')
def index():
    return blueprint.send_static_file('index.html')
