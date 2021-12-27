"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgres://postgres:postgres@postgres:5432/warblertest"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()
        
    
    def tearDown(self):
        """Clean up any fouled DB transactions"""
        db.session.rollback()
    
    def test_home_page(self):
        """Test home page while not logged in"""
        with self.client as c:
            resp = c.get('/')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("What's Happening?", html)
    def test_login_page(self):
        """Tests login page"""
        with self.client as c:
            resp = c.get('/login')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Welcome back.', html)
    def test_user_login(self):
        """Tests logging in user"""
        with self.client as c:
            resp = c.post('/login', data ={
                'username' : 'testuser',
                'password' : 'testuser'                
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Hello, testuser!', html)
            resp = c.get(f'/users/{self.testuser.id}')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Following', html)
            self.assertIn('Messages', html)
            self.assertIn('Followers', html)
    def test_invalid_login(self):
        """Tests logging in user"""
        with self.client as c:
            resp = c.post('/login', data ={
                'username' : 'testuser225',
                'password' : 'testuser225'}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Invalid credentials.', html)
        
    def test_user_page_loggedout(self):
        """Tests user page while logged out"""
        with self.client as c:
            resp = c.get(f'/users/{self.testuser.id}/following')
            self.assertEqual(resp.status_code, 302)
            resp = c.get(f'/users/{self.testuser.id}/following', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Access unauthorized', html)
    def test_signup_page(self):
        """Tests signup page"""
        with self.client as c:
            resp = c.get(f'/signup')
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Join Warbler today.', html)
            resp = c.post('/signup', data={'username':'test_user2', 'password' : 'test_password', 'email' : 'test_email2@email.com'})
            self.assertEqual(resp.status_code, 302)
            resp = c.post('/signup', data={'username':'test_user3', 'password' : 'test_password', 'email' : 'test_email3@email.com'}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('test_user3', html)
    def test_logout_page(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get('/logout')
            self.assertEqual(resp.status_code, 302)
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Goodbye testuser', html)
        with self.client as c:
            resp = c.get('/logout', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please log in', html)
            
        
            
            
        
            
    
    
            
        
        
            
            
            
            
            
        