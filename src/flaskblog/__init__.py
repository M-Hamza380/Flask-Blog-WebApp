from flask import Flask

from src.flaskblog.users import logger

def create_app():
    try:
        logger.info('Enter into create_app function to create flask app.')
        app = Flask(__name__)

        # Kind of Encrpt or secure the cookies or seesion data related to our website.
        app.config['SECRET_KEY'] = "Zain-Ul-Hassan"

        logger.info('Exited into create_app function the app is successfully created.')
        return app
    except Exception as e:
        logger.error(e)
        raise e


