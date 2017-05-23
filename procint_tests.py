"""
I HAVE FINALLY MADE NON-LEGACY CODE
"""

import os
import unittest
import procint
import tempfile

class ProcintTestCase(unittest.TestCase):

    def setUp(self):
        procint.app.config['TESTING'] = True
        self.app = procint.app.test_client()

    def tearDown(self):
        pass

    def login(self, username, password):
        """Log in the test using the given username and password. If a test needs to be logged in simply call
        this first."""

        login_data = dict(username=username,
                          password=password)
        return self.app.post('/login', data=login_data)

    def login_successfully(self):
        return login(os.environ['USERNAME'], os.environ['PASSWORD'])

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
        rv = login('najarvis', 'thisisnotthepassword')
        assert b'<input class="form-control" type="text" name="username" placeholder="Username">' in rv.data

        rv = login_successfully()
        assert b'<h2 class="blog-post-title">' in rv.data

    def test_add_remove_post(self):
        login_successfully()

        num_posts = len(os.listdir('blueprints/blog/templates/posts/'))
        data = dict(title="TEST_POST",
                    content="THIS IS A TEST POST")
        rv = self.app.post('/create_post', data=data)

        assert b'<h2 class="blog-post-title">TEST_POST</h2>' in rv.data
        assert len(os.listdir('blueprints/blog/templates/posts/')) == num_posts + 1

        self.app.post('/delete_post', data=dict(post_title="TEST_POST"))

        assert len(os.listdir('blueprints/blog/templates/posts/')) == num_posts

if __name__ == "__main__":
    unittest.main()
