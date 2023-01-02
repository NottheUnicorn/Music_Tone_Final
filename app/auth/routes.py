from flask import (render_template, redirect, url_for,
                   request, current_app)
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import login_manager
from . import auth
from .forms import SignupForm, LoginForm
from .models import User

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Check if the user doesn't exist
        user = User.get_by_email(email)
        if user is not None:
            error = f'The {email} is already used'
        else:
            # Create the user
            user = User(name=name, email=email)
            user.set_password(password)
            user.save()

            # Login the user
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('site.home')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('site.home')
            return redirect(next_page)
    return render_template('login_form.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
