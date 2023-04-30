#!/bin/bash

# FLASK_APP=app.py FLASK_DEBUG=1 FLASK_ENV=development python3 -m flask run --host=localhost --port=5000 --debugger --reload

flask --app worblehat.flaskapp --debug run --host=localhost --port=5000 --debugger --reload
