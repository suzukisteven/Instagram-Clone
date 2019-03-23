from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, app
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image
from models.following import Following
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
            return "Please select a file with a valid name."
            
        if file and allowed_file(file.filename):
            file.filename = secure_filename(str(id) + "_" + file.filename + "_" +str(datetime.datetime.now()))
            output = upload_file_to_s3(file, app.config["S3_BUCKET"])
            Image.create(image_path=output, user_id=id)
            flash("Your Post was created", "success")
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
        flash("You are not authorized to do that.", "danger")
        return redirect(url_for('sessions.new'))