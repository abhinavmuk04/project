from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()
