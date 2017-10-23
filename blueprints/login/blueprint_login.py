import os
import bcrypt
from tinydb import TinyDB, Query
from flask import Blueprint, render_template, request, session, url_for, redirect

blueprint_login = Blueprint('login', __name__, template_folder='templates')
blueprint_logout = Blueprint('logout', __name__, template_folder='templates')

# TODO: Have a 'last page' variable so logging in doesn't always take you to the blog page.
@blueprint_login.route('/login', methods=['GET', 'POST'])
def view_login():

    if request.method == 'POST':
        if is_valid_login(username=request.form['username'],
                          password=request.form['password']):

            session['user'] = request.form['username'].lower()

        else:
            return render_template('login.html')

        return redirect(url_for('blog.post_creator'))

    return render_template('login.html')

@blueprint_login.route('/logout')
def view_logout():
    del session['user']
    return redirect(url_for('blog.view_post'))

def is_valid_login(username: str, password: str):

    # Open the database
    db = TinyDB('db.json')
    users_table = db.table('users')

    user = users_table.get(Query().username == username)
    if user is not None:
        return bcrypt.checkpw(password.encode(), user['password'].encode())
        
    return False
