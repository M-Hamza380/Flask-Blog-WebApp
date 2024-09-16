import os

from dotenv import dotenv_values

config = dotenv_values(".env")


class Config:
    SECRET_KEY = config.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = config.get("SECURITY_PASSWORD_SALT")
    MAIL_DEFAULT_SENDER = config.get("MAIL_DEFAULT_SENDER")
    DB_NAME = config.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
