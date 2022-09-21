from email.mime import image
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    profile_picture = db.Column(db.Text, default="/static/stock_bar.jpg")
    bio = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=False)
    pinned = db.Column(db.Integer, nullable=True)

    is_authorized = db.Column(db.Boolean, default=False, nullable=False)

    pinned = db.relationship('Recipe', secondary='pinned')

    recipes = db.relationship('Recipe')

    def __repr__(self):
        return f"<Username = {self.username}, Email = {self.email}, ID = {self.id}>"

    @classmethod
    def register(cls, username, email, password, profile_picture):

        hash_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hash_password,
            profile_picture=profile_picture,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
