import os
import datetime
from .db import get_db
from .ttb_algorithm import ttb_algo

from flask import Flask, request, url_for, render_template

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
        if number_of_courses is not None:
            num_of_course = int(number_of_courses)
            course = []
            class_code = []
            for i in range(num_of_course):
                course_temp = request.form.get("course " + (i+1))
                class_code_temp = request.form.get("class " + (i+1))
                course.append(course_temp)
                class_code.append(class_code_temp)
            run_template = render_template("index.html", number_course=num_of_course, term=term)
        else:
            run_template = render_template("index.html")
        return run_template

    
    @app.route('/conflicts', methods=["GET", "POST"])
    #get data from courses and find the conflicts
    def data():
        main_page = main()
        res = get_db(main_page.term, main_page.course, main_page.class_code)
        return res
        ttb_algo = ttb_algorithm()
        conflict_list = ttb_algo(res)
        if conflict_list == []:
            run_template = render.template("ttb.html", term, course, class_code, start_time, end_time, duration)
        else:
            run_template = render.template("conflicts.html", conflict_list)
        # for x in res:
        #     print(x)
        return run_template
