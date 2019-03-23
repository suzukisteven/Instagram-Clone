from models.user import User, BaseModel
from app import app
from playhouse.hybrid import hybrid_property
import peewee as pw

class Following(BaseModel):
    fan = pw.ForeignKeyField(User, backref='idols', on_delete='CASCADE')
    idol = pw.ForeignKeyField(User, backref='fans', on_delete='CASCADE')
    is_approved = pw.BooleanField(default=False)
