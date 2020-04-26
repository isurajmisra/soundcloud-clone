from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from soundcloud import db, bcrypt
from soundcloud.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from soundcloud.users.utils import save_media
from soundcloud.users.model import User
from soundcloud.songs.model import Songs
from soundcloud.services import get_all_songs_by_user
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/update-account", methods=["GET", "POST"])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_media(form.picture.data, "static/profile_pics")
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for(
            "static", filename="profile_pics/" + current_user.image_file
        )

    return render_template(
        "update-account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/account")
@login_required
def account():
    songs = get_all_songs_by_user(current_user.id)
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)

    return render_template("account.html", songList=songs, image_file=image_file)


@users.route("/like/<int:song_id>/<action>")
@login_required
def like_action(song_id, action):
    song = Songs.query.filter_by(id=song_id).first_or_404()
    if action == "like":
        current_user.like(song)
        db.session.commit()
    if action == "unlike":
        current_user.unlike(song)
        db.session.commit()

    return redirect(request.referrer)
