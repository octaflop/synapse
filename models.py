# -*- encoding: utf-8 -*-
import datetime

from mongoengine import *
connect('synapse')

SALT = "FAkeSa8r3y2qwi"
#EMAILREG =\
#"/^([\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+\.)*[\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+@((((([a-z0-9]{1}[a-z0-9\-]{0,62}[a-z0-9]{1})|[a-z])\.)+[a-z]{2,6})|(\d{1,3}\.){3}\d{1,3}(\:\d{1,5})?)$/i"

class Site(Document):
    title = StringField(required=True)
    motto = StringField()
    domain = StringField(required=True)
    logo = StringField()

class User(Document, object):
    email = StringField(required=True)#, regex=EMAILREG)
    username = StringField(required=True, unique=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    hashedpassword = StringField()
    date_created = DateTimeField()

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    date_created = DateTimeField()

class Media(EmbeddedDocument):
    title = StringField(required=True)
    filename = StringField(required=True)
    slug = StringField(required=True)
    slugid = StringField(required=True, unique=True, min_length=8, max_length=8)
    date_created = DateTimeField(required=True)
    author = ReferenceField(User)
    description = StringField()

class Post(Document, object):
    title = StringField(max_length=120)
    author = ReferenceField(User)
    slug = StringField(required=True)#, unique=True)
    slugid = StringField(required=True, unique=True, min_length=8, max_length=8)
    tags = ListField(StringField(max_length=45))
    date_created = DateTimeField()
    rss = StringField()
    meta = {
            'ordering': ['-published_date']
            }

class TextPost(Post):
    content = StringField()
    html_content = StringField()
    media = ListField(EmbeddedDocumentField(Media))

class FlatPage(TextPost):
    pass

class Dependency(Document):
    title = StringField(required=True)
    url = StringField(required=True)
    authors = ListField(StringField())
    imgurl = StringField()

