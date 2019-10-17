import sqlite3
import mysql.connector
from .settings import host, user, password, database
import json

import click
from flask import current_app, g
from flask.cli import with_appcontext

@staticmethod
def get_db(term_value, courses, class_codes):
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    mycursor = db.cursor()
    if term_value == 1:
        term = "2019-20 Sem 1"
    else:
        term = "2019-20 Sem 2"
    # query = "SELECT * FROM `19/20 COMP Course Timetable` WHERE term=%s and course_code=%s and class_section=%s"
    query = "SELECT DISTINCT term, course_code, class_section, start_time, end_time, course_title, duration, day FROM `19/20 COMP Course Timetable` where term=%s and course_code=%s and class_section=%s"
    for i in courses:
        mycursor.execute(query, (term, courses[i], class_codes[i]))
        myresult = mycursor.fetchall()
        # myresult:  obj
        for j in range(len(myresult)):
            result = {'course': myresult[j]['course'], 'class_code': myresult[j]['class_code'], 'start_time': myresult[j]['start_time'], 'end_time': myresult[j]['end_time'], 'duration': myresult[j]['duration'], 'day': myresult[j]['day']}
            formatted_result.update(result)
        # result = json.dumps(myresult, default=myconverter)
        return formatted_result
        