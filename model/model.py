
from mongoengine import SequenceField, BooleanField, Document, StringField, DateTimeField
import datetime


class User(Document):
    id = SequenceField(primary_key=True)
    user_name = StringField(unique=True, max_length=50, required=True)
    email = StringField(unique=True)
    password = StringField(required=True, min_length=8, max_length=40)
    is_active = BooleanField(default=False)
    db_created = DateTimeField(default=datetime.datetime.now)

