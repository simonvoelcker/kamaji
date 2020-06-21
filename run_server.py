from app import create_app

app = create_app()

# Note: This is not how one would run the application in production,
# for reasons stated in the Flask documentation:
# https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment

app.run(host='localhost', port=8000, debug=False)
