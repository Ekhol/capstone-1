from email.mime import image
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

########################## Pinned Drinks Model ###################################


class Pinned(db.Model):
    """Joining table to connect pinned drinks to the user that pinned them"""

    __tablename__ = 'pinned'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'))

    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id', ondelete='CASCADE'), unique=True)


########################## Initialize DB #########################################

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
