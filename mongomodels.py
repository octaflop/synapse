# -*- encoding: utf-8 -*-
from strings import *
import uuid as ui
import datetime

from mongoengine import *
connect('aliendog')

SALT = "FAkeSa8r3y2qwi"
EMAILREG =\
"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"

class User(Document):
    email = StringField(required=True, regex=EMAILREG)
    username = StringField(required=True, unique=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    hashedpassword = StringField()

class Photo(Document):
    title = StringField(max_length=120, required=True, unique=True)
    title_en = StringField(max_length=120)
    title_fr = StringField(max_length=120)
    filename = StringField(unique=True)
    path = StringField()
    artist = ReferenceField('Artist')

class Artist(Document):
    unique_name = StringField(max_length=120, unique=True, required=True)
    first_name = StringField(max_length=120)
    last_name = StringField(max_length=120)
    bio_en = StringField()
    bio_fr = StringField()
    photos = ListField(ReferenceField(Photo))

