from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user

from src.flaskblog.models import Post, User

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html', title='Landing Page')


@views.route('/about')
def about():
    return render_template('about.html', title='About')

@views.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', posts=posts)

@views.route('/user/<string:username>')
def user_posts(username):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('users_posts.html', title='User Posts', user=user, posts=posts)

@views.route('/users_dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('dashboard.html', title='Dashboard', posts=posts, user=user)

@views.route('/admin-home')
def admin_home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    return render_template('admin/home.html', title='Admin Home')

@views.route('/admin-dashboard')
def admin_dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('admin/admin_dashboard.html', title='Admin Dashboard', posts=posts, user=user)
