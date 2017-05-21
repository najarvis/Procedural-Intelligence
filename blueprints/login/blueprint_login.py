import os
from flask import Blueprint, render_template, request, session, url_for, redirect

blueprint_login = Blueprint('login', __name__, template_folder='templates')
blueprint_logout = Blueprint('logout', __name__, template_folder='templates')

@blueprint_login.route('/login', methods=['GET', 'POST'])
def view_login():

    if request.method == 'POST':
        if is_valid_login(username=request.form['username'],
                          password=request.form['password']):

            session['user'] = request.form['username'].lower()

        else:
            return render_template('login.html')

        return redirect(url_for('blog.view_blog'))

    return render_template('login.html')

@blueprint_login.route('/logout')
def view_logout():
    del session['user']
    return redirect(url_for('blog.view_blog'))

def is_valid_login(username: str, password: str):
    return username == os.environ['USERNAME'] and password == os.environ['PASSWORD']
