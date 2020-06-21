# kamaji
This is a demo application which serves a simple page listing Studio Ghibli movies along with the characters in them. The data is obtained from a publicly available REST API.

## Design decisions

The application is a simple Flask app with one endpoint for the client, /movies/, and one for the data, /api/films-and-people. The naming is inconsistent (movie vs. film) because the former was specified this way to me and the latter stems from the Ghibli API :)

Since there is only a single, very simple API endpoint, bare-bones Flask was used, and no Flask-RESTPlus or even SwaggerUI. More complicated APIs should rely on these tools for documentation purposes and more readable code.

The "frontend" is a single static HTML page which includes a small JS script which in turn fetches the film-and-people data from the backend and renders it using an HTML list.

It would have been possible to serve a backend-rendered page by using Flask's `render_template` function. This would have made the JS script unnecessary and the loading of the page would occur in a single request, meaning there would not be a partially loaded page for the duration of the (slow) Ghibli API calls. However, by splitting the API into a layout (HTML) and a data part (JSON), both can be altered without affecting the other, thereby making the code more flexible and reusable. As is often the case, it ultimately depends on the use case which approach is better.

## Running it

### Run with Docker

- Install Docker
- `cd` into the `kamaji` directory
- `docker build . -t kamaji`
- `docker run --network=host -t kamaji`
- Open `localhost:8000/movies/` in your browser

### Run without Docker

- Install Python 3.6 or greater (f-strings required)
- `cd` into the `kamaji` directory
- `pip install -r requirements.txt`
- `python run_server.py`
- Open `localhost:8000/movies/` in your browser

Note how Docker did not save us any steps this time. But it replaces the virtual environment we would need in case we want to have other Python applications running on the same machine.

### Run the tests

- Install Python and the pip requirements as stated above
- `python -m unittest`
