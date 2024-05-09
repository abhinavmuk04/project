from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=30)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user:
            raise ValidationError('Username is taken.')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=30)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired(), Length(min=1, max=100)])
    submit = SubmitField('Search')

class SearchNew(FlaskForm):
    search_query = StringField('Query', validators=[InputRequired(), Length(min=1, max=100)])
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(min=5, max=500)])
    submit = SubmitField('Enter Comment')
