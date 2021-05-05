# Flask-SQLAlchemy Catering Website
Used Flask and SQLAlchemy to create an interactive website for a hypothetical catering company to manage events and assign staff. 

## Details:
There are three types of users: the company owner account, the company staff accounts, and registered customer accounts. Customers can request events on given days or cancel their previously scheduled events, staff can sign up to work scheduled events, and the owner can see a complete summary of all scheduled events, as well as who is working them. Events are limited to one per day, and each event required three staff members to run it.

Customers can make their own accounts at will. Staff accounts are created by the owner. The owner's login information is hard-coded into the Flask app for ease of testing. 

All users and events are stored in a SQLite database, stored in `catering.db`.

All necessary software packages are included in `requirements.txt`.

The app can be run as follows:
* set the `FLASK_APP` environment variable to `catering.py`
* initialize the database with `flask initdb`
* spin up the app with `flask run` 