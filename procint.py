import os

from flask import Flask, render_template, redirect
from blueprints.blueprint_blog import blog_page

app = Flask(__name__)
app.register_blueprint(blog_page)

@app.route('/')
def default():
    return redirect(url_for('blog', num_per_page=1, page=0))
    return render_template("index.html")

@app.route('/special')
def special_creator():
    return render_template("special_creator.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

