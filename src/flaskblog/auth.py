from flask import Blueprint, render_template, flash, redirect, url_for

from src.flaskblog.users.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", category='success')
        return redirect(url_for('views.home'))
    return render_template("register.html", title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("You have been logged in!", category='success')
        return redirect(url_for('views.home'))
    return render_template("login.html", title='Login', form=form)


@auth.route("/logout")
def logout():
    return render_template()

@auth.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    return render_template('forgot_password.html')

