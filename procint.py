import os
from flask import Flask, render_template, redirect, url_for, session

from blueprints.blog.blueprint_blog import blueprint_blog
from blueprints.login.blueprint_login import blueprint_login
from blueprints.gallery.blueprint_gallery import blueprint_gallery

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = os.environ['SECRET_KEY']

app.register_blueprint(blueprint_blog)
app.register_blueprint(blueprint_login)
app.register_blueprint(blueprint_gallery)

@app.route('/')
def default():
    return redirect(url_for('blog.view_blog'))

@app.route('/special')
def special_creator():
    return render_template("special_creator.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')

