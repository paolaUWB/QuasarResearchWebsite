# TITLE: __init__
# CONTRIBUTORS: Kathleen Guinee, Audrey Nguyen
# DESCRIPTION: Runs the website

import os
import pymysql
import csv
import sys

from flask import Flask
from flask import render_template, url_for, g, request, send_file, flash, redirect
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required

from app.config import APP_TMP, Config

load_dotenv()

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

port = os.environ.get('MYSQL_DATABASE_PORT')

# DATABASE METHODS

# Connects to the database
# If won't connect properly to MYSQL, change the port number (e.g. port=12345) to match yours
def connect_db():
    port = os.environ.get('MYSQL_DATABASE_PORT')
    #Remote mysql server
    if(port):
        # print("world")
        return pymysql.connect(
            host = 'vergil.u.washington.edu', user = 'root', password = os.environ.get('MYSQL_DATABASE_PASSWORD'),
            database = 'quasarWebsite_db', autocommit = True, charset = 'utf8mb4',port=32445,
            cursorclass = pymysql.cursors.DictCursor) 
    #local mysql server
    else:
        # print("hello")
        return pymysql.connect(
            host = 'localhost', user = 'root', password = os.environ.get('MYSQL_DATABASE_PASSWORD'),
            database = 'quasarWebsite_db', autocommit = True, charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor) 

# Gets the database
def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

# Closes the database
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# imports routes
from app import routes

# creates a shell context that adds the database instance and models to the shell session
from app import models, app, db
from app.models import User
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

# Runs the app
if __name__ == '__main__':
    app.debug = True #Enables debug mode when uncommented
    app.run()