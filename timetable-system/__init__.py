import os
import mysql.connector
import json
import datetime

from flask import Flask


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

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    @app.route('/')
    def data():
        def get_db():
            db = mysql.connector.connect(
                host="sophia.cs.hku.hk",
                user="h3537222",
                passwd="juliana5",
                database="h3537222"
            )

            mycursor = db.cursor()

            mycursor.execute("SELECT * FROM `19/20 COMP Course Timetable`")

            myresult = mycursor.fetchall()

            result = json.dumps(myresult, default=myconverter)
            return result

        res = get_db()

        return res
        for x in res:
            print(x)

    return app
