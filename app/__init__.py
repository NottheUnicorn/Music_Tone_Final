import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_pyfile('config.py', silent=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:%40Pookas69@localhost:5432/music"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret'

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
    migrate.init_app(app, db)

    from .site import site
    app.register_blueprint(site)

    from .auth import auth
    app.register_blueprint(auth)

    return app
