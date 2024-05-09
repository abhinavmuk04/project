from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Review
from .forms import RegistrationForm, LoginForm, SearchForm, ReviewForm
from . import bcrypt, db
from .lastfm_client import LastFmClient
from .config import LASTFM_API_KEY
lastfm_client = LastFmClient(api_key=LASTFM_API_KEY)

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    print("User authenticated:", current_user.is_authenticated)
    if current_user.is_authenticated:
        top_albums = lastfm_client.get_top_albums()
        return render_template('home.html', title='Home', albums=top_albums)
    return render_template('home.html', title='Home')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        user.save()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))




searchy = Blueprint('searchy', __name__)

@searchy.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search_query.data
        results = lastfm_client.search_album(query)
    return render_template('search_results.html', title='Search Results', form=form, results=results)

@searchy.route('/searchar', methods=['GET', 'POST'])
@login_required
def searchar():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search_query.data
        results = lastfm_client.search_art(query)
    return render_template('searchartist.html', title='Search Results', form=form, results=results)



