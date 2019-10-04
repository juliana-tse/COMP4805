import sqlite3
import mysql.connector
from .settings import host, user, password, database
import json

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db(self, term, course, class_code):
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    mycursor = db.cursor()
    query = "SELECT * FROM `19/20 COMP Course Timetable` WHERE term=%s and course_code=%s and class_section=%s"
    mycursor.execute(query, (term, course, class_code))
    myresult = mycursor.fetchall()
    result = json.dumps(myresult, default=myconverter)
    return result