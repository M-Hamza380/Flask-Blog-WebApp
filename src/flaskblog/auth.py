import os, secrets
from PIL import Image
from . import bcrypt, db, app
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user

from .models import User
from src.flaskblog.users.forms import LoginForm, RegistrationForm, UpdateAccountForm

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Your account has been created! You are now able to login.", category='success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f"An error occurred while registering: {str(e)}", category='error')
            db.session.rollback()
            return render_template("register.html", title='Register', form=form)
    return render_template("register.html", title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Login unsuccessful. Please check email and password', category='error')
            return render_template("login.html", title='Login', form=form)
        
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        flash("You have been logged in!", category='success')
        return redirect(next_page) if next_page else redirect(url_for('views.home'))
    
    return render_template("login.html", title='Login', form=form)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('auth.login'))
    except Exception as e:
        flash(f"An error occurred while logging out: {str(e)}", category='error')
        return redirect(url_for('views.home'))


@auth.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    return render_template('forgot_password.html')

def save_picture(form_picture):
    if form_picture is None:
        raise ValueError("Form picture cannot be None")

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_file = random_hex + f_ext
    pic_dir = os.path.join(app.root_path, 'static/profile_pics')
    pic_path = os.path.join(pic_dir, pic_file)

    try:
        os.makedirs(pic_dir, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create directory: {pic_dir}") from e

    try:
        output_size = (125, 125)
        with Image.open(form_picture) as img:
            img.thumbnail(output_size)
            img.save(pic_path)
    except OSError as e:
        raise OSError(f"Failed to save image: {pic_path}") from e

    return pic_file


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            try:
                pic_file = save_picture(form.picture.data)
            except Exception as e:
                flash(f'Error while saving the picture: {str(e)}', category='error')
                return redirect(url_for('auth.account'))
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        try:
            db.session.commit()
        except Exception as e:
            flash(f'Error while updating the account: {str(e)}', category='error')
            return redirect(url_for('auth.account'))
        flash('Your account has been updated!', category='success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    try:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    except Exception as e:
        flash(f'Error while generating the image file url: {str(e)}', category='error')
        image_file = None
    return render_template('account.html', title='Account', image_file=image_file, form=form)

