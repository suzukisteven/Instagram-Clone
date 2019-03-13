from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import app
from playhouse.hybrid import hybrid_property
import peewee as pw
import re 


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
        if not self.password:
            self.errors.append('You must enter a password!')
        breakpoint()
        if not re.match(r"^[p][b][k][d][f][2][:][s][h][a][2][5][6][:].{79}\b", self.password):
            # nest password validation here
            hashed_password = generate_password_hash(self.password)
            self.password = hashed_password

    @hybrid_property
    def profile_image_url(self):
        if self.profile_image_path:
            # If a profile_image_path exists, display the profile image
            return app.config['S3_LOCATION'] + self.profile_image_path
        else:
            # Otherwise, display a placeholder image instead.
            return app.config['S3_LOCATION'] + "20profile_placeholder.png2019-03-07_122049.466378"
