import os
from dataclasses import dataclass
from dotenv import dotenv_values

config = dotenv_values(".env")

@dataclass(frozen=True)
class Config:
    SECRET_KEY: str = config['SECRET_KEY']
    DB_PATH: str = config['DB_PATH']
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{config['DB_PATH']}"
    MAIL_SERVER: str = 'smtp.googlemail.com'
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD: str = os.environ.get('EMAIL_PASS')

