import sqlite3
import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    db = mysql.connector.connect(
        host="sophia.cs.hku.hk",
        user="h3537222",
        passwd="juliana5",
        database="h3537222"
    )

    mycursor = db.cursor()

    mycursor.execute("SELECT * FROM 19/20 COMP Course Timetable")

    myresult = mycursor.fetchall()

    return myresult