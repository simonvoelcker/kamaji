import requests

from flask import abort, jsonify, Blueprint, Response

blueprint = Blueprint('api', __name__, url_prefix='/api')


def get_from_ghibli_api(entity_type: str) -> list:
    response = requests.get(f'https://ghibliapi.herokuapp.com/{entity_type}')
    if response.status_code != 200:
        abort(Response('Failed to get films list from Ghibli API', status=502))
    return response.json()


@blueprint.route('/films-and-people')
def list_films_and_people() -> Response:
    films = get_from_ghibli_api('films')
    people = get_from_ghibli_api('people')

    # Map film id to a list of people names. Initialize with ALL film names (even those without people).
    people_by_film_id = {film['id']: [] for film in films}

    # Add people to their respective films, as given by their "films" list.
    # Skip those people whose film ID was missing in the films list.
    for person in people:
        for film_url in person['films']:
            # TODO use a regex
            film_id = film_url.split('/')[-1]
            if film_id in people_by_film_id:
                people_by_film_id[film_id].append(person['name'])

    # Prepare lookup of film title by ID.
    film_title_by_id = {film['id']: film['title'] for film in films}

    # Create dictionary which maps film names to a list of names of people in the film.
    # The lists of names are sorted to provide stable output.
    films_and_people = {
        film_title_by_id[film_id]: sorted(people)
        for film_id, people in people_by_film_id.items()
    }

    return jsonify(films_and_people)
