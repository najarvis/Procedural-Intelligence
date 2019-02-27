"""Handles basic logging in / out functionality."""

import time
import uuid

import bcrypt
from tinydb import TinyDB, Query
from flask import Blueprint, render_template, request, session, url_for, redirect, jsonify

BLUEPRINT_LOGIN = Blueprint('login', __name__, template_folder='templates')

# TODO: Have a 'last page' variable so logging in doesn't always take you to the blog page.
@BLUEPRINT_LOGIN.route('/login', methods=['GET', 'POST'])
@BLUEPRINT_LOGIN.route('/login/<route>', methods=['GET', 'POST'])
def view_login(route=None):
    """Handles logging in the user.

    On a GET request, returns the login page, on a POST request, checks to see if
    the username and password are valid and attempts to log in the user."""

    if request.method == 'POST':
        if is_valid_login(username=request.form['username'],
                          password=request.form['password']):

            session['user'] = request.form['username'].lower()

            if route is None:
                return redirect(url_for('blog.post_creator'))

            return redirect(url_for(route))

        else:
            return render_template('login.html')

    return render_template('login.html')

@BLUEPRINT_LOGIN.route('/logout')
def view_logout():
    """Handles logging the user out."""
    if 'user' not in session:
        return jsonify({"status": "error", "reason": "Not logged in!"})

    del session['user']
    return redirect(url_for('blog.view_post'))

@BLUEPRINT_LOGIN.route('/create_user', methods=['POST'])
def create_user():
    """This route creates a new user. Requires a valid access code. See generate_user_code()"""

    data = request.get_json(force=True)
    if "username" not in data or "password" not in data or "code" not in data:
        return jsonify({"status": "error", "reason": "payload must include the fields: 'username', 'password', and 'code'"})

    code = data["code"]
    uname = data["username"]
    passwd = data["password"]

    code_db = TinyDB('codes.json')
    CodeQuery = Query()
    code_element = code_db.get(CodeQuery.value == code)
    if code_element is not None:
        # There is a matching code in the db
        if code_element.get("valid_until") < time.time():
            return jsonify({"status": "error", "reason": "Access code expired. Please ask for a new one."})
        
        # It is valid
        db = TinyDB('db.json')
        users_table = db.table('users')
        bcrypt_password = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
        users_table.insert({"username": uname, "password": bcrypt_password.decode(), "roles": ["user"]})

        # Remove code so it can't be used again.
        code_db.remove(CodeQuery.value == code)
        return jsonify({"status": "success"})
    
    else:
        return jsonify({"status": "Invalid code."})

@BLUEPRINT_LOGIN.route('/gen_code', methods=['GET'])
def generate_user_code():
    """This route generates a new 24 hour user code, adds it to the database, and returns it."""
    if 'user' not in session:
        return redirect(url_for('login.view_login', route='login.generate_user_code'))

    code_db = TinyDB('codes.json')
    new_code = str(uuid.uuid4())

    code_db.insert({"value": new_code, "valid_until": time.time() + (60 * 60 * 24)})
    return jsonify({"status": "success", "code": new_code})


def is_valid_login(username: str, password: str):
    """Simply returns a boolean value for if the username and password combo are valid"""

    # Open the database
    db = TinyDB('db.json')
    users_table = db.table('users')

    user = users_table.get(Query().username == username)
    if user is not None:
        return bcrypt.checkpw(password.encode(), user['password'].encode())

    return False
