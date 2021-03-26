'''
    db models for catering.py
'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    #not expected to store password securely yet (ick)
    password = db.Column(db.String, nullable = False)
    type = db.Column(db.String, nullable = False)

    def __init__(self, username, password, type):
        #don't init user_id, have it be generated
        self.username = username
        self.password = password
        self.type = type

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key = True)
    event_name = db.Column(db.String, nullable = False)
    date = db.Column(db.String, nullable = False)  #this will use html's date input, formatted as 'yyyy-mm-dd'
    cust_name = db.Column(db.String, db.ForeignKey('users.user_id'), nullable=False)
    staff1 = db.Column(db.String, db.ForeignKey('users.user_id'))
    staff2 = db.Column(db.String, db.ForeignKey('users.user_id'))
    staff3 = db.Column(db.String, db.ForeignKey('users.user_id'))

    def __init__(self, event_name, date, cust_name, staff1, staff2, staff3):
        self.event_name = event_name
        self.date = date
        self.cust_name = cust_name
        self.staff1 = staff1
        self.staff2 = staff2
        self.staff3 = staff3

    def __repr__(self):
        return '<Event name: {}, Event date: {}, Customer name: {}, Staff: {}, {}, {}'.format(self.event_name, self.date, self.cust_name, self.staff1, self.staff2, self.staff3)

