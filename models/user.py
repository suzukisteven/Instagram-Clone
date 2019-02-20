from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import peewee as pw


class User(UserMixin, BaseModel):
    first_name = pw.CharField(unique=False, null=False)
    last_name = pw.CharField(unique=False, null=False)
    user_name = pw.CharField(unique=True, null=False, index=True)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        if check_password_hash(self.hashed_password, password):
            return True
        else:
            return False

    @login.user_loader
    def load_user(self, id):
        try:
            return User.get_by_id(id)
        except:
            pass
    
