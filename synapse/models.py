# -*- encoding: utf-8 -*-
from settings import UPLOAD_FOLDER, STATIC_PATH
import datetime
from strings import permalink
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
    # datetime
    created = DateTimeField()
    published = DateTimeField()
    updated = ListField(DateTimeField())
    meta = {
        'ordering': ['-published']
        }
    @permalink
    def permalink(self):
        return 'profile', {'username':self.username}

class Comment(EmbeddedDocument):
    slugid = StringField(required=True, unique=True, max_length=8) #min_length=8, max_length=8)
    content = StringField()
    name = StringField(max_length=120)
    # datetime
    created = DateTimeField()
    published = DateTimeField()
    updated = ListField(DateTimeField())
    meta = {
        'ordering': ['-published']
        }
    @permalink
    def permalink(self):
        return 'comment', {'slugid': self.slugid}

#class Media(EmbeddedDocument, object):
class Media(Document, object):
    title = StringField(required=True)
    filename = StringField(required=True)
    slug = StringField(required=True)
<<<<<<< HEAD
    slugid = StringField(required=True, unique=True, max_length=8) #min_length=8, max_length=8)
=======
    slugid = StringField(required=True, unique=True, min_length=8, max_length=8)
>>>>>>> be32bd6abe4dc110e2e3a9e2080d72d49aed9560
    author = ReferenceField(User)
    description = StringField()
    # datetime
    created = DateTimeField()
    published = DateTimeField()
    updated = ListField(DateTimeField())
    @permalink
    def raw(self):
        return STATIC_PATH, {'filename':self.filename}
    meta = {
        'ordering': ['-published']
        }
    #@permalink
    #def permalink(self):
    #    return 'media', {'slugid': self.slugid}


class Post(Document, object):
    title = StringField(max_length=120)
    author = ReferenceField(User)
    slug = StringField(required=True)#, unique=True)
<<<<<<< HEAD
    slugid = StringField(required=True, unique=True, max_length=8) #min_length=8, max_length=8)
=======
    slugid = StringField(required=True, unique=True, min_length=8, max_length=8)
>>>>>>> be32bd6abe4dc110e2e3a9e2080d72d49aed9560
    tags = ListField(StringField(max_length=45))
    rss = StringField()
    # datetime
    created = DateTimeField()
    published = DateTimeField()
    updated = ListField(DateTimeField())
    meta = {
        'ordering': ['-published']
        }
    @permalink
    def permalink(self):
        return 'post_by_slugid', {'slugid':self.slugid}

class TextPost(Post):
    content = StringField()
    html_content = StringField()
    #media = ListField(EmbeddedDocumentField(Media))

class FlatPage(TextPost):
    title = StringField(max_length=120, unique=True)

class Dependency(Document):
    title = StringField(required=True)
    url = StringField(required=True)
    authors = ListField(StringField())
    imgurl = StringField()

