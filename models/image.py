from models.user import User, BaseModel
from app import app
from playhouse.hybrid import hybrid_property
import peewee as pw

class Image(BaseModel):
    image_path = pw.CharField()
    caption = pw.TextField(unique=False, null=True)
    user_id = pw.ForeignKeyField(User, backref='images', on_delete='CASCADE')

    @hybrid_property
    def image_url(self):
        return app.config['S3_LOCATION'] + self.image_path
        
