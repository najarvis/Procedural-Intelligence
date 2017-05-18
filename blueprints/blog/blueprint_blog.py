import os
from flask import Blueprint, render_template, request

blueprint_blog = Blueprint('blog', __name__, template_folder='templates')

@blueprint_blog.route('/blog')
@blueprint_blog.route('/blog/<num_per_page>/<page>')
def view_blog(num_per_page=5, page=0):
    posts = get_blog_posts(int(num_per_page), int(page))
    return render_template("blog.html", posts=posts)

@blueprint_blog.route('/create_post', methods=['GET', 'POST'])
def post_creator():
    
    if request.method == 'POST':
        add_post(request.form['title'], request.form['content'])

    return render_template("post_creator.html")

def add_post(title: str, text: str):
    posts_nums = sorted([int(i.split('.html')[0].split('-')[-1]) for i in os.listdir(blueprint_blog.root_path+"/templates/posts/")])
    new_post_num = int(posts_nums[-1]) + 1
    print(posts_nums)

    with open(blueprint_blog.root_path+"/templates/posts/post-"+str(new_post_num)+'.html', 'w') as f:
        paragraphs = text.split('\n')
        final_text = '<h1>'+title+'</h1>'
        final_text += '<p>'
        final_text += '</p><p>'.join(paragraphs)
        final_text += '</p>'
        f.write(final_text)


def get_blog_posts(num_to_show=5, page=0):
    """Grabs files like 'post-1.html', 'post-23.html' and so on and returns num_to_show worth of them on a specific page."""

    # Returns all the numbers on the posts
    posts_nums = sorted([int(i.split('.html')[0].split('-')[-1]) for i in os.listdir(blueprint_blog.root_path+"/templates/posts/")])

    # Returns the posts requested
    posts = ["post-"+str(i)+".html" for i in posts_nums[-num_to_show-(num_to_show * page):len(posts_nums)-(num_to_show * page)]]
    posts.reverse()
    return posts

