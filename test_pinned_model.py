from app import app
from unittest import TestCase
from models import db, User, Recipe, Pinned
import os

os.environ['DATABASE-URL'] = "postgresql:///pocket-cocktails-test"

db.create_all()


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

    def test_pinned_model(self):

        recipe = Recipe(name="test", ingredients="stuff",
                        instructions="do it", has_alcohol=True, glass_type="Rocks", author_id=self.user_id)

        pinned = Pinned(user_id=1, recipe_id=1)

        self.recipe_id = 1
        recipe.id = self.recipe_id

        db.session.add(recipe)
        db.session.commit()

        db.session.add(pinned)
        db.session.commit()

        self.assertEqual(pinned.user_id, 1)
        self.assertEqual(pinned.recipe_id, 1)
