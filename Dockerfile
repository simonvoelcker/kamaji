# You can use this to run the server very conveniently with default options.
# Remember that the way run_server.py is implemented, this is not ready for
# production. A proper server and WSGI are missing.

FROM python:3.8-alpine
COPY . /
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python run_server.py
