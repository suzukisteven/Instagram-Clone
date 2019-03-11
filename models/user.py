from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, app
from playhouse.hybrid import hybrid_property
import peewee as pw


class User(UserMixin, BaseModel):
    first_name = pw.CharField(unique=False, null=False)
    last_name = pw.CharField(unique=False, null=False)
    user_name = pw.CharField(unique=True, null=False, index=True)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)
    profile_image_path = pw.CharField(unique=False, null=True)

    def validate(self):
        if len(self.user_name) < 4:
            self.errors.append('Username must be longer than 4 characters!')
        if len(self.password) < 6:
            self.errors.append('Password must be longer than 6 characters!')
        if self.password == " ":
            self.errors.append('You must enter a password!')
        hashed_password = generate_password_hash(self.password)
        self.password = hashed_password


    @login.user_loader
    def load_user(id):
        try:
            return User.get_by_id(id)
        except:
            pass

    @hybrid_property
    def profile_image_url(self):
        if self.profile_image_path:
            return app.config['S3_LOCATION'] + self.profile_image_path
        else:
            return app.config['S3_LOCATION'] + "20profile_placeholder.png2019-03-07_122049.466378"
