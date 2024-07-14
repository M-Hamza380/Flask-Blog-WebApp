import os
from dotenv import dotenv_values

config = dotenv_values(".env")

class Config:
    SECRET_KEY = config.get("SECRET_KEY")
    DB_PATH = "site.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    