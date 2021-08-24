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

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

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

    def test_add_message(self):
        """Can user add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Hello', html)
            
    def test_view_msg_logged_in(self):
        """Tests viewing a message while logged in"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("/messages/new", data={"text": "Hello"})
            msg = Message.query.one()
            resp = c.get(f'/messages/{msg.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('Hello', html)
    
    def test_invalid_message(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get('/messages/43463325622346542266432')
            self.assertEqual(resp.status_code,404)
    
            
    def test_loggedout_msg_add(self):
        """Tests add message functions while logged out"""
        with self.client as c:
            resp = c.get('/messages/new', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized', html)
            resp = c.post("/messages/new", data={"text": "Hello2"}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized', html)
    
    def test_delete_msg(self):
        """Tests deleting message while logged in and logged out"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.post("/messages/new", data={"text": "DELETE_ME"}, follow_redirects=True)
            msg=Message.query.one()
            resp = c.post(f'/messages/{msg.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('DELETE_ME', html)
            resp = c.post("/messages/new", data={"text": "DELETE_ME_AGAIN"}, follow_redirects=True)
            msg=Message.query.one()
            resp = c.get('/logout')
            resp = c.post(f'/messages/{msg.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized', html)
    
    def test_other_user_msg(self):
        """Tests attempting to delete another user's messages"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser2",
                                    image_url=None)
            db.session.commit()
            test_msg = Message(text='TEST_MSG', user_id=testuser2.id)
            db.session.add(test_msg)
            db.session.commit()
            resp = c.post(f'/messages/{test_msg.id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized', html)
            
            
        
        
            
            
        
            
