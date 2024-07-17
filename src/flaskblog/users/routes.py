from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from src.flaskblog import db, bcrypt

from src.flaskblog.users.utils import save_picture, send_reset_email
from src.flaskblog.models import User
from src.flaskblog.users.forms import (LoginForm, RegistrationForm, UpdateAccountForm, 
                                       RequestResetForm, ResetPasswordForm, ChangePasswordForm)


users = Blueprint('users', __name__)


@users.route('/admin-panel', methods=['GET', 'POST'])
def admin_login():
    return render_template('admin/admin_login.html')


@users.route("/register", methods=['GET', 'POST'])
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
            return redirect(url_for('users.login'))
        except Exception as e:
            flash(f"An error occurred while registering: {str(e)}", category='error')
            db.session.rollback()
            return render_template("register.html", title='Register', form=form)
    return render_template("register.html", title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
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


@users.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('users.login'))
    except Exception as e:
        flash(f"An error occurred while logging out: {str(e)}", category='error')
        return redirect(url_for('views.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            try:
                pic_file = save_picture(form.picture.data)
            except Exception as e:
                flash(f'Error while saving the picture: {str(e)}', category='error')
                return redirect(url_for('users.account'))
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        try:
            db.session.commit()
        except Exception as e:
            flash(f'Error while updating the account: {str(e)}', category='error')
            return redirect(url_for('users.account'))
        flash('Your account has been updated!', category='success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    try:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    except Exception as e:
        flash(f'Error while generating the image file url: {str(e)}', category='error')
        image_file = None
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', category='info')
            return redirect(url_for('users.login'))
        else:
            flash('No account with that email was found.', 'warning')
            return redirect(url_for('users.reset_request'))
    return render_template('reset_request.html', title='Reset Request', form=form)


@users.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', category='warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login.', category='success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, form.old_password.data):
            flash('Incorrect old password', category='error')
            return redirect(url_for('users.change_password'))
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login.', category='success')
        return redirect(url_for('users.login'))
    return render_template('change_password.html', title='Change Password', form=form)
