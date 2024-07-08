from . import db, login_manager
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def user_load(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(90), unique=True, nullable=False)
    image_file = db.Column(db.String(90), nullable=False, default='default.jpg')
    password = db.Column(db.String(90), nullable=False)
    
    def __repr__(self) -> str:
        return f"Welcome User: ('{self.username}', '{self.email}', '{self.image_file}')"

