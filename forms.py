from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FieldList, BooleanField
from wtforms.validators import DataRequired, Email, Length, URL


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('Profile Picture (Optional)')


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class IngredientForm(FlaskForm):

    amount = StringField('Amount', validators=[DataRequired()])
    ingredient = StringField('Ingredient', validators=[DataRequired()])


class RecipeForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    ingredient_amount = FieldList(IngredientForm(
        'Ingredients', validators=[DataRequired()]))
    has_alcohol = BooleanField('Alcoholic', validators=[
                               DataRequired()], default="checked")
    glass_type = StringField('Glass type', validators=[DataRequired()])
    image_url = StringField('Optional Image URL', validators=[URL()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
