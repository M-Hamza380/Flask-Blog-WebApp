import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    SECRET_KEY = "ZainX"
    DB_NAME = "/sql-alchemy/database.db"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

