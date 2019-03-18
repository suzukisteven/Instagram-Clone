from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from models.image import Image
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, app
import datetime


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

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
        return redirect(url_for('sessions.new'))
    else:
        flash("Failed to create a new user.", "danger")
        return render_template('new.html', errors=user.errors)

@users_blueprint.route('/<id>', methods=["GET"])
@login_required
def show(id):
    user = User.get_or_none(id=id)
    return render_template('images/userprofile.html', user=user, Image=Image)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if current_user == user:
        return render_template('edit.html', user=user)
    else:
        return redirect(url_for('users.edit', id=current_user.id))

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)
    if current_user == user:
        user.user_name = request.form['user_name']
        user.email = request.form['email']
        if request.form.get('password'):
            user.password = request.form.get('password')

        if request.form.get('description'):
            user.description = request.form.get('description')

        if request.files.get('user_file'):
            if "user_file" not in request.files:
                flash("No file found! Please try again.")
            
            file = request.files["user_file"]

            if file.filename == "":
                return "Please select a file with a valid filename."
            
            if file and allowed_file(file.filename):
                file.filename = secure_filename(str(user.id) + file.filename + str(datetime.datetime.now()))
                output = upload_file_to_s3(file, app.config["S3_BUCKET"])
                user.profile_image_path = output
            else:
                flash("Please upload only .png, ,jpg, .jpeg or .gif format", "danger")
                return render_template('home.html')
        
        if user.save():
            flash("Your Profile has been updated.", "success")
            return redirect(url_for('users.show', id=user.id))
        else:
            flash("Your changes were not saved. Please try again.", "danger")
            return redirect(url_for('users.edit', id=user.id, errors=user.errors))
    else:
        flash("You are not authorized to do that.", "danger")
        return render_template('home.html')

@users_blueprint.route('/toggle_privacy/<id>', methods=['POST'])
def update_profile_privacy(id):
    user = User.get_by_id(id)
    if current_user == user:
        user.update(profile_privacy = not user.profile_privacy).execute()
        flash("Your profile privacy settings have been updated.", "info")
        return redirect(url_for('users.edit', id=user.id))
    else:
        return redirect(url_for('sessions.create'))

