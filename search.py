from flask import redirect, render_template, flash, Blueprint, request
from models import Recipe
from forms import SearchForm
from app import DB_URL
import requests

search_route = Blueprint('search_route', __name__, template_folder='templates')


@search_route.route('/search', methods=["GET", "POST"])
def search_home():

    form = SearchForm()
    if request.method == 'POST':
        return search_results(form)

    return render_template("search/search.html", form=form)


@search_route.route('/results')
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


@search_route.route('/recipes/cdb', methods=["GET", "POST"])
def cdb_home():
    form = SearchForm()
    if request.method == 'POST':
        return cdb_results(form)

    return render_template("/cdb-recipes/home.html", form=form)


@search_route.route('/recipes/cdb_results')
def cdb_results(search):

    search_string = search.data['search']
    res = requests.get(f'{DB_URL}/search.php?s={search_string}').json()
    drinkJSON = res["drinks"]
    drink = drinkJSON[0]

    return render_template("/cdb-recipes/results.html", drink=drink)
