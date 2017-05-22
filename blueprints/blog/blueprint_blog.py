import os
import datetime
from flask import Blueprint, render_template, request, session, url_for, redirect

blueprint_blog = Blueprint('blog', __name__, template_folder='templates')

@blueprint_blog.route('/blog')
@blueprint_blog.route('/blog/<num_per_page>/<page>')
def view_blog(num_per_page=1, page=0):
    posts = get_blog_posts(int(num_per_page), int(page))
    max_num = max([int(i.split('.html')[0].split('-')[-1]) for i in os.listdir(blueprint_blog.root_path+"/templates/posts/")])

    prev_title, next_title  = get_surrounding_titles(max_num - int(num_per_page) * int(page))
    
    return render_template("blog.html", posts=posts, per_page=int(num_per_page), page_num=int(page), next_title=next_title, prev_title=prev_title)

@blueprint_blog.route('/create_post', methods=['GET', 'POST'])
def post_creator():
    if 'user' not in session:
        return redirect(url_for('login.view_login'))
 
    if request.method == 'POST':
        add_post(request.form['title'], request.form['content'])
        return render_template(url_for("view_blog", num_per_page=1, page=0))

    return render_template("post_creator.html")

def add_post(title: str, text: str):
    """Create a post-*.html file and save it based on input fields."""

    posts_nums = sorted([int(i.split('.html')[0].split('-')[-1]) for i in os.listdir(blueprint_blog.root_path+"/templates/posts/")])
    new_post_num = int(posts_nums[-1]) + 1 # Grab the highest post number and add one to it. It will be the number for the new post.

    # Create a string for the date
    d = datetime.datetime.now()
    date_string = "Posted on: {m}/{d}/{y}".format(m=d.month, d=d.day, y=d.year)

    with open(blueprint_blog.root_path+"/templates/posts/post-"+str(new_post_num)+'.html', 'w') as f:
        paragraphs = text.split('\n')
        
        # Add in the title and date
        final_text = '<h2 class="blog-post-title">' + title + '</h2>'
        final_text += '<p class="blog-post-meta">' + date_string + '</p>' 

        # Add in all the paragraphs
        final_text += '<p>'
        final_text += '</p><p>'.join(paragraphs)
        final_text += '</p>'
        
        f.write(final_text)

def get_post_title(post_num: int):
    """Grabs the title of a post by grabbing the text between the h2 tags"""

    try:
        with open(blueprint_blog.root_path+'/templates/posts/post-'+str(post_num)+'.html', 'r') as f:
            s = f.read()
            title = s[s.find('<h2 class="blog-post-title">')+len('<h2 class="blog-post-title">'):s.find('</h2>')] # This grabs the text between the <h2> and </h2> tags.
            return title

    except FileNotFoundError:
        return None

def get_surrounding_titles(post_num: int):
    """Grabs the titles of the post previous to and after a given post (defined by it's post number).
    
    Returns a tuple in the form (previous title, next title), with None for either if they are not found.
    """

    prev_title = get_post_title(post_num-1)
    next_title = get_post_title(post_num+1)
    
    return (prev_title, next_title)

def get_blog_posts(num_to_show=5, page=0):
    """Grabs files like 'post-1.html', 'post-23.html' and so on and returns num_to_show worth of them on a specific page."""

    # Returns all the numbers on the posts
    posts_nums = sorted([int(i.split('.html')[0].split('-')[-1]) for i in os.listdir(blueprint_blog.root_path+"/templates/posts/")])

    # Returns the posts requested
    posts = ["post-"+str(i)+".html" for i in posts_nums[-num_to_show-(num_to_show * page):len(posts_nums)-(num_to_show * page)]]
    posts.reverse()
    return posts

