from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src.flaskblog import db
from src.flaskblog.models import Post
from src.flaskblog.users.forms import PostForm

from ..logger import logger

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    try:
        logger.info("Enter into create_post function.")
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash("Your post has been created!", category="success")
            return redirect(url_for("views.home"))
        logger.info("Exited into create_post function.")
        return render_template("create_post.html", Title="New Post", form=form, legend="New Post")
    except Exception as e:
        logger.error(f"Error while creating post: {str(e)}")
        flash(f"Error while creating post: {str(e)}", category="error")
        return render_template("create_post.html", Title="New Post", form=form, legend="New Post")


@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    try:
        logger.info("Enter into update_post function.")
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Your post has been updated!", category="success")
            return redirect(url_for("posts.post", post_id=post.id))
        elif request.method == "GET":
            form.title.data = post.title
            form.content.data = post.content
        logger.info("Exited into update_post function.")
        return render_template("create_post.html", Title="Update Post", form=form, legend="Update Post")
    except Exception as e:
        logger.error(f"Error while updating post: {str(e)}")
        flash(f"Error while updating post: {str(e)}", category="error")
        return render_template("create_post.html", Title="Update Post", form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
@login_required
def delete_post(post_id):
    try:
        logger.info("Enter into delete_post function.")
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted!", category="success")
        logger.info("Exited into delete_post function.")
        return redirect(url_for("views.home"))
    except Exception as e:
        logger.error(f"Error while deleting post: {str(e)}")
        flash(f"Error while deleting post: {str(e)}", category="error")
        return redirect(url_for("views.home"))
