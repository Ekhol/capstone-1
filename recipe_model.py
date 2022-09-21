from email.mime import image
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class Recipe(db.Model):

    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    has_alcohol = db.Column(db.Boolean, default=True, nullable=False)
    glass_type = db.Column(db.String, nullable=False)
    image_url = db.Column(db.Text, nullable=True,
                          default="/static/stock_bar.jpg")

    """This is determined by an authorized user and moves it into public view when True"""
    is_public = db.Column(db.Boolean, default=False, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User')

    def __repr__(self):
        return f"<Name = {self.name}, Ingredients = {self.ingredients}, Instructions = {self.instructions}>"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
