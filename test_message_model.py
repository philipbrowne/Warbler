"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up any fouled DB transactions"""
        db.session.rollback()
    
    def test_message_model(self):
        
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()
        
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        
        db.session.add(u2)
        db.session.commit()
        
        m1 = Message(text='Test_Message', user_id=u.id)
        db.session.add(m1)
        db.session.commit()
        self.assertEqual(repr(m1), f'{m1}')
        self.assertEqual(m1.user, u)
        m2 = Message(text='Test_Message2', user_id=u2.id)
        db.session.add(m2)
        db.session.commit()
        u.likes.append(m2)
        db.session.commit()
        self.assertEqual(u.likes, [m2])
        u.likes.remove(m2)
        db.session.commit()
        self.assertEqual(u.likes, [])
        m3 = Message(user_id=u2.id)
        db.session.add(m3)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        m4 = Message(text='Test_Message3')
        db.session.add(m4)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        
        
        
        
        