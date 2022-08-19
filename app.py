from flask import Flask, redirect, render_template, session, g, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import os
import json

from models import db, connect_db, User, Recipe
from forms import RegistrationForm, LoginForm

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

############################ Recipe Routes ############################


@app.route('/recipes')
def list_recipes():

    search = request.args.get('q')

    if not search:
        recipes = Recipe.query.all()
    else:
        recipes = Recipe.query.filter(Recipe.name.like(f"%{search}%")).all()

    return render_template('recipes/index.html', recipes=recipes)
