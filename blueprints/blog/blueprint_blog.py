"""Handles the blog functionality of the website."""

from cmath import inf
import os
import datetime
from flask import Blueprint, render_template, request, session, url_for, redirect
from tinydb import TinyDB, Query

BLUEPRINT_BLOG = Blueprint('blog', __name__, template_folder='templates')

@BLUEPRINT_BLOG.route('/blog')
@BLUEPRINT_BLOG.route('/blog/<title>')
def view_post(title=None):
    """Main blog route. Displays posts based on a title or the most recent one.
    """

    # Open the database
    db = TinyDB('db.json')
    post_table = db.table('posts')

    # If the title is specified, try to show that post.
    if title is not None:
        post = post_table.get(Query().title == title.title())
        if post is not None:
            post_num = post['post_number']
        else:
            return render_template("404.html")

    else:
        # By default, show the latest post.
        if post_table:
            post_num = max(p['post_number'] for p in post_table.all())
        else:
            post_num = 0

    # Get the post dict
    post = post_table.get(Query().post_number == post_num)
    prev_title, next_title = get_surrounding_titles(post_num)

    first_title = get_first_post()

    try:
        if post is not None:
            file_path = BLUEPRINT_BLOG.root_path + "/posts/" + post['filename']
            with open(file_path, 'r') as f:
                post['content'] = f.read().split('\n')

    except FileNotFoundError:
        # Missing the file but it is found in the database.
        return render_template("500.html")

    return render_template("blog.html",
                           post=post,
                           next_title=next_title,
                           prev_title=prev_title,
                           first_title=first_title)

@BLUEPRINT_BLOG.route('/all')
def view_all_posts():
    """Displays all posts in one page."""
    #TODO: Make functional

    return render_template("all_posts.html")

@BLUEPRINT_BLOG.route('/create_post', methods=['GET', 'POST'])
def post_creator():
    """Creates a post based on request information or displays the post creator.
    """

    if 'user' not in session:
        return redirect(url_for('login.view_login', route='blog.create_post'))

    if request.method == 'POST':
        add_post(request.form['title'], request.form['content'])
        return redirect(url_for("blog.view_post"))

    return render_template("post_creator.html")

@BLUEPRINT_BLOG.route('/delete_post', methods=['POST'])
def post_deleter():
    """Deletes a post based on it's name."""
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

    # Post number should always increase.
    # Only time it doesn't is if the most recent post gets removed.
    if post_table:
        post_number = max(post['post_number'] for post in post_table.all()) + 1
    else:
        post_number = 0

    date = datetime.datetime.now()
    formatted_date = "{m}/{d}/{y}".format(m=date.month, d=date.day, y=date.year)

    filename = str(title) + ".txt"
    post_query = Query()
    if post_table.get(post_query.title == title.title()) is not None:
        print("HOW")
        raise ValueError("Duplicate title not allowed!")

    # TODO: Implement subjects and icon.
    subject = "Projects"
    icon = ''

    post_table.insert({'filename': filename,
                       'title': title.title(),
                       'date': formatted_date,
                       'author': 'Nick Jarvis',
                       'subject': subject,
                       'icon': icon,
                       'post_number': post_number})

    with open(BLUEPRINT_BLOG.root_path+"/posts/"+filename, 'w') as f:
        f.write(text)

def remove_post(title: str):
    """Searches for a post with the supplied title and deletes it if it finds it.

    Raises FileNotFoundError if post with title not found
    """

    db = TinyDB('db.json')
    post_table = db.table('posts')

    post_query = Query()
    post = post_table.get(post_query.title == title.title())
    if post is not None:
        fname = post['filename']
        post_table.remove(post_query.title == title.title())
        os.remove(BLUEPRINT_BLOG.root_path+"/posts/"+fname)
        return

    else:
        raise FileNotFoundError("No post with title: \"%s\" found" % title)

def get_post_title(post_num: int):
    """Grabs the title of a post by grabbing the text between the h2 tags"""

    db = TinyDB('db.json')
    post_table = db.table('posts')
    post_query = Query()

    post = post_table.get(post_query.post_number == post_num)
    if post is not None:
        return post['title']

    return None

def get_surrounding_titles(post_num: int):
    """Grabs the titles of the post previous to and after a given post
    (defined by it's post number).

    Returns a tuple in the form (previous title, next title), with None
    for either if they are not found.
    """

    prev_title = get_post_title(post_num-1)
    next_title = get_post_title(post_num+1)

    return (prev_title, next_title)

def get_first_post() -> str:
    db = TinyDB('db.json')
    post_table = db.table('posts')

    post_num = min([post.get('post_number', inf) for post in post_table.all()])
    title = get_post_title(post_num)

    return title