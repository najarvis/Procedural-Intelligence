"""Main file for Procedural Intelligence Website.

    Copyright (c) 2018 - Nick Jarvis
"""
import os
import datetime
from flask import Flask, render_template, redirect, url_for, send_from_directory

from blueprints.blog.blueprint_blog import BLUEPRINT_BLOG
from blueprints.login.blueprint_login import BLUEPRINT_LOGIN
from blueprints.gallery.blueprint_gallery import BLUEPRINT_GALLERY
from blueprints.game.blueprint_game import BLUEPRINT_GAME
from blueprints.datastore.blueprint_datastore import BLUEPRINT_DATA
from blueprints.wheel.blueprint_wheel import BLUEPRINT_WHEEL
from blueprints.tools.blueprint_tools import BLUEPRINT_TOOLS

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
FLASK_APP.register_blueprint(BLUEPRINT_DATA)
FLASK_APP.register_blueprint(BLUEPRINT_WHEEL)
FLASK_APP.register_blueprint(BLUEPRINT_TOOLS)

FLASK_APP.config['DEBUG'] = True

@FLASK_APP.route('/')
def default():
    """Main page route"""
    return render_template("index.html")
    # return redirect(url_for('blog.view_post'))

@FLASK_APP.route('/projects')
def projects():
    """Projects page route"""
    return render_template("projects.html")

@FLASK_APP.route('/about')
def about():
    """About page route"""
    return render_template("about.html")

@FLASK_APP.route('/contact')
def contact():
    """Contact page route."""
    return render_template("contact.html")

@FLASK_APP.route('/special')
def special_creator():
    """Special route I created for a tool."""
    return render_template("special_creator.html")

@FLASK_APP.route('/lw-next-show')
def next_show():
    """Special route for another tool."""
    return render_template("show.html")

@FLASK_APP.route('/jarvis-resume')
def download_resume():
    """Sends the user my resume"""
    return send_from_directory('static/other', 'NickJarvisResume.pdf')

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

@FLASK_APP.route('/can-jarvis-play-siege')
def jarvis_siege():
    central = datetime.timezone(offset=datetime.timedelta(hours=-5))
    now = datetime.datetime.now(tz=central)
    now_format = now.strftime("%I:%M")
    template_str = "It is currently {curr} Central time, can Jarvis play?: {verdict}"
    if now.hour >= 17:
        verdict = "Maybe!"
    else:
        verdict = "Probably not :("

    return render_template("jarvis_siege.html", siege=template_str.format(curr=now_format, verdict=verdict))

if __name__ == "__main__":
    FLASK_APP.run(host='0.0.0.0')
