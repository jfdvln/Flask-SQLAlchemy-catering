'''
    Jacob Diefes
    Project 2
    CS 1520
    3/25/21

    Website for managing a catering company, using Python, Flask, SQLAlchemy, and the Flask-SQLAlchemy extension.
'''

'''
    NOTES [delete later]
    to set host and port,
        FLASK_APP='fl01_hello.py' flask run -h localhost -p 8000
        etc.
    
'''

import os
from flask import Flask, render_template, flash, url_for, session, g, request, redirect
from models import db, User, Event #and other tables


#init app
app = Flask(__name__)


#config
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',   #not really needed
    USERNAME='owner',
    PASSWORD='pass',

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')
))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


#cli commands
@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    print("Database initialized")

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(user_id = session['user_id']).first()

@app.route("/", methods=['GET', 'POST'])
def home():
    ''' home page, default view to show schedule? '''
    #insert schedule here from db
    #do some handling based on whether user is logged in or not
    error = None

    if (db.session.query(User).filter_by(username=app.config['USERNAME'])).first() is None:
        # add the owner to the db if not already there (just makes things easier)
        db.session.add(
            User(app.config['USERNAME'], app.config['PASSWORD'], 'owner'))
        db.session.commit()

    events = Event.query.filter_by().all()  #just grab every scheduled event

    if g.user is not None:
        if g.user.type == 'owner':
            #display list of all scheduled events
            print('Welcome, Owner')
        else:
            print('Welcome,', g.user.username)  

    if request.method == 'POST':
        event = Event.query.filter_by(date = request.form['date']).first()
        if event is not None:
            error = 'That date is not available. Please try again.'
        else:
            flash('Event scheduled successfully!')
            db.session.add(Event(request.form['event_name'], request.form['date'], g.user.username, None, None, None))
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('home.html', events = events, error = error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' log user in '''
    if g.user:
        return redirect(url_for('home'))
    error = None

    if request.method == 'POST':
        #look in table of user  
        user = User.query.filter_by(username = request.form['username']).first()
        #print(db.session.query(User).filter_by().first())
        if (user is None) or (user.password != request.form['password']):
            error = 'Invalid username or password.' #because "security"

        else:
            flash('Login successful!')
            session['user_id'] = user.user_id
            session['logged_in'] = True
            #print(session['user_id'])
            return redirect(url_for('home'))
    
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    ''' log user out '''
    flash('Logout successful.')
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('home'))


@app.route('/new_staff', methods=['GET', 'POST'])
def new_staff():
    ''' owner may register new staff accounts '''
    if g.user.type != 'owner':
        return redirect(url_for('home'))   #redirect if not correct permission
    error = None

    if request.method == 'POST':
        user = User.query.filter_by(username = request.form['username']).first()
        eflag = False
        if user is not None:
            error = 'Username already taken. Please try again.'
            eflag = True
        if request.form['password'] != request.form['password2']:
            error = 'Passwords must match. Please try again.'
            eflag = True
        
        if eflag == False:
            flash('New staff account created.')
            db.session.add(User(request.form['username'], request.form['password'], 'staff'))
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('new_staff.html', error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' register a new customer account '''
    if g.user:
        flash('Must be logged out to create a new account.')
        return redirect(url_for('home'))
    error = None

    if request.method == 'POST':
        user = User.query.filter_by(username = request.form['username']).first()
        eflag = False
        if user is not None:
            error = 'Username already taken. Please try again.'
            eflag = True
        if request.form['password'] != request.form['password2']:
            error = 'Passwords must match. Please try again.'
            eflag = True
        
        if eflag == False:
            flash('New customer account created. You have been logged in.')
            db.session.add(User(request.form['username'], request.form['password'], 'customer'))
            db.session.commit()
            session['user_id'] = User.query.filter_by(username = request.form['username']).first().user_id
            session['logged_in'] = True
            return redirect(url_for('home'))

    return render_template('register.html', error = error)

@app.route('/<event>/cancel')
def cancel_event(event):
    ''' event cancellation '''
    if (not g.user) or (g.user.type != 'customer'):
        return redirect(url_for('home'))
    if g.user.username != Event.query.filter_by(event_name = event).first().cust_name:
        return redirect(url_for('home'))
    
    to_delete = Event.query.filter_by(event_name = event).first()
    db.session.delete(to_delete)
    db.session.commit()

    flash('Event {} deleted.'.format(event))
    return redirect(url_for('home'))

@app.route('/<event>/work')
def work(event):
    ''' staff sign up to work a scheduled event '''
    if (not g.user) or (g.user.type != 'staff'):
        return redirect(url_for('home'))
    
    to_work = Event.query.filter_by(event_name = event).first()
    if (to_work.staff1 is None):
        flash('Signed up to work {}.'.format(event))
        to_work.staff1 = g.user.username
        db.session.commit()
        return redirect(url_for('home'))
    elif (to_work.staff2 is None):
        flash('Signed up to work {}.'.format(event))
        to_work.staff2 = g.user.username
        db.session.commit()
        return redirect(url_for('home'))
    elif (to_work.staff3 is None):
        flash('Signed up to work {}.'.format(event))
        to_work.staff3 = g.user.username
        db.session.commit()
        return redirect(url_for('home'))
    else:
        flash('Error: no available work slots.')

    return redirect(url_for('home'))

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(user_id = session['user_id']).first()
            #this will return the first (and should be only match) to this user id

if __name__ == "__main__":
    app.run()
