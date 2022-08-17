from app import db
from models import User, Recipe

db.drop_all()
db.create_all()

user1 = User(

    username="test",
    email="test@test.com",
    password="testing"
)

recipe1 = Recipe(

    name="test",
    ingredients="test",
    instructions="test, test, test",
    has_alcohol=True,
    glass_type="Old Fashioned",
    is_public=False
)

db.session.commit()
