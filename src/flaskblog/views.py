from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        # Handle the exception appropriately
        # For example, you can log the exception or return an error page
        # Here, we'll just raise it again to propagate the exception
        raise e


@views.route('/about')
def about():
    return render_template('about.html', title='About')


@views.route('/users_dashboard')
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

