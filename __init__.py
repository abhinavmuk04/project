from flask import Flask
from .extensions import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)
    from .routes import searchy
    app.register_blueprint(searchy)

    from .models import User
    login_manager.login_view = "main.login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(pk=user_id).first()

    return app
