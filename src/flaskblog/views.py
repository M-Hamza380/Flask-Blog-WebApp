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


