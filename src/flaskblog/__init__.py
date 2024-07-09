import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from src.flaskblog.users import logger

app = Flask(__name__)

db = SQLAlchemy()
DB_NAME = './sql-alchemy/database.db'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
login_manager.login_message_category = 'info'

def create_app():
    try:
        logger.info('Enter into create_app function to create flask app.')

        app.config['SECRET_KEY'] = "Zain-Ul-Hassan"

        db_path = os.path.abspath(DB_NAME)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
        db.init_app(app)

        with app.app_context():
            from .views import views
            from .auth import auth

            app.register_blueprint(views, url_prefix='/')
            app.register_blueprint(auth, url_prefix='/')

        logger.info('Exited into create_app function the app is successfully created.')
        return app
    except Exception as e:
        logger.error(f'An error occurred while creating the app: {e}')
        raise e

def create_database(app):
    try:
        logger.info('Enter into create_database function and create the database.')
        db_path = os.path.abspath(DB_NAME)
        db_dir = os.path.dirname(db_path)

        if not db_dir:
            raise ValueError('Invalid database path')

        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f'Created directory for database: {db_dir}')
        
        if not os.path.exists(db_path):
            with app.app_context():
                db.create_all()
                logger.info(f'Database created at: {db_path}')
        else:
            logger.info(f'Database already exists at: {db_path}')
    except FileNotFoundError as e:
        logger.error(f'File not found: {e}')
        raise
    except Exception as e:
        logger.error(f'An error occurred while creating the database: {e}')
        raise
