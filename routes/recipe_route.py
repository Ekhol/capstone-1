from flask import redirect, render_template, g, flash, Blueprint, request
from models import db, Recipe, User, Pinned
from forms import RecipeForm

recipe_route = Blueprint('recipe_route', __name__, template_folder='templates')


@recipe_route.route('/recipes')
def list_recipes():

    search = request.args.get('q')

    if not search:
        recipes = Recipe.query.all()
    else:
        recipes = Recipe.query.filter(Recipe.name.like(f"%{search}%")).all()

    return render_template('recipes/index.html', recipes=recipes)


@recipe_route.route('/recipes/submit', methods=['GET', 'POST'])
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


@recipe_route.route('/recipes/<int:recipe_id>')
def recipe_details(recipe_id):

    recipe = Recipe.query.get_or_404(recipe_id)
    pinned = Pinned.query.filter(Pinned.recipe_id == recipe_id)

    if recipe.is_public or g.user.id == recipe.author_id or g.user.is_authorized:

        return render_template("recipes/details.html", recipe=recipe, pinned=pinned)

    else:

        flash("Access unauthorized.", "danger")
        return redirect("/")


@recipe_route.route('/recipes/<int:recipe_id>/publish', methods=["GET", "POST"])
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


@recipe_route.route('/recipes/<int:recipe_id>/private', methods=["GET", "POST"])
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


@recipe_route.route('/recipes/<int:recipe_id>/delete', methods=["GET", "POST"])
def delete_recipe(recipe_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()

    return redirect(f"/user/{g.user.id}")


@recipe_route.route("/recipes/<int:recipe_id>/pin")
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
