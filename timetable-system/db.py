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

def update_db(update_data):
    db = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database
    )
    mycursor = db.cursor()
    query_t = "UPDATE `COMP Course Timetable` set timeslot=%s, instructor=%s, course_nature=%s where term=%s and course_code=%s and class_section=%s"
    for j in range(len(update_data)):
        mycursor.execute(query_t, (update_data[j]['timeslot'], update_data[j]['instructor'], update_data[j]['course_nature'], update_data[j]['term'], update_data[j]['course'], update_data[j]['class_code']))
        db.commit()
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
    mycursor.execute(query_all)
    myresult = mycursor.fetchall()
    query_result=[]
    for j in range(len(myresult)):
        result = {'term': myresult[j][2], 'course': myresult[j][0], 'class_code': myresult[j][1], 'course_nature': myresult[j][3], 'instructor': myresult[j][4], 'timeslot': myresult[j][5]}
        load_result = json.dumps(result)
        json_result = json.loads(load_result)
        query_result.append(json_result)
    return query_result

def insert_db(insert_data):
    db = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,
    database=database
    )
    mycursor = db.cursor()
    query_t = "INSERT INTO `COMP Course Timetable` (`course_code`, `class_section`, `term`, `course_nature`, `instructor`, `timeslot`) VALUES (%s, %s, %s, %s, %s, %s)"
    for j in range(len(insert_data)):
        mycursor.execute(query_t, (insert_data[j]['course'], insert_data[j]['class_code'], insert_data[j]['term'], insert_data[j]['course_nature'], insert_data[j]['instructor'], insert_data[j]['timeslot']))
        db.commit()
    return 'success'

def get_exist_course_db(initial_data):
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    mycursor = db.cursor()
    query = "SELECT * FROM `COMP Course Timetable` where term=%s and course_code=%s and class_section=%s"
    formatted_result = []
    for i in range(len(initial_data)):
        mycursor.execute(query, (initial_data[i]['term'], initial_data[i]['course'], initial_data[i]['class_code']))
        myresult = mycursor.fetchall()
        query_result=[]
        for j in range(len(myresult)):
            result = {'term': myresult[j][2], 'course': myresult[j][0], 'class_code': myresult[j][1], 'course_nature': myresult[j][3], 'instructor': myresult[j][4], 'timeslot': myresult[j][5]}
            load_result = json.dumps(result)
            json_result = json.loads(load_result)
            query_result.append(json_result)
        formatted_result = formatted_result + query_result
    return formatted_result

def get_term_db(term_data):
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    mycursor = db.cursor()
    query = "SELECT * FROM `COMP Course Timetable` where term=%s"
    mycursor.execute(query, (term_data,))
    myresult = mycursor.fetchall()
    query_result=[]
    for j in range(len(myresult)):
        result = {'term': myresult[j][2], 'course': myresult[j][0], 'class_code': myresult[j][1], 'course_nature': myresult[j][3], 'instructor': myresult[j][4], 'timeslot': myresult[j][5]}
        load_result = json.dumps(result)
        json_result = json.loads(load_result)
        query_result.append(json_result)
        print(query_result)
    return query_result
