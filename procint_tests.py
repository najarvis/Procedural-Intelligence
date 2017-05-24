"""
I HAVE FINALLY MADE NON-LEGACY CODE
"""

import os
import unittest
import procint
import tempfile
from io import BytesIO

class ProcintTestCase(unittest.TestCase):

    def setUp(self):
        procint.app.config['TESTING'] = True
        self.app = procint.app.test_client()
        self.handle = None

    def tearDown(self):
        if self.handle is not None:
            os.close(self.handle)

    def login(self, username, password):
        """Log in the test using the given username and password. If a test needs to be logged in simply call
        this first."""

        login_data = dict(username=username,
                          password=password)
        return self.app.post('/login', data=login_data, follow_redirects=True)

    def login_successfully(self):
        return self.login(os.environ['USERNAME'], os.environ['PASSWORD'])

    def test_default(self):
        """Test to see if the default page redirects to the blog"""
        rv = self.app.get('/', follow_redirects=True)
        assert b'<h2 class="blog-post-title">' in rv.data

    def test_blog(self):
        rv = self.app.get('/blog')
        assert b'<h2 class="blog-post-title">' in rv.data

    def test_post_nums(self):
        rv = self.app.get('/blog/3/0')
        assert rv.data.count(b'<h2 class="blog-post-title">') == 3

    def test_login(self):
        # TODO: Check for an error message like 'incorrect login credentials'.
        rv = self.login('admin', 'password') # Check incorrect login just redirects back to login page.
        assert b'<input class="form-control" type="text" name="username" placeholder="Username">' in rv.data

        rv = self.login_successfully()
        assert b'<h2 class="blog-post-title">' in rv.data

    def test_add_remove_post(self):
        self.login_successfully()

        num_posts = len(os.listdir('blueprints/blog/templates/posts/'))
        data = dict(title="TEST_POST",
                    content="THIS IS A TEST POST")
        rv = self.app.post('/create_post', data=data, follow_redirects=True)

        assert b'<h2 class="blog-post-title">TEST_POST</h2>' in rv.data
        assert len(os.listdir('blueprints/blog/templates/posts/')) == num_posts + 1

        self.app.post('/delete_post', data=dict(post_title="TEST_POST"))

        assert len(os.listdir('blueprints/blog/templates/posts/')) == num_posts

    def test_upload(self):
        """Test uploading a file"""
        self.login_successfully()

        num_files = len(os.listdir('static/images'))
        self.handle, filename = tempfile.mkstemp()

        rv = self.app.post('/upload',
                           data={
                               'file': (BytesIO(b'my file contents'), 'hello_world.txt')
                           },
                           follow_redirects=True)

        assert len(os.listdir('static/images')) == num_files + 1

        os.remove('static/images/hello_world.txt')
        assert len(os.listdir('static/images')) == num_files

if __name__ == "__main__":
    unittest.main()
