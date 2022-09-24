from flask import redirect, render_template, g, flash, Blueprint
from models import db, User, Pinned
from forms import LoginForm, EditUserForm
from routes.recipe_route import delete_recipe

user_route = Blueprint('user_route', __name__, template_folder='templates')


@user_route.route('/user/<int:user_id>')
def user_details(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('users/details.html', user=user)


@user_route.route('/user/edit', methods=['GET', 'POST'])
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


@user_route.route('/user/<int:user_id>/make_admin', methods=["GET", "POST"])
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


@user_route.route("/user/delete", methods=["GET", "POST"])
def confirm_delete():

    form = LoginForm()

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user.username == "testing":
        flash("Cannot delete the test account.", "danger")
        return redirect("/")

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            return redirect(f"/user/{user.id}/delete")

    return render_template('users/delete.html', form=form)


@user_route.route("/user/<int:user_id>/delete", methods=["GET", "POST"])
def delete_user(user_id):

    user = User.query.get(user_id)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    elif g.user.username == "testing":
        flash("Cannot delete the test account.", "danger")
        return redirect("/")

    elif g.user.id == user.id or g.user.is_authorized:
        for recipe in user.recipes:
            delete_recipe(recipe.id)
        db.session.delete(user)
        db.session.commit()

        return redirect("/")


@user_route.route("/user/<int:user_id>/pinned")
def show_pinned(user_id):

    user = User.query.get(user_id)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    elif g.user.id == user.id:

        return render_template("users/pinned.html", user=user)
