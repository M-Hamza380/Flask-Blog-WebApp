from flask import url_for, redirect
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from itsdangerous import URLSafeTimedSerializer as Serializer
from datetime import datetime

from src.flaskblog import db, login_manager, app

@login_manager.user_loader
def user_load(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('users.login'))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(90), unique=True, nullable=False)
    image_file = db.Column(db.String(90), nullable=False, default='default.jpg')
    password = db.Column(db.String(90), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=300):
        secret_key = app.config.get('SECRET_KEY')
        if secret_key is None:
            raise ValueError('SECRET_KEY is not set in app.config')
        s = Serializer(secret_key, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self) -> str:
        return f"User: ('{self.username}', '{self.email}', '{self.image_file}') "

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Role: ('{self.name}')"

class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email', 'image_file', 'earned_coins', 'purchased_coins', 'total_coins', 'role', )
    column_searchable_list = ('username', 'email', 'books', 'role')
    column_filters = ('username', 'email')
    form_excluded_columns = ('password',)

class RoleAdmin(ModelView):
    column_list = ('id', 'name')
    form_excluded_columns = ('users',)  

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Post: ('{self.title}', '{self.date_posted}')"
    
