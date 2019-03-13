from models.user import User, BaseModel
from app import app
from playhouse.hybrid import hybrid_property
import peewee as pw

class Image(BaseModel):
    image_path = pw.CharField()
    # Foreign key reference to which user the images belong to.
    # One-to-Many relationship: User can have multiple images, but they belong to a single user.
    # The backref allows for you to query images.user, images.id etc
    user_id = pw.ForeignKeyField(User, backref='images')

    @hybrid_property
    def image_url(self):
        return app.config['S3_LOCATION'] + self.image_path
        
