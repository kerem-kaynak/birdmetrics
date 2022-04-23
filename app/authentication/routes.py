from os import name
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from flask.helpers import get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash
from app.authentication.helpers.forms import LoginForm, RegisterForm
from app.authentication.models import User

blueprint = Blueprint('authentication', __name__)

@blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('simple_pages.revenue'))
        else:
            flash('Invalid credentials, try again.')
        return(redirect(url_for('asd.login')))
    elif request.method == 'POST':
        flash('Invalid credentials, try again.')
        return(redirect(url_for('asd.login')))
    
    return render_template('authentication/login.html', form = form)

@blueprint.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User(email = form.email.data, password = generate_password_hash(form.password.data))
            user.save()

            login_user(user)
            return redirect(url_for('authentication.login'))
        except:
            flash('Invalid entry, please try again.')
    elif request.method == 'POST':
        flash('Invalid form entry, please try again.')
    return render_template('authentication/register.html', form = form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))

