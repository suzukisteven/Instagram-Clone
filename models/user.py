from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    first_name = pw.CharField(unique=False, null=False)
    last_name = pw.CharField(unique=False, null=False)
    user_name = pw.CharField(unique=True, null=False, index=True)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(unique=False, null=False)
    
