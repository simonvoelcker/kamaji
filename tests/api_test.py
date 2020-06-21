import unittest
import responses

from app import create_app


class ApiTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.app = create_app(testing=True)
        # Note: We could use config classes to distinguish production and test
        # configurations. If there was more configuration data to handle,
        # such as a DB connection, that would be advisable.
        self.app.config['GHIBLI_API_HOST'] = 'http://fakehost.com'
        self.client = self.app.test_client()

    @responses.activate
    def _run_request(self, mock_films, mock_people, status=200):
        """
        Run a request with given films and people to mock Ghibli API with.
        """
        responses.add(responses.GET, 'http://fakehost.com/films',
                      json=mock_films, status=status)
        responses.add(responses.GET, 'http://fakehost.com/people',
                      json=mock_people, status=status)
        return self.client.get('/api/films-and-people')

    def test_request_failure(self):
        response = self._run_request(mock_films=[], mock_people=[], status=418)
        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.data.decode('utf-8'),
                         'Failed to get films from Ghibli API')

    def test_no_films_or_people(self):
        """
        With no films or people, the expected output of
        our films-and-people API is an empty dictionary.
        """
        response = self._run_request(mock_films=[], mock_people=[])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

    def test_no_people(self):
        """
        With no people, we expect a dictionary with a key for each film.
        """
        film = {
            'id': '1',
            'title': 'Léon: The Professional'
        }
        response = self._run_request(mock_films=[film], mock_people=[])
        self.assertEqual(response.status_code, 200)
        expected_films_and_people = {
            'Léon: The Professional': [],
        }
        self.assertEqual(response.json, expected_films_and_people)

    def test_no_films(self):
        """
        With no films, the expected output of is an empty dictionary.
        We could still use the film IDs given in each persons "films" list,
        but we'd lack the film titles.
        """
        person = {
            'id': '1',
            'name': 'Mathilda',
            'films': ['http://fakehost.com/films/1'],
        }
        response = self._run_request(mock_films=[], mock_people=[person])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

    def test_one_film_two_people(self):
        film = {
            'id': '1',
            'title': 'Léon: The Professional'
        }
        people = [
            {
                'id': '1',
                'name': 'Mathilda',
                'films': ['http://fakehost.com/films/1']
            }, {
                'id': '2',
                'name': 'Léon',
                'films': ['http://fakehost.com/films/1']
            },
        ]
        response = self._run_request(mock_films=[film], mock_people=people)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'Léon: The Professional': ['Léon', 'Mathilda'],
        })

    def test_one_person_two_films(self):
        films = [
            {'id': '1', 'title': 'Léon: The Professional'},
            {'id': '2', 'title': 'Scarface'},
        ]
        person = {
            'id': '1',
            'name': 'Tony',
            'films': [
                'http://fakehost.com/films/1',
                'http://fakehost.com/films/2',
            ]
        }
        response = self._run_request(mock_films=films, mock_people=[person])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'Léon: The Professional': ['Tony'],
            'Scarface': ['Tony'],
        })
