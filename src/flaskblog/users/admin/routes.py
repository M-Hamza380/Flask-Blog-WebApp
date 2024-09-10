from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from src.flaskblog import db, bcrypt

from src.flaskblog.users.utils import save_picture
from src.flaskblog.models import User
from src.flaskblog.users.forms import AdminLoginForm, UpdateAdminAccountForm


admin = Blueprint('admin', __name__)

@admin.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin_user = User.query.filter_by(email=form.admin_email.data).first()
        if admin_user is not None and admin_user.email == "tecdev74@gmail.com" and bcrypt.check_password_hash(admin_user.password, form.admin_password.data):
            login_user(admin_user)
            next_page = request.args.get('next')            
            flash('Login successful in admin panel.', category='success')
            return redirect(next_page) if next_page else redirect(url_for('views.admin_home', admin_user=admin_user, form=form))
        else:
            flash('Incorrect email or password', category='error')
            return redirect(url_for('users.login'))
        
    return render_template('admin/admin_login.html', title='Admin Login', form=form)


@admin.route("/admin-logout", methods=["GET"])
@login_required
def admin_logout():
    try:
        logout_user()
        return redirect(url_for('users.login'))
    except Exception as e:
        flash(f"An error occurred while logging out: {str(e)}", category='error')
        return redirect(url_for('views.admin_home'))

@admin.route('/admin-account', methods=['GET', 'POST'])
@login_required
def admin_account():
    form = UpdateAdminAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            try:
                pic_file = save_picture(form.picture.data)
            except Exception as e:
                flash(f'Error while saving the picture: {str(e)}', category='error')
                return redirect(url_for('admin.admin_account'))
            current_user.image_file = pic_file

        current_user.email = form.email.data
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error while updating the account: {str(e)}', category='error')
            return redirect(url_for('admin.admin_account'))
        
        flash('Your account has been updated!', category='success')
        return redirect(url_for('admin.admin_account'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
    try:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    except Exception as e:
        flash(f'Error while generating the image file url: {str(e)}', category='error')
        image_file = None

    return render_template('admin/admin_account.html', title='Admin Account', image_file=image_file, form=form)
