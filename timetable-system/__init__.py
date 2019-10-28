import os
from datetime import datetime, timedelta
from .db import get_db
from .ttb_algorithm import check_conflicts
# import json
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

    @app.template_filter("increment_time")
    def increment_time(value, increment_value):
        # time_datetime =  datetime.strptime(value)
        increment_time = timedelta(hours=increment_value)
        result_time = value + increment_time
        # string_time = datetime.strftime(result_time)
        return result_time

    # app.jinja_env.filters['increment_time'] = increment_time

    @app.template_filter('strtotime')
    def strtotime(value):
        return datetime.strptime(value, '%H:%M:%S')

    # app.jinja_env.filters['strtotime'] = strtotime

    @app.template_filter('timetostr')
    def timetostr(value):
        return datetime.strftime(value, '%H:%M:%S')
    @app.route('/', methods=["GET", "POST"])
    #receive data from form
    def main():
        global term
        term = request.form.get("term")
        number_of_courses = request.form.get("no_courses")
        if number_of_courses is not None:
            global num_of_course
            num_of_course = int(number_of_courses)
            run_template = render_template("index.html", number_course=num_of_course, term=term)
        else:
            run_template = render_template("index.html")
        return run_template

    
    @app.route('/result', methods=["GET", "POST"])
    #get data from courses and find the conflicts
    def data():
        course = []
        class_code = []
        for i in range(num_of_course):
            course_temp = request.form.get("course " + str(i+1))
            class_code_temp = request.form.get("class " + str(i+1))
            course.append(course_temp)
            class_code.append(class_code_temp)
        res = get_db(term, course, class_code)
        # return res
        # ttb_algo = check_conflicts()
        conflict_list = check_conflicts(res, course)
        start_time_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        def daterange(start_time, end_time):
            for n in range(int((end_time - start_time).seconds / 3600)):
                yield start_time + timedelta(hours=n)
        # start_time = datetime(2013, 1, 1)
        # end_time = datetime(2015, 6, 2)
        
        day_start_time = datetime.strptime("08:30:00", "%H:%M:%S")
        day_end_time = datetime.strptime("18:30:00", "%H:%M:%S")
        ttb_range = daterange(day_start_time, day_end_time)
        # for single_date in daterange(day_start_time, day_end_time):
        #     print(single_date.strftime("%H:%M:%S"))
        if conflict_list == []:
            run_template = render_template(
                "timetable.html", days=start_time_list, initialtime=day_start_time, timeRange=ttb_range, results=res)
        else:
            run_template = render_template("conflicts.html", conflicts_list=conflict_list)
        # for x in res:
        #     print(x)
        return run_template


        # app.jinja_env.filters['timetostr'] = timetostr

    return app
