import os
from datetime import datetime, timedelta
from .db import get_db, update_db, get_admin_db, insert_db, get_exist_course_db, get_term_db, delete_admin_db, get_course_by_id
from .ttb_algorithm import check_conflicts
from .ttb_admin_algorithm import check_course_conflicts
import json
from flask import Flask, request, url_for, render_template, make_response
import pdfkit

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
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
        increment_time = timedelta(hours=increment_value)
        result_time = value + increment_time
        return result_time

    @app.template_filter('strtotime')
    def strtotime(value):
        return datetime.strptime(value, '%H:%M:%S')

    @app.template_filter('timetostr')
    def timetostr(value):
        return datetime.strftime(value, '%H:%M:%S')
    
    @app.context_processor
    def utility_processor():
        def daterange(start_time, end_time):
            for n in range(int((end_time - start_time).seconds / 3600)):
                yield start_time + timedelta(hours=n)

        def match_num(result, match_start_time, match_day):
            match = 0
            for i in range(len(result)):
                if result[i]['start_time'] == match_start_time and result[i]['day'] == match_day:
                    match = match + 1
                else:
                    match = match
            return match

        def match_result(result, match_start_time, match_day):
            for i in range(len(result)):
                if result[i]['start_time'] == match_start_time and result[i]['day'] == match_day:
                    return result[i]
        
        def skip_func(match_time, skip_time):
            is_skip = 0
            for i in range(len(skip_time)):
                if match_time == skip_time[i]:
                    is_skip = 1
                    break
                else:
                    is_skip = is_skip
            return is_skip
        return dict(daterange=daterange, match_num=match_num, match_result=match_result, skip_func=skip_func)

    @app.route('/')
    def main():
        run_template = render_template("index.html")
        return run_template

    @app.route('/admin_main')
    def admin_main():
        return render_template("admin_main.html")
    
    @app.route('/admin_query', methods=["GET", "POST"])
    def admin_query():
        run_template = render_template("admin_query.html")
        return run_template

    @app.route('/admin_query_result/<selected_term>/', methods=["GET", "POST"])
    def admin_query_result(selected_term):
        global result_to_pdf
        global result_template
        if selected_term == 'all_courses':
            result_to_pdf = get_admin_db()
        else:
            result_to_pdf = get_term_db(selected_term)
        # TODO make next and previous page when too many results
        result_template = render_template(
            "admin_query_result_pdf.html", courses_info=result_to_pdf)
        run_template = render_template(
            "admin_query_result.html", courses_info=result_to_pdf)
        return run_template
    
    @app.route('/export_pdf')
    def export_pdf():
        # use pdfkit to directly change html from jinja to pdf after removing the buttons
        config = pdfkit.configuration(
            wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        css = ['timetable-system/static/query_result_pdf.css']
        # TODO page split if too many data
        doc = pdfkit.from_string(result_template, False, configuration=config, css=css)
        response = make_response(doc)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=course_information.pdf'
        return response

    @app.route('/admin_delete', methods=["GET", "POST"])
    def admin_delete():
        if delete_course_ids is None:
            all_courses = get_admin_db()
            run_template = render_template("admin_delete.html", all_courses=all_courses)
        else:
            delete_course_ids = request.form.get("delete_course")
            # delete_course_ids should be a list
            delete_admin_db(delete_course_ids)
            delete_course_info = get_course_by_id(delete_course_ids)
            run_template = render_template("admin_delete_success.html", delete_courses = delete_course_info)
        return run_template

    @app.route('/admin_update_main', method=["GET"])
    def admin_update_main():
        run_template = render_template("admin_update_main.html")

    @app.route('/admin_update', methods=["GET", "POST"])
    def admin_update():
        number_of_courses_t = request.form.get("no_courses_t")
        if number_of_courses_t is not None:
            global num_of_course_t
            num_of_course_t = int(number_of_courses_t)
            run_template = render_template(
                "admin_update.html", number_course=num_of_course_t)
        else:
            run_template = render_template("admin_update.html")
        return run_template

    @app.route('/course_results', methods=["GET", "POST"])
    def course_results():
        initial_data = []
        for i in range(num_of_course_t):
            course_temp_t = request.form.get("course_t " + str(i+1))
            class_code_temp_t = request.form.get("class_t " + str(i+1))
            term_temp_t = request.form.get("term_t " + str(i+1))
            instructor_temp_t = request.form.get("instructor_t " + str(i+1))
            time_temp_t = request.form.get("time_t " + str(i+1))
            course_nature_temp_t = request.form.get("course_nature_t " + str(i+1))
            initial_data_temp = {'course': course_temp_t, 'class_code': class_code_temp_t, 'term': term_temp_t, 'instructor': instructor_temp_t, 'timeslot': time_temp_t, 'course_nature': course_nature_temp_t}
            initial_data.append(initial_data_temp)
        exist_result = get_exist_course_db(initial_data)
        all_data = get_admin_db()
        #find exist data, temp update (replace exist_data by initial_data), temp insert (insert initial_data to all_data), check temp conflicts
        if all_data != []:
            for in_data in initial_data:
                for a in range(len(all_data)):
                    if all_data[a]['course'] == in_data['course'] and all_data[a]['class_code'] == in_data['class_code'] and all_data[a]['term'] == in_data['term']:
                        all_data[a] = in_data
                        match = 0
                    else:
                        match = 1
                if match == 0:
                    continue
                elif match == 1:
                    all_data.append(in_data)
        else:
            all_data = initial_data
        conflict_list_temp = check_course_conflicts(all_data)
        if conflict_list_temp == []:
            if len(exist_result) > 0:
                insert_data = []
                update_data = []
                for i_data in initial_data:
                    for e_data in exist_result:
                        if i_data['course'] == e_data['course'] and i_data['class_code'] == e_data['class_code'] and i_data['term'] == e_data['term']:
                            update_data.append(i_data)
                        else:
                            insert_data.append(i_data)
                update_db(update_data)
                insert_db(insert_data)
                # TODO make next and previous page when too many results
                run_template = render_template(
                    "success.html", update_courses=initial_data)
            elif len(exist_result) == 0:
                insert_db(initial_data)
                # TODO make next and previous page when too many results
                run_template = render_template(
                    "success.html", update_courses=initial_data)
        else:
            run_template = render_template(
                "course_conflicts.html", conflicts_list=conflict_list_temp)
        return run_template

    @app.route('/student', methods=["GET", "POST"])
    #receive data from form
    def student():
        global term
        term = request.form.get("term")
        number_of_courses = request.form.get("no_courses")
        if number_of_courses is not None:
            global num_of_course
            num_of_course = int(number_of_courses)
            run_template = render_template("student.html", number_course=num_of_course, term=term)
        else:
            run_template = render_template("student.html")
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
        conflict_list = check_conflicts(res, course)
        start_time_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        def daterange(start_time, end_time):
            for n in range(int((end_time - start_time).seconds / 3600)):
                yield start_time + timedelta(hours=n)
        
        day_start_time = datetime.strptime("08:30:00", "%H:%M:%S")
        day_end_time = datetime.strptime("18:30:00", "%H:%M:%S")
        ttb_range = daterange(day_start_time, day_end_time)

        if conflict_list == []:
            run_template = render_template(
                "timetable.html", days=start_time_list, initialtime=day_start_time, timeRange=ttb_range, result=res, endtime=day_end_time)
        else:
            str_conflict_list = []
            for c in conflict_list:
                str_c = json.dumps(', '.join(c)).replace('"', '')
                str_conflict_list.append(str_c)
            run_template = render_template(
                "conflicts.html", conflicts_list=str_conflict_list)
        return run_template

    return app
