import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin

from src.flaskblog.users.logger import logger
from src.flaskblog.config import Config


app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    try:
        logger.info('Enter into create_app function to create flask app.')

        app.config.from_object(config_class)

        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)

        with app.app_context():
            from .views import views
            from ..flaskblog.users.admin.routes import admin_bp
            from src.flaskblog.users.main.routes import users
            from ..flaskblog.users.posts.routes import posts
            from src.flaskblog.users.errors.handlers import errors

            app.register_blueprint(views, url_prefix='/')
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(users, url_prefix='/')
            app.register_blueprint(posts, url_prefix='/')
            app.register_blueprint(errors)

        logger.info('Exited into create_app function the app is successfully created.')
        return app
    except Exception as e:
        logger.error(f'An error occurred while creating the app: {e}')
        raise e

def create_database(app, config_class=Config):
    try:
        logger.info('Enter into create_database function and create the database.')
        db_path = os.path.abspath(config_class.DB_NAME)
        db_dir = os.path.dirname(db_path)

        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f'Created directory for database: {db_dir}')
        
        if not os.path.exists(db_path):
            with app.app_context():
                db.create_all()
                logger.info(f'Database created at: {db_path}')
        else:
            logger.info(f'Database already exists at: {db_path}')
    except Exception as e:
        logger.error(f'An error occurred while creating the database: {e}')
        raise
