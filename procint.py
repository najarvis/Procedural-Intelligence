from flask import Flask, render_template, redirect, url_for
from blueprints.blog.blueprint_blog import blueprint_blog

app = Flask(__name__)
app.register_blueprint(blueprint_blog)

@app.route('/')
def default():
    return redirect(url_for('blog.view_blog', num_per_page=1, page=0))

@app.route('/special')
def special_creator():
    return render_template("special_creator.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

