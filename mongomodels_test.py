# -*- encoding: utf-8 -*-
from pprint import pprint
from mongoengine import *
from strings import *

from mongomodels import User, Artist, Photo
from mongoengine.queryset import OperationError

connect('aliendog')

user = User(username=u'faris', email=u"bob@example.com")
password = u'ædin'
user.hashedpassword = hash_it(user.username, password)
##print type(hash_it(user.username, password))
##pprint(hash_it(user.username, password))
print user.id
try:
    user.save()
    print "woot, saved: %s" % user.hashedpassword
except OperationError:
    print "username not unique"
print user.id
print user.hashedpassword
print user.first_name

# Artist
artist = Artist(first_name=u'fœnix', last_name=u'bobby', bio_en='yall',
        bio_fr=u'ıt')
