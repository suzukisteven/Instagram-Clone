from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, app
import datetime


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

    user = User(first_name=first_name, last_name=last_name, user_name=user_name, email=email, password=user_password)

    if user.save():
        flash(f"Successfully created account for: {request.form['user_name']}. Please Login to continue.", "success")
        return redirect(url_for('users.login'))
    else:
        flash("Failed to create a new user.", "danger")
        return render_template('new.html', errors=user.errors)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # if current_user.is_authenticated:
        #     # session['user_name'] = request.form['user_name']
        #     flash("Logged in successfully.")
        #     return redirect(url_for('home'))

        user = User.get(User.user_name == request.form['user_name'])

        if not user:
            flash(f"Invalid username or password.")
            return redirect(url_for('users.login'))
        else:
            if check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash(f"Successfully Logged in.", "success")
                return redirect(url_for('home'))
            else:
                flash(f"Invalid username or password.", "danger")
                return redirect(url_for('users.login'))


@users_blueprint.route('/logout')
def logout():
    logout_user()
    session.pop('user_name', None)
    return render_template('login.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return render_template('userprofile.html', user_name=user_name)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id)
    return render_template('edit.html', user=user)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)
    user.user_name = request.form['user_name']
    user.email = request.form['email']
    user.password = request.form['password']

    if current_user == user:
        if user.save():
            flash("Your Profile has been updated.", "success")
        else:
            flash("Your changes were not saved. Please try again.", "danger")
            return redirect(url_for('users.edit', id=user.id, errors=user.errors))
    else:
        flash("You are not authorized to do that.", "danger")
        return render_template('home.html')

    if "user_file" not in request.files:
        flash("No file found!")
    
    file = request.files["user_file"]

    if file.filename == "":
        return "Please select a file."
    
    if file and allowed_file(file.filename):
        file.filename = secure_filename(str(user.id) + file.filename + str(datetime.datetime.now()))
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        user.profile_image_path = output
        user.save()
        return render_template('home.html')
    
    else:
        return redirect("/")

    

