from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/login', methods=['GET'])
def new():
    return render_template('/sessions/new.html')

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