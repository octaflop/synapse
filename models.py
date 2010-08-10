# -*- encoding: utf-8 -*-
from strings import *
import uuid as ui
import datetime

from mongoengine import *
connect('aliendog')

SALT = "FAkeSa8r3y2qwi"
EMAILREG =\
"/^([\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+\.)*[\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+@((((([a-z0-9]{1}[a-z0-9\-]{0,62}[a-z0-9]{1})|[a-z])\.)+[a-z]{2,6})|(\d{1,3}\.){3}\d{1,3}(\:\d{1,5})?)$/i"

class Site(Document):
    title = StringField(required=True)
    domain = StringField(required=True)

class User(Document):
    email = StringField(required=True, regex=EMAILREG)
    username = StringField(required=True, unique=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    hashedpassword = StringField()
    date_created = DateTimeField()

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    date_created = DateTimeField()

class Post(Document):
    title = StringField(max_length=120)
    author = ReferenceField(User)
    slug = StringField()
    tags = ListField(StringField(max_length=45))
    date_created = DateTimeField()

class TextPost(Post):
    author = ReferenceField(User)
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class AudioPost(Post):
    audio_path = StringField()

