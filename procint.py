import os
from flask import Flask, render_template, redirect, url_for, session

from blueprints.blog.blueprint_blog import blueprint_blog
from blueprints.login.blueprint_login import blueprint_login
from blueprints.gallery.blueprint_gallery import blueprint_gallery
from blueprints.game.blueprint_game import blueprint_game

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

app.secret_key = os.environ['SECRET_KEY']

app.register_blueprint(blueprint_blog)
app.register_blueprint(blueprint_login)
app.register_blueprint(blueprint_gallery)
app.register_blueprint(blueprint_game)

@app.route('/')
def default():
    return redirect(url_for('blog.view_blog'))

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/special')
def special_creator():
    return render_template("special_creator.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(413)
def page_not_found(e):
    return render_template("413.html", e=e), 413

if __name__ == "__main__":
    app.run(host='0.0.0.0')

