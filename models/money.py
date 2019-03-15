from models.user import User, BaseModel
from models.image import Image, BaseModel
from app import app
import peewee as pw

class Money(BaseModel):
    amount = pw.DecimalField(decimal_places=2)
    # Foreign key reference to which user the images belong to.
    # One-to-Many relationship: User can have multiple donations, but they belong to a single user.
    # The backref allows for you to query image.donations, user.donations etc
    user_id = pw.ForeignKeyField(User, backref='donations')
    image_id = pw.ForeignKeyField(Image, backref='donations')