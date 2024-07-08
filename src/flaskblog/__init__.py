import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.flaskblog.users import logger

db = SQLAlchemy()
DB_NAME = './sql-alchemy/database.db'

def create_app():
    try:
        logger.info('Enter into create_app function to create flask app.')
        app = Flask(__name__)

        # Kind of Encrpt or secure the cookies or seesion data related to our website.
        app.config['SECRET_KEY'] = "Zain-Ul-Hassan"

        db_path = os.path.abspath(DB_NAME)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
        db.init_app(app)

        from .views import views
        from .auth import auth

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        from .models import User

        logger.info('Exited into create_app function the app is successfully created.')
        return app
    except Exception as e:
        logger.error(e)
        raise e

def create_database(app):
    try:
        logger.info('Enter into create_database function and create the database.')
        db_dir = os.path.dirname(os.path.abspath(DB_NAME))
        db_path = os.path.abspath(DB_NAME)

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
        logger.error(e)
        raise e
