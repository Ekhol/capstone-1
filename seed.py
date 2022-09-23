from app import db
from models import Pinned, Recipe, User

db.drop_all()
db.create_all()

user1 = User(

    id=1,
    username="Admin",
    email="testing@testing.com",
    password="testing",
    is_authorized=True,

)

recipe1 = Recipe(

    id=1,
    name="test",
    ingredients="test",
    instructions="test, test, test",
    has_alcohol=True,
    glass_type="Old Fashioned",
    is_public=True
)

pinned1 = Pinned(

    user_id=1,
    recipe_id=1

)
db.session.commit()
