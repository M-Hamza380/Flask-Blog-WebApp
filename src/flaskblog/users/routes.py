from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, login_required, logout_user
from src.flaskblog import db, bcrypt

from src.flaskblog.users.utils import save_picture, send_reset_email
from src.flaskblog.models import User
from src.flaskblog.users.forms import (LoginForm, RegistrationForm, UpdateAccountForm, 
                                       RequestResetForm, ResetPasswordForm, ChangePasswordForm,
                                       AdminLoginForm, UpdateAdminAccountForm, PostForm)


from src.flaskblog.models import Post
from src.flaskblog.users.logger import logger

users = Blueprint('users', __name__)

@users.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('views.home'))
    return render_template('create_post.html', Title='New Post', form=form, legend='New Post')

@users.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@users.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('users.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', Title='Update Post', form=form, legend='Update Post')


@users.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('views.home'))


@users.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin_user = User.query.filter_by(email=form.admin_email.data).first()
        if admin_user is not None and admin_user.email == "tecdev74@gmail.com" and bcrypt.check_password_hash(admin_user.password, form.admin_password.data):
            login_user(admin_user)
            next_page = request.args.get('next')            
            flash('Login successful in admin panel.', category='success')
            return redirect(next_page) if next_page else redirect(url_for('users.admin_home'))
        else:
            flash('Incorrect email or password', category='error')
            return redirect(url_for('users.login'))
        
    return render_template('admin/admin_login.html', title='Admin Login', form=form)


@users.route("/admin-logout", methods=["GET"])
@login_required
def admin_logout():
    try:
        logout_user()
        return redirect(url_for('users.login'))
    except Exception as e:
        flash(f"An error occurred while logging out: {str(e)}", category='error')
        return redirect(url_for('views.admin_home'))

@users.route('/admin-account', methods=['GET', 'POST'])
@login_required
def admin_account():
    form = UpdateAdminAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            try:
                pic_file = save_picture(form.picture.data)
            except Exception as e:
                flash(f'Error while saving the picture: {str(e)}', category='error')
                return redirect(url_for('users.admin_account'))
            current_user.image_file = pic_file

        current_user.email = form.email.data
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error while updating the account: {str(e)}', category='error')
            return redirect(url_for('users.account'))
        
        flash('Your account has been updated!', category='success')
        return redirect(url_for('users.admin_account'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
    try:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    except Exception as e:
        flash(f'Error while generating the image file url: {str(e)}', category='error')
        image_file = None

    return render_template('admin/admin_account.html', title='Admin Account', image_file=image_file, form=form)


@users.route("/register", methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash("You have been logged in!", category='success')
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist!', category='error')
    
    return render_template("login.html", title='Login', form=form)


@users.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('users.login'))
    except Exception as e:
        flash(f"An error occurred while logging out: {str(e)}", category='error')
        return redirect(url_for('views.index'))

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
    logger.info(f"Entered reset_token route.")

    user = User.verify_reset_token(token)
    if user:
        logger.info(f'User found: {user.username}')
    else:
        logger.info('Invalid or expired token, redirecting to reset request.')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    if request.method == 'POST':
        logger.info("POST request received.")

        if form.validate_on_submit():
            logger.info('Form validated, attempting to reset password.')
            try:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password                
                db.session.commit()
                logger.info('Password updated successfully in the database.')
                return redirect(url_for('users.login'))
            except Exception as e:
                db.session.rollback()
                logger.error(f'Error updating password: {e}')
                return redirect(url_for('users.reset_token', token=token))
        else:
            logger.info(f"Form validation failed. Errors: {form.errors}")

    return render_template('reset_token.html', title='Reset Password', form=form, token=token)

@users.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():    
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
