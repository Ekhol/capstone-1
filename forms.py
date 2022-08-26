from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, URL


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('Profile Picture (Optional)')


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             Length(min=6), DataRequired()])


class RecipeForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    has_alcohol = BooleanField('Alcoholic', validators=[
        DataRequired()], default="checked")
    glass_type = StringField('Glass type', validators=[DataRequired()])
    image_url = StringField('Optional Image URL')
    instructions = TextAreaField('Instructions', validators=[DataRequired()])

############### TO DO: create password authentication before the edit user form ####


class EditUserForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio')
    image_url = StringField('Image URL')
    password = PasswordField('Current Password', validators=[
                             Length(min=6), DataRequired()])


class SearchForm(FlaskForm):

    search = StringField('', validators=[DataRequired()])
