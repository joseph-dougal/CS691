from itsdangerous import URLSafeTimedSerializer
from project.helpers.mailer import send_email
from flask import url_for, render_template
from project import app


def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    password_reset_url = url_for(
        'login_routes.reset_with_token',
        token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)

    html = render_template(
        'pages/email_password_reset.html',
        password_reset_url=password_reset_url)

    send_email('Password Reset Requested', user_email, html)
