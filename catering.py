'''
    Jacob Diefes
    Project 2
    CS 1520
    3/25/21

    Website for managing a catering company, using Python, Flask, SQLAlchemy, and the Flask-SQLAlchemy extension.
'''

import os
from flask import Flask
from models import db


#init app
app = Flask(__name__)


#config
app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = 'this is a dev key',
    USERNAME = 'owner',
    PASSWORD = 'pass',

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')
))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


#cli commands
@app.cli.command('initdb')
def initdb_command():
    db.create_all()
    print("Database initialized")

@app.route("/")
def test():
    return "test"

if __name__ == "__main__":
    app.run()