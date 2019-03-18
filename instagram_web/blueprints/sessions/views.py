from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user
from instagram_web.helpers.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/login', methods=['GET'])
def new():
    return render_template('/sessions/new.html')

@sessions_blueprint.route('/google/login', methods=['GET'])
def google_login():
    redirect_uri = url_for('sessions.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/google/authorize', methods=['GET'])
def google_authorize():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash(f"Welcome back, {user.first_name}", "success")
        return redirect(url_for('users.show', id=user.id))
    else:
        flash("You don't seem to have an account yet. Please create one to continue.", "danger")
        return redirect(url_for('users.new'))

@sessions_blueprint.route('/sessions/', methods=['POST'])
def create():
    user = User.get(User.user_name == request.form['user_name'])

    if not user:
        flash(f"Invalid username or password.")
        return redirect(url_for('sessions.new'))
    else:
        if check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash(f"Welcome back, { current_user.first_name }!", "success")
            next = request.args.get('next')
            return redirect(next or url_for('users.show', id=user.id))
        else:
            flash(f"Invalid username or password.", "danger")
            return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sessions.new'))