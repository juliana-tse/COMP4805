import sqlite3
import mysql.connector
from .settings import host, user, password, database
import json
import datetime

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db(term_value, courses, class_codes):
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    mycursor = db.cursor()
    if term_value == "1":
        term = "2019-20 Sem 1"
    else:
        term = "2019-20 Sem 2"
    query = "SELECT DISTINCT term, course_code, class_section, start_time, end_time, course_title, duration, day FROM `19/20 COMP Course Timetable` where term=%s and course_code=%s and class_section=%s"
    formatted_result = []
    for i in range(len(courses)):
        mycursor.execute(query, (term, courses[i], class_codes[i]))
        myresult = mycursor.fetchall()
        query_result=[]
        for j in range(len(myresult)):
            result = {'term': myresult[j][0], 'course_code': myresult[j][1], 'class_code': myresult[j][2], 'start_time': str(myresult[j][3]), 'end_time': str(myresult[j][4]), 'course_title': myresult[j][5], 'duration': str(myresult[j][6]), 'day': myresult[j][7]}
            load_result = json.dumps(result)
            json_result = json.loads(load_result)
            query_result.append(json_result)
        formatted_result = formatted_result + query_result
    return formatted_result

def update_db(times, instructors, course_natures, terms, courses, class_codes):
    db = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database
    )
    mycursor = db.cursor()
    query_t = "UPDATE `COMP Course Timetable` set timeslot=%s and instructor=%s and course_nature=%s where term=%s and course_code=%s and class_section=%s"
    for j in range(len(courses_t)):
        mycursor.execute(query_t, (time_t[j], instructor_t[j], course_nature_t[j], term_t[j], courses_t[j], class_codes[j]))
        db.commit()
        mycursor.close()
    return 'success'

def get_teacher_db():
    db = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database
    )
    mycursor = db.cursor()
    query_all = "SELECT * FROM `COMP Course Timetable`"
    mycursor.execute(query)
    result = mycursor.fetchall()

    format_result = []
    return format_result


def insert_db(times, instructors, course_natures, terms, courses, class_codes):
    db = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database
    )
    mycursor = db.cursor()
    query_t = "INSERT INTO `COMP Course Timetable` (`course_code`, `class_section`, `term`, `course_nature`, `instructor`, `timeslot`) VALUES (%s, %s, %d, %s, %s, %s, %s)"
    for j in range(len(courses_t)):
        mycursor.execute(query_t, (courses_t[j], class_codes[j],
                                   term_t[j], course_nature_t[j], instructor_t[j], time_t[j]))
        db.commit()
        mycursor.close()
    return 'success'
