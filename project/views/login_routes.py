from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from project.views.utils import send_password_reset_email
from itsdangerous import URLSafeTimedSerializer
from project.db_utils.login_model import User
from datetime import datetime
from project import app, db


login_routes = Blueprint('login_routes', __name__)


@login_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user is not None and user.check_password(password) is False:
        flash('Wrong password, please try again.', 'danger')
        return redirect(url_for('login_routes.login'))

    elif user is None:
        flash('Invalid email address.', 'danger')
        return redirect(url_for('login_routes.login'))

    else:
        user.authenticated = True
        user.last_logged_in = user.current_logged_in
        user.current_logged_in = datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('utility_routes.home'))

    


@login_routes.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    user = current_user
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('login_routes.login'))


@login_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method != 'POST':
        return render_template('register.html')
        
    email = request.form['email']
    pw = request.form['password']

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if user is None:

        new_user = User(email, pw)
        new_user.authenticated = True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Thanks for registering!', 'success')

        return redirect(url_for('utility_routes.home'))

    else:
        flash('Email already exists', 'danger')
        return render_template('register.html')

    


@login_routes.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    if request.method != 'POST':
        return render_template('forgot-password.html')

    email = request.form['email']
    try:
        user = User.query.filter_by(email=email).first_or_404()
    except:
        flash('Invalid email address!', 'danger')
        return redirect(url_for('login_routes.reset'))

    if user.email:
        send_password_reset_email(user.email)
        flash('Please check your email for a password reset link.', 'info')
    else:
        flash('Your email was not found', 'danger')
    return redirect(url_for('login_routes.login'))




@login_routes.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):

    try:
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('login_routes.login'))

    if request.method != 'POST':
        return render_template('forgot-password-token.html', token=token)
        
    new_password = request.form['new_password']
    try:
        user = User.query.filter_by(email=email).first_or_404()
    except:
        flash('Invalid email address!', 'danger')
        return redirect(url_for('login_routes.login'))

    user.set_password(new_password)
    db.session.add(user)
    db.session.commit()
    flash('Your password has been updated!', 'success')
    return redirect(url_for('login_routes.login'))

    


