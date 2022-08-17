from flask import Flask, redirect, render_template, session, g, flash, request
from flask_debugtoolbar import DebugToolbarExtension
import os
import json

from models import db, connect_db, User, Recipe

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pocket-cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route("/")
def root():

    return redirect("/home")


############################ Homepage and Public View ############################

@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def login(user):

    session[CURR_USER_KEY] = user.id


def logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/home')
def homepage():

    return render_template("homepage.html")
