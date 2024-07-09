import os, secrets
from PIL import Image
from flask_mail import Message
from flask import url_for

from src.flaskblog import app, mail

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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:

{url_for('users.reset_token', token=token, _external=True)}

if you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
