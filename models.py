'''
    db models for catering.py
'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Test(db.Model):
    test = db.Column(db.Integer, primary_key = True)

    def __init__(self, test):
        self.test = test
        