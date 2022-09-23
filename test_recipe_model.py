from app import app
from unittest import TestCase
from models import db, User, Recipe
import os

os.environ['DATABASE-URL'] = "postgresql:///pocket-cocktails-test"


class UserModelTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.user_id = 1
        user = User.register(username="testing", email="test@testing.com",
                             profile_picture="/static/stock_bar.jpg", password="testing")
        user.id = self.user_id
        db.session.commit()

        self.user = User.query.get(self.user_id)

        self.client = app.test_client()

    def tearDown(self):
        result = super().tearDown()
        db.session.rollback()
        return result

    def test_recipe_model(self):

        recipe = Recipe(name="test", ingredients="stuff",
                        instructions="do it", has_alcohol=True, glass_type="Rocks", author_id=self.user_id)

        db.session.add(recipe)
        db.session.commit()

        self.assertEqual(len(self.user.recipes), 1)
        self.assertEqual(self.user.recipes[0].name, "test")
