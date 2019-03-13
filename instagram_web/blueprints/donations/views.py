from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from flask_login import current_user, login_required
from instagram_web.util.helpers import upload_file_to_s3, allowed_file, app
import datetime


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')


@donations_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('donations/new.html')

@donations_blueprint.route('/checkout', methods=['POST'])
def create():
    return redirect(url_for('donations.create'))

