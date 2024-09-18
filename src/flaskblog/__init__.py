from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from ..flaskblog.config import Config
from ..flaskblog.users.logger import logger

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    try:
        logger.info("Enter into create_app function to create flask app.")

        app.config.from_object(config_class)

        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)

        with app.app_context():
            from flaskblog.users.admin.routes import admin_bp
            from flaskblog.users.errors.handlers import errors
            from flaskblog.users.main.routes import users
            from flaskblog.users.posts.routes import posts

            from .views import views

            app.register_blueprint(views, url_prefix="/")
            app.register_blueprint(admin_bp, url_prefix="/admin")
            app.register_blueprint(users, url_prefix="/")
            app.register_blueprint(posts, url_prefix="/")
            app.register_blueprint(errors)

        logger.info("Exited into create_app function.")
        return app
    except Exception as e:
        logger.error(f"An error occurred while creating the app: {e}")
        raise e


def create_database(app):
    try:
        logger.info("Enter into create_database function.")

        with app.app_context():
            db.create_all()
            logger.info(f"Database created at: {app.config['SQLALCHEMY_DATABASE_URI']}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
