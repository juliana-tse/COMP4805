import os
import datetime
from db import get_db

from flask import Flask, request, url_for

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    @app.route('/', methods=["GET", "POST"])
    #receive data from form
    def main():
        term = request.form.get("term")
        number_of_courses = request.form.get("no_courses")
        if (number_of_courses < 4) or (number_of_courses > 6):
            print("The number of courses is invalid")
        else:
            num_course = number_of_courses
    return render_template("index.html", number_course=num_course)

    
    @app.route('/conflicts')
    #get data from courses and find the conflicts
        def data():
        res = get_db()
        return res
        for x in res:
            print(x)
    return app
