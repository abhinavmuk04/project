from flask_login import UserMixin
from .extensions import db

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    album_name = db.StringField(required=True)
    review = db.StringField(required=True, min_length=5, max_length=500)
