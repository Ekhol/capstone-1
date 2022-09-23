import email
from app import app
from unittest import TestCase
from models import db, User
import os

os.environ['DATABASE-URL'] = "postgresql:///pocket-cocktails-test"

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        user1 = User.register(username="Test1", email="test1@testing.com",
                              password="password", profile_picture="/static/stock_bar.jpg")
        user_id1 = 1
        user1.id = user_id1

        user2 = User.register(username="Test2", email="test2@testing.com",
                              password="password2", profile_picture="/static/stock_bar.jpg")
        user_id2 = 2
        user2.id = user_id2

        db.session.commit()

        user1 = User.query.get(user_id1)
        user2 = User.query.get(user_id2)

        self.user1 = user1
        self.user2 = user2

        self.user_id1 = user_id1
        self.user_id2 = user_id2

        self.client = app.test_client()

    def tearDown(self):
        result = super().tearDown()
        db.session.rollback()
        return result

    def test_user_model(self):

        user = User(email="test@test.com",
                    username="testing", password="hash_password")
        user_id = 420
        user.id = user_id

        db.session.add(user)
        db.session.commit()

        self.assertEqual(len(user.recipes), 0)

    def test_register(self):

        user = User.register(username="testing_again", email="test3@testing.com",
                             password="tessssst", profile_picture="/static/stock_bar.jpg")
        user_id = 10
        user.id = user_id
        db.session.commit()

        user = User.query.get(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testing_again")
        self.assertEqual(user.email, "test3@testing.com")
        self.assertNotEqual(user.password, "tessssst")

    def test_authenticate(self):

        user = User.authenticate(self.user1.username, "password")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user_id1)

    def test_bad_username(self):
        self.assertFalse(User.authenticate("a;sldkfj;as", "password"))

    def test_bad_password(self):
        self.assertFalse(User.authenticate(self.user1.username, "wrong"))
