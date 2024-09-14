from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from src.flaskblog.models import Post, User

from ..flaskblog.users.logger import logger

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html", title="Landing Page")


@views.route("/about")
def about():
    return render_template("about.html", title="About")


@views.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", title="Home", posts=posts)


@views.route("/user/<string:username>")
def user_posts(username):
    try:
        logger.info("Enter into user_posts function.")
        if not current_user.is_authenticated:
            return redirect(url_for("users.login"))

        page = request.args.get("page", 1, type=int)
        user = User.query.filter_by(username=username).first_or_404()
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        logger.info("Exited into user_posts function.")
        return render_template("users_posts.html", title="User Posts", user=user, posts=posts)
    except Exception as e:
        logger.error(f"An error occurred while fetching user posts: {e}")
        return redirect(url_for("users.login"))


@views.route("/users_dashboard")
def dashboard():
    try:
        logger.info("Enter into dashboard function.")
        if not current_user.is_authenticated:
            return redirect(url_for("users.login"))

        page = request.args.get("page", 1, type=int)
        user = User.query.filter_by(username=current_user.username).first_or_404()
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        logger.info("Exited into dashboard function.")
        return render_template("dashboard.html", title="Dashboard", posts=posts, user=user)
    except Exception as e:
        logger.error(f"An error occurred while fetching dashboard: {e}")
        return redirect(url_for("users.login"))


@views.route("/admin-home")
def admin_home():
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))

    return render_template("admin/home.html", title="Admin Home")


@views.route("/admin-dashboard")
def admin_dashboard():
    try:
        logger.info("Enter into admin_dashboard function.")
        if not current_user.is_authenticated:
            return redirect(url_for("users.login"))

        page = request.args.get("page", 1, type=int)
        user = User.query.filter_by(username=current_user.username).first_or_404()
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        logger.info("Exited into admin_dashboard function.")
        return render_template(
            "admin/admin_dashboard.html",
            title="Admin Dashboard",
            posts=posts,
            user=user,
        )
    except Exception as e:
        logger.error(f"An error occurred while fetching admin dashboard: {e}")
        return redirect(url_for("users.login"))
