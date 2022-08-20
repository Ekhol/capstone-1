from crypt import methods
from flask import Flask, redirect, render_template, session, g, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import os
import json

from models import db, connect_db, User, Recipe
from forms import RegistrationForm, LoginForm, RecipeForm, EditUserForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pocket-cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "12345"

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route("/")
def root():

    return redirect("/home")


############################ Homepage and Public View ############################

@app.route('/home')
def homepage():

    return render_template("homepage.html")

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

############################ Recipe Routes ############################

################ TO DO: Make only publicly available recipes viewable ###
################ - Add search function for the cocktailDB recipes #######


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

    if not g.user:
        flash("Must be logged to view this recipe", "danger")
        return redirect("/")

    elif recipe.is_public or g.user.id == recipe.author_id or g.user.is_authorized:

        return render_template("/recipes/details.html", recipe=recipe)

    else:

        flash("Access unauthorized.", "danger")
        return redirect("/")
