from app import create_app

app = create_app()

# Note: This is not how one would run the application in production.
# One would instead set up a proper webserver and WSGI.
# Flask has extensive documentation on how to do this:
# https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment

app.run(host='localhost', port=8000, debug=False)
