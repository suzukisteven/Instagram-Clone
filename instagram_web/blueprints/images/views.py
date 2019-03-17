from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, app
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image
import datetime

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/<id>', methods=["POST"])
@login_required
def upload_photo(id):
    if "user_file" not in request.files:
        flash("You didn't upload a file! Please try again.", "danger")

    file = request.files.get('user_file')

    if file:
        if file.filename == "":
            return "Please select a file with a name."
            
        if file and allowed_file(file.filename):
            file.filename = secure_filename(str(id) + file.filename + str(datetime.datetime.now()))
            output = upload_file_to_s3(file, app.config["S3_BUCKET"])
            Image.create(image_path=output, user_id=id)
            flash("Post created", "success")
            return redirect(url_for('users.show', id=id))
        else:
            flash("Only .jpg, .jpeg, .png, or .gif formats are accepted.", "danger")
            return redirect("/")
    else:
        return redirect("/")

@images_blueprint.route('/<image_id>/delete', methods=["POST"])
@login_required
def delete(image_id):
    if current_user.id == Image.user_id:
        image = Image.delete().where(Image.id == image_id)
        if image.execute():
            flash("Your post was successfully deleted.", "success")
            return redirect(url_for('users.show', id=current_user.id))
        else:
            flash("Your post could not be deleted. Please try again.", "danger")
            return redirect(url_for('users.show', id=current_user.id))
    else:
        flash("You are not authorized to do that." "danger")
        return redirect(url_for('sessions.new'))

# HOW DO I PASS THE USERS ID INTO REDIRECT? import current_user from flask_login and set id=current_user.id
# How can I stop other users from going to the users URL and deleting their posts? 1) Hide the delete button 2) not sure
# How do I dependent destroy a post that has a foreign key attached to it with an entry? No idea man

# How did I manage to setup migrations so I only need to run a cli command migrate to run migrations?
# There is no decorator @app.cli.command in app.py