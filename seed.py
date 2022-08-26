from app import db
from models import User, Recipe

db.drop_all()
db.create_all()

user1 = User(

    id=1,
    username="Admin",
    email="frost.nathan1995@gmail.com",
    password="testing",
    is_authorized=True,

)

recipe1 = Recipe(

    name="test",
    ingredients="test",
    instructions="test, test, test",
    has_alcohol=True,
    glass_type="Old Fashioned",
    is_public=True
)

db.session.commit()
