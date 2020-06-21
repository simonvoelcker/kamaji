# kamaji
Kamaji hands you the info you need from the Ghibli API.

## Run with Docker

- Install Docker
- `cd` into the `kamaji` directory
- `docker build . -t kamaji`
- `docker run --network=host -t kamaji`
- Open `localhost:8000/movies` in your browser

## Run without Docker

- Install Python 3.6 or greater (f-strings required)
- `cd` into the `kamaji` directory
- `pip install -r requirements.txt`
- `python run_server.py`
- Open `localhost:8000/movies` in your browser

Note how Docker did not save us any steps this time. But it replaces the virtual environment we would need in case we want to have other Python applications running on the same machine.

## Run the tests

- Install Python and the pip requirements as stated above
- `python -m unittest`
