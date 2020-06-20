from flask import jsonify, Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/movies')
def list_movies():
    movies = [
        'My neighbor Totoro',
        'Porco Rosso',
    ]
    return jsonify(movies)
