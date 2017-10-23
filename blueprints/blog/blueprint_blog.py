import os
import datetime
from flask import Blueprint, render_template, request, session, url_for, redirect
from flask import current_app as app
from tinydb import TinyDB, Query

blueprint_blog = Blueprint('blog', __name__, template_folder='templates')

@blueprint_blog.route('/blog')
@blueprint_blog.route('/blog/<title>')
def view_post(title=None):
    # Open the database
    db = TinyDB('db.json')
    post_table = db.table('posts')

    # If the title is specified, try to show that post.
    if title is not None:
        p = post_table.get(Query().title == title.title())
        if p is not None:
            post_num = p['post_number']
        else:
            return render_template("404.html")

    else:
        # By default, show the latest post.
        if len(post_table) > 0:
            post_num = max(p['post_number'] for p in post_table.all())
        else:
            post_num = 0

    # Get the post dict
    post = post_table.get(Query().post_number == post_num)
    prev_title, next_title  = get_surrounding_titles(post_num)

    try:
        if post is not None:
            with open(blueprint_blog.root_path + "/posts/" + post['filename'], 'r') as f:
                post['content'] = f.read().split('\n')

    except FileNotFoundError:
        # Missing the file but it is found in the database.
        return render_template("500.html")
    
    return render_template("blog.html", post=post, next_title=next_title, prev_title=prev_title)

@blueprint_blog.route('/all')
def view_all_posts():

    return render_template("all_posts.html")

@blueprint_blog.route('/create_post', methods=['GET', 'POST'])
def post_creator():
    if 'user' not in session:
        return redirect(url_for('login.view_login'))
 
    if request.method == 'POST':
        add_post(request.form['title'], request.form['content'])
        return redirect(url_for("blog.view_post"))

    return render_template("post_creator.html")

@blueprint_blog.route('/delete_post', methods=['POST'])
def post_deleter():
    if 'user' not in session:
        return redirect(url_for('login.view_login'))

    remove_post(request.form['post_title'])
    return redirect(url_for("blog.view_post"))

def add_post(title: str, text: str):
    """Create a post-*.html file and save it based on input fields.

       Each post has the following things
        * filename
        * title (Primary Key)
        * date
        * author
        * subject - TODO
        * icon (filename) - TODO
        * post_number
    """

    # Open the database
    db = TinyDB('db.json')
    post_table = db.table('posts')

    # Post number should always increase. Only time it doesn't is if the most recent post gets removed.
    if len(post_table) > 0:
        post_number = max(p['post_number'] for p in post_table.all()) + 1
    else:
        post_number = 0

    d = datetime.datetime.now()
    date = "{m}/{d}/{y}".format(m=d.month, d=d.day, y=d.year)

    filename = str(title) + ".txt"
    Post = Query()
    if post_table.get(Post.title == title.title()) is not None:
        print("HOW")
        raise ValueError("Duplicate title not allowed!")

    # TODO
    subject = "Projects"
    icon = ''

    post_table.insert({'filename': filename, 'title': title.title(), 'date': date, 'author': 'Nick Jarvis', 'subject': subject, 'icon': icon, 'post_number': post_number})

    with open(blueprint_blog.root_path+"/posts/"+filename, 'w') as f:
        f.write(text)

def remove_post(title: str):
    """Searches for a post with the supplied title and deletes it if it finds it.

    Raises FileNotFoundError if post with title not found
    """

    db = TinyDB('db.json')
    post_table = db.table('posts')

    Post = Query()
    p = post_table.get(Post.title == title.title())
    if p is not None:
        fname = p['filename']
        post_table.remove(Post.title == title.title())
        os.remove(blueprint_blog.root_path+"/posts/"+fname)
        return
    
    else:
        raise FileNotFoundError("No post with title: \"%s\" found" % title)


def get_post_title(post_num: int):
    """Grabs the title of a post by grabbing the text between the h2 tags"""
    
    db = TinyDB('db.json')
    post_table = db.table('posts')
    Post = Query()

    p = post_table.get(Post.post_number == post_num)
    if p is not None:
        return p['title']

    else:
        return None

def get_surrounding_titles(post_num: int):
    """Grabs the titles of the post previous to and after a given post (defined by it's post number).
    
    Returns a tuple in the form (previous title, next title), with None for either if they are not found.
    """

    prev_title = get_post_title(post_num-1)
    next_title = get_post_title(post_num+1)
    
    return (prev_title, next_title)
