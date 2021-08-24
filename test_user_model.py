"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
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


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test User Model"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled DB transactions"""
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(repr(u), f'<User #{u.id}: testuser, test@test.com>')

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u2)
        db.session.commit()
        self.assertEqual(
            repr(u2), f'<User #{u2.id}: testuser2, test2@test.com>')

        u.following.append(u2)
        db.session.commit()
        self.assertEqual(u.is_following(u2), True)
        self.assertEqual(u2.is_followed_by(u), True)
        u.following.remove(u2)
        db.session.commit()
        self.assertEqual(u.is_following(u2), False)
        self.assertEqual(u2.is_followed_by(u), False)

        db.session.delete(u)
        db.session.delete(u2)
        db.session.commit()
        u3 = u.signup(u.username, u.email, u.password, u.image_url)
        db.session.commit()
        self.assertNotEqual(u.password, u3.password)
        dupe_user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        dupe_user.signup(dupe_user.username, dupe_user.email,
                         dupe_user.password, dupe_user.image_url)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        self.assertEqual(u3.authenticate(u3.username, u.password), u3)
        self.assertFalse(u3.authenticate(u2.username, u.password))
        self.assertFalse(u3.authenticate(u3.username, u2.password))
        incomplete_user1 = User(username="testuser3",
                                password="HASHED_PASSWORD3")
        db.session.add(incomplete_user1)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        incomplete_user2 = User(username="testuser4",
                                email="test4@test.com")
        db.session.add(incomplete_user2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
        incomplete_user3 = User(email="test4@test.com",
                                password="HASHED_PASSWORD4")
        db.session.add(incomplete_user3)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()
