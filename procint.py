import os

from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route('/')
def default():
    return redirect(url_for('blog', num_per_page=1, page=0))
    return render_template("index.html")

@app.route('/blog')
@app.route('/blog/<num_per_page>/<page>')
def blog(num_per_page=5, page=0):
    posts = get_blog_posts(int(num_per_page), int(page))
    return render_template("blog.html", posts=posts)

@app.route('/special')
def special_creator():
    return render_template("special_creator.html")

def get_blog_posts(num_to_show=5, page=0):
    """Grabs files like 'post-1.html', 'post-23.html' and so on and returns num_to_show worth of them on a specific page."""
    
    # Returns all the numbers on the posts
    posts_nums = sorted([int(i.split('.html')[0].split('-')[-1]) for i in os.listdir("templates/posts/")])
    
    # Returns the posts requested
    posts = ["post-"+str(i)+".html" for i in posts_nums[-num_to_show-(num_to_show * page):len(posts_nums)-(num_to_show * page)]]
    posts.reverse()
    return posts

if __name__ == "__main__":
    app.run(host='0.0.0.0')

