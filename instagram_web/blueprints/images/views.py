from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, app
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image
import datetime

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/<id>', methods=["POST"])
def upload_photo(id):
    if "user_file" not in request.files:
        flash("No file found! Please try again.")

    file = request.files["user_file"]

    if file.filename == "":
        return "Please select a file."

    if file and allowed_file(file.filename):
        file.filename = secure_filename(str(id) + file.filename + str(datetime.datetime.now()))
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        Image.create(image_path=output, user_id=id)
        return redirect(url_for('users.show', id=id))
    else:
        return redirect("/")