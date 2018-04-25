"""Main file for Procedural Intelligence Website.

    Copyright (c) 2018 - Nick Jarvis
"""
import os
from flask import Flask, render_template, redirect, url_for

from blueprints.blog.blueprint_blog import BLUEPRINT_BLOG
from blueprints.login.blueprint_login import BLUEPRINT_LOGIN
from blueprints.gallery.blueprint_gallery import BLUEPRINT_GALLERY
from blueprints.game.blueprint_game import BLUEPRINT_GAME

UPLOAD_FOLDER = 'static/images'

FLASK_APP = Flask(__name__)

# These configs are for large image uploads.
FLASK_APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
FLASK_APP.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

FLASK_APP.secret_key = os.environ['SECRET_KEY']

FLASK_APP.register_blueprint(BLUEPRINT_BLOG)
FLASK_APP.register_blueprint(BLUEPRINT_LOGIN)
FLASK_APP.register_blueprint(BLUEPRINT_GALLERY)
FLASK_APP.register_blueprint(BLUEPRINT_GAME)

FLASK_APP.config['DEBUG'] = True

@FLASK_APP.route('/')
def default():
    """Main page route"""
    return redirect(url_for('blog.view_post'))

@FLASK_APP.route('/projects')
def projects():
    """Projects page route"""
    return render_template("projects.html")

@FLASK_APP.route('/special')
def special_creator():
    """Special route I created for a tool."""
    return render_template("special_creator.html")

@FLASK_APP.route('/lw-next-show')
def next_show():
    """Special route for another tool."""
    return render_template("show.html")

@FLASK_APP.errorhandler(404)
def page_not_found(error):
    """Basic 404 error route"""
    # TODO: Log error
    return render_template("404.html", error=error), 404

@FLASK_APP.errorhandler(413)
def entity_too_large(error):
    """Basic 413 'Entity too large' error route"""
    # TODO: Log error
    return render_template("413.html", error=error), 413

if __name__ == "__main__":
    FLASK_APP.run(host='0.0.0.0')
