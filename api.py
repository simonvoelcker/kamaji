from flask_restplus import Namespace, Resource

api = Namespace('Ghibli API', description='Ghibli API')


@api.route('/movies')
class MoviesApi(Resource):
    @api.doc(
        description='Get list of movies',
        response={
            200: 'Success'
        }
    )
    def get(self):
        return '', 200
