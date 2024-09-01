from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('users.login.html', title='Login')


@views.route('/about')
def about():
    return render_template('about.html', title='About')


@views.route('/users_dashboard')
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@views.route('/admin-home')
def admin_home():
    return render_template('admin/home.html', title='Admin Home')

@views.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin/admin_dashboard.html', title='Admin Dashboard')
