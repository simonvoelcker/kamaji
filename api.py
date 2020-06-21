import requests

from flask import jsonify, Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/films-and-people')
def list_films_and_people():
    response = requests.get('https://ghibliapi.herokuapp.com/films')
    if response.status_code != 200:
        return 'Failed to get films list from Ghibli API', 502
    films = response.json()

    film_title_by_id = {film['id']: film['title'] for film in films}

    response = requests.get('https://ghibliapi.herokuapp.com/people')
    if response.status_code != 200:
        return 'Failed to get people list from Ghibli API', 502
    people = response.json()

    # map film id to a list of people names
    # this mapping must be initialized with ALL film IDs as keys in case a film has no people in it
    people_by_film_id = {film['id']: [] for film in films}

    # add people to their respective films, as given by their "films" list
    # skip those people whose film ID was missing in the films list
    for person in people:
        for film_url in person['films']:
            # TODO use a regex
            film_id = film_url.split('/')[-1]
            if film_id in people_by_film_id:
                people_by_film_id[film_id].append(person['name'])

    # look up film names and replace keys
    # also sort people names for stable output
    films_and_people = {
        film_title_by_id[film_id]: sorted(people)
        for film_id, people in people_by_film_id.items()
    }

    return jsonify(films_and_people)
