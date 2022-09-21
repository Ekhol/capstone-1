from crypt import methods
from flask import Flask, redirect, render_template, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import os
import json
import requests

from user_model import db, connect_db, User
from recipe_model import db, connect_db, Recipe
from pinned_model import db, connect_db, Pinned
from forms import RegistrationForm, LoginForm
from user_route import user_route
from recipe_route import recipe_route
from search_route import search_route

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.register_blueprint(user_route)
app.register_blueprint(recipe_route)
app.register_blueprint(search_route)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///pocket-cocktails')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


DB_URL = 'http://www.thecocktaildb.com/api/json/v1/1'


@app.route("/")
def root():

    return redirect("/home")


############################ Homepage and Public View ############################

@app.route('/home')
def getRandomCocktail():
    res = requests.get(f'{DB_URL}/random.php').json()
    drinkJSON = res["drinks"]
    drink = drinkJSON[0]
    return render_template("homepage.html", drink=drink)


@app.route("/new-account")
def make_acc():

    return render_template('users/no_account.html')


############################ User Creation/Login/Logout ############################

@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    session[CURR_USER_KEY] = user.id


def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                profile_picture=form.image_url.data or User.profile_picture.default.arg,
            )
            db.session.commit()
        except IntegrityError:
            flash("Username is already taken", 'danger')
            return render_template('users/register.html', form=form)
        do_login(user)
        return redirect("/")
    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            do_login(user)
            return redirect("/")
        flash("Invalid login", "danger")
    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    do_logout()
    return redirect("/login")

############################ CocktailDB Display ############################


@app.route('/recipes/cdb/<int:recipe_id>')
def cdb_details(recipe_id):

    res = requests.get(f'{DB_URL}/lookup.php?i={recipe_id}').json()
    drinkJSON = res["drinks"]
    drink = drinkJSON[0]

    ingredients_to_extract = {'strIngredient1', 'strIngredient2', 'strIngredient3', 'strIngredient4', 'strIngredient5', 'strIngredient6', 'strIngredient7',
                              'strIngredient8', 'strIngredient9', 'strIngredient10', 'strIngredient11', 'strIngredient12', 'strIngredient13', 'strIngredient14', 'strIngredient15'}

    measurements_to_extract = {'strMeasure1', 'strMeasure2', 'strMeasure3', 'strMeasure4', 'strMeasure5', 'strMeasure6', 'strMeasure7',
                               'strMeasure8', 'strMeasure9', 'strMeasure10', 'strMeasure11', 'strMeasure12', 'strMeasure13', 'strMeasure14', 'strMeasure15'}

    ingredients = [value for key,
                   value in drink.items() if key in ingredients_to_extract]

    measurements = [value for key,
                    value in drink.items() if key in measurements_to_extract]

    return render_template("/cdb-recipes/details.html", drink=drink, ingredients=ingredients, measurements=measurements)
