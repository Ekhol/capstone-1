from crypt import methods
from flask import Flask, redirect, render_template, session, g, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import os
import json
import requests

from models import db, connect_db, User, Recipe, Pinned
from forms import RegistrationForm, LoginForm, RecipeForm, EditUserForm, SearchForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pocket-cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "12345"

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

    return render_template('uses/no_account.html')


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
            flash(f"Howdy, {user.username}!", "success")
            return redirect("/")

        flash("Invalid login", "danger")

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():

    do_logout()

    return redirect("/login")

############################ User Account Routes ############################


@app.route('/user/<int:user_id>')
def user_details(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('users/details.html', user=user)


@app.route('/user/edit', methods=['GET', 'POST'])
def edit_user():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.username.data
            user.image_url = form.image_url.data or "/static/stock_bar.jpg"
            user.bio = form.bio.data

            db.session.commit()
            return redirect(f"/user/{user.id}")

        flash("Incorrect password", "danger")

    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/user/<int:user_id>/make_admin', methods=["GET", "POST"])
def make_admin(user_id):

    user = User.query.get(user_id)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    elif g.user.id == user.id:
        user.is_authorized = True
        db.session.add(user)
        db.commit()

        return redirect("/")


@app.route("/user/delete", methods=["GET", "POST"])
def confirm_delete():

    form = LoginForm()

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            return redirect(f"/user/{user.id}/delete")

    return render_template('users/delete.html', form=form)


@app.route("/user/<int:user_id>/delete", methods=["GET", "POST"])
def delete_user(user_id):

    user = User.query.get(user_id)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    elif g.user.id == user.id or g.user.is_authorized:
        db.session.delete(user)
        db.session.commit()

        return redirect("/")


@app.route("/user/<int:user_id>/pinned")
def show_pinned(user_id):

    user = User.query.get(user_id)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    elif g.user.id == user.id:

        return render_template("users/pinned.html", user=user)


@app.route('/recipes')
def list_recipes():

    search = request.args.get('q')

    if not search:
        recipes = Recipe.query.all()
    else:
        recipes = Recipe.query.filter(Recipe.name.like(f"%{search}%")).all()

    return render_template('recipes/index.html', recipes=recipes)


@app.route('/recipes/submit', methods=['GET', 'POST'])
def new_recipe():

    if not g.user:
        flash("Must be logged in to submit a recipe", "danger")
        return redirect("/login")

    form = RecipeForm()

    if form.validate_on_submit():
        recipe = Recipe(
            name=form.name.data,
            ingredients=form.ingredients.data,
            has_alcohol=form.has_alcohol.data,
            glass_type=form.glass_type.data,
            image_url=form.image_url.data or Recipe.image_url.default.arg,
            instructions=form.instructions.data,

        )
        g.user.recipes.append(recipe)
        db.session.commit()

        return redirect(f"/recipes/{recipe.id}")

    return render_template('recipes/submit.html', form=form)


@app.route('/recipes/<int:recipe_id>')
def recipe_details(recipe_id):

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.is_public or g.user.id == recipe.author_id or g.user.is_authorized:

        return render_template("recipes/details.html", recipe=recipe)

    else:

        flash("Access unauthorized.", "danger")
        return redirect("/")


@app.route('/recipes/<int:recipe_id>/publish', methods=["GET", "POST"])
def publish_recipe(recipe_id):

    recipe = Recipe.query.get_or_404(recipe_id)

    if not g.user:
        flash("Must be recipe owner or admin to publish.", "danger")
        return redirect("/")

    elif g.user.id == recipe.author_id:
        recipe.is_public = True
        db.session.add(recipe)
        db.session.commit()

        return redirect(f"/user/{g.user.id}")

    else:
        flash("Access unauthorized.", "danger")
        return redirect("/")


@app.route('/recipes/<int:recipe_id>/private', methods=["GET", "POST"])
def make_private_recipe(recipe_id):

    recipe = Recipe.query.get_or_404(recipe_id)

    if not g.user:
        flash("Must be recipe owner or admin to make private.", "danger")
        return redirect("/")

    elif g.user.id == recipe.author_id:
        recipe.is_public = False
        db.session.add(recipe)
        db.session.commit()

        return redirect(f"/user/{g.user.id}")

    else:
        flash("Access unauthorized.", "danger")
        return redirect("/")


@app.route('/recipes/<int:recipe_id>/delete', methods=["GET", "POST"])
def delete_recipe(recipe_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()

    return redirect(f"/user/{g.user.id}")


@app.route("/recipes/<int:recipe_id>/pin")
def pin_cocktail(recipe_id):

    drink = Recipe.query.get(recipe_id)
    user = User.query.get(g.user.id)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    elif drink.is_public or g.user.id == drink.author_id:

        user.pinned.append(drink)

        db.session.add(user)
        db.session.commit()

        return redirect(f"/user/{g.user.id}/pinned")


############################ CocktailDB Routes ############################


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


@app.route('/recipes/cdb')
def cdb_home():
    form = SearchForm()

    return render_template("/cdb-recipes/home.html", form=form)

############################ Search Routes ############################


@app.route('/search', methods=["GET", "POST"])
def search_home():

    if not g.user:
        return redirect("/new-account")

    form = SearchForm()
    if request.method == 'POST':
        return search_results(form)

    return render_template("search/search.html", form=form)


@app.route('/results')
def search_results(search):

    search_string = search.data['search']
    results = Recipe.query.filter(
        Recipe.name.ilike(f"%{search_string}%")).all()

    if search_string == '':
        flash("Please Enter a Valid Search Term", "danger")
        return render_template("/search")

    if not results:
        flash('No results found')
        return redirect("/search")

    else:
        return render_template('search/results.html', results=results)
