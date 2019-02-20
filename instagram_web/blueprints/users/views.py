from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from werkzeug.security import generate_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user_name = request.form['user_name']
    email = request.form['email']
    user_password = request.form['password']
    hashed_password = generate_password_hash(user_password)

    user = User(first_name=first_name, last_name=last_name, user_name=user_name, email=email, password=hashed_password)
    if user.save():
        flash(f"Saved {request.form['user_name']} to DB.")
        return redirect(url_for('home'))
    else:
        flash(f"Failed to create a new user. Please try again with different credentials.")
        return render_template('home.html')

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
