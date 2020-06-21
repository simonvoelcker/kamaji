import re
import requests

from flask import abort, Blueprint, current_app, jsonify, Response

blueprint = Blueprint('api', __name__, url_prefix='/api')


def get_from_ghibli_api(entity_type: str) -> list:
    host = current_app.config['GHIBLI_API_HOST']
    response = requests.get(f'{host}/{entity_type}')
    if response.status_code != 200:
        message = f'Failed to get {entity_type} from Ghibli API'
        abort(Response(message, status=502))
    return response.json()


@blueprint.route('/films-and-people')
def list_films_and_people() -> Response:
    """
    Fetch films and people info via Ghibli API and create mapping of film names
    to people. No schema validation is performed on the JSON obtained from the
    Ghibli API, but a production-ready implementation should do this.
    It could be as simple as catching the KeyError exceptions that
    a bad schema would trigger and returning a 502 status code.
    """

    films = get_from_ghibli_api('films')
    people = get_from_ghibli_api('people')

    # Map film id to a list of people names.
    # Initialize with ALL film names (even those without people).
    people_by_film_id = {film['id']: [] for film in films}

    # Inconveniently, the "films" list provided by the people-endpoint contains
    # film URLs, not IDs. We must therefore parse the ID from the URL.
    film_url_rx = re.compile(r'^.*/(?P<film_id>[0-9a-f\-]+)$')

    # Add people to their respective films, as given by their "films" list.
    # Skip people whose film ID can't be parsed or is missing in the film list.
    # A production-ready implementation should log a warning here.
    for person in people:
        for film_url in person['films']:
            match = film_url_rx.match(film_url)
            if match and match.group('film_id') in people_by_film_id:
                people = people_by_film_id[match.group('film_id')]
                people.append(person['name'])

    # Prepare lookup of film title by ID.
    film_title_by_id = {film['id']: film['title'] for film in films}

    # Create dictionary which maps film names to a list of people in the film.
    # The lists of people (actually names) are sorted to provide stable output.
    films_and_people = {
        film_title_by_id[film_id]: sorted(people)
        for film_id, people in people_by_film_id.items()
    }

    response = jsonify(films_and_people)
    response.cache_control.max_age = 60
    return response
