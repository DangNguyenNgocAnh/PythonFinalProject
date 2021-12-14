from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from .models import  Post, User, Comment, Like,Follow
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get('title')
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text,title=title, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/edit-post/<post_id>", methods = ['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    elif request.method == 'POST':
        text = request.form.get('text')
        title = request.form.get('title')
        if len(text) < 1 or len(title)<1:
            flash('Please edit text !', category='error')
        else:
            post.text = text
            post.title = title
            db.session.commit()
            flash('Post is updated!', category='success')
            return redirect(url_for('views.home'))
    return render_template('edit_post.html', user= current_user, post= post)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        flash('Posts does not exist.', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/profile/<username>")
@login_required
def profile(username):
    users = User.query.filter_by(username=username).first()

    if not user:
        return redirect(url_for('views.home'))

    return render_template("profile.html", user=current_user,posts=posts ,users=users)


@views.route("/follow/<user_id>", methods=['GET'])
@login_required
def follow(user_id):
    followed = User.query.filter_by(id=user_id).first()
    hasfollow = Follow.query.filter_by(follower_id=current_user.id, followed_id=followed.id).first()
    if not followed:
        flash('User does not exists.', category='error')
    elif hasfollow:
        db.session.delete(hasfollow)
        db.session.commit()
    else:
        hasfollow = Follow(follower_id= current_user.id, followed_id=followed.id)
        db.session.add(hasfollow)
        db.session.commit()
    return redirect(url_for('views.home'))


@views.route("/follower/<username>")
@login_required
def follower(username):
    return render_template("follower.html", user=current_user, posts=posts, username=username)

@views.route("/following/<username>")
@login_required
def following(username):
    return render_template("following.html", user=current_user, posts=posts, username=username)
