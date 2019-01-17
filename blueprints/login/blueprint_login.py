"""Handles basic logging in / out functionality."""

import bcrypt
from tinydb import TinyDB, Query
from flask import Blueprint, render_template, request, session, url_for, redirect

BLUEPRINT_LOGIN = Blueprint('login', __name__, template_folder='templates')

# TODO: Have a 'last page' variable so logging in doesn't always take you to the blog page.
@BLUEPRINT_LOGIN.route('/login', methods=['GET', 'POST'])
def view_login():
    """Handles logging in the user.

    On a GET request, returns the login page, on a POST request, checks to see if
    the username and password are valid and attempts to log in the user."""

    if request.method == 'POST':
        if is_valid_login(username=request.form['username'],
                          password=request.form['password']):

            session['user'] = request.form['username'].lower()

        else:
            return render_template('login.html')

        return redirect(url_for('blog.post_creator'))

    return render_template('login.html')

@BLUEPRINT_LOGIN.route('/logout')
def view_logout():
    """Handles logging the user out."""

    del session['user']
    return redirect(url_for('blog.view_post'))

def is_valid_login(username: str, password: str):
    """Simply returns a boolean value for if the username and password combo are valid"""

    # Open the database
    db = TinyDB('db.json')
    users_table = db.table('users')

    user = users_table.get(Query().username == username)
    if user is not None:
        return bcrypt.checkpw(password.encode(), user['password'].encode())

    return False
