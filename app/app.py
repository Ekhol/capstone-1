from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pocket-cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route("/")
def homepage():

    return redirect("/home")
