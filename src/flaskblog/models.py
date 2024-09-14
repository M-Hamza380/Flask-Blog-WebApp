from datetime import datetime, timedelta

from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin

from src.flaskblog import db, login_manager


@login_manager.user_loader
def user_load(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("users.login"))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(90), unique=True, nullable=False)
    image_file = db.Column(db.String(90), nullable=False, default="default.jpg")
    password = db.Column(db.String(90), nullable=False)
    password_reset_count = db.Column(db.Integer, nullable=False, default=0)
    last_reset_request = db.Column(db.DateTime, default=None)
    posts = db.relationship("Post", backref="author", lazy=True)

    def can_reset_password(self):
        if self.last_reset_request is None:
            return True

        one_day_ago = datetime.now() - timedelta(days=1)

        if self.last_reset_request < one_day_ago:
            self.password_reset_count = 0
            return True

        return self.password_reset_count < 3

    def increment_reset_count(self):
        if self.last_reset_request is None or self.last_reset_request < datetime.now() - timedelta(days=1):
            self.password_reset_count = 1
        else:
            self.password_reset_count += 1

        self.last_reset_request = datetime.now()

    def __repr__(self) -> str:
        return f"User: ('{self.username}', '{self.email}', '{self.image_file}') "


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Role: ('{self.name}')"


class UserAdmin(ModelView):
    column_list = ("id", "username", "email", "image_file", "posts", "role")
    column_searchable_list = ("username", "email", "posts", "role")
    column_filters = ("username", "email")
    form_excluded_columns = ("password", "posts")


class RoleAdmin(ModelView):
    column_list = ("id", "name")
    form_excluded_columns = ("users",)


class PostAdmin(ModelView):
    column_list = ("id", "title", "date_posted", "author")
    column_searchable_list = ("title", "content")
    column_filters = ("title", "date_posted")
    form_excluded_columns = ("user_id",)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Post: ('{self.title}', '{self.date_posted}')"
