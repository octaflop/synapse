# -*- encoding: utf-8 -*-
from pprint import pprint
from mongoengine import *
from strings import *

from mongomodels import User, Artist, Photo
from mongoengine.queryset import OperationError

connect('aliendog')

# create
user = User(username=u'george', email=u"bob@example.com")
password = u'ædin'
user.hashedpassword = hash_it(user.username, password)
##print type(hash_it(user.username, password))
##pprint(hash_it(user.username, password))

# test
print user.id
try:
    user.save()
    print "woot, saved: %s" % user.hashedpassword
except OperationError:
    print "username not unique"
print user.id
print user.hashedpassword
print user.first_name

# destroy
try:
    user.delete()
except:
    raise ValueError("user not deleted!")

# Artist
# create
artist1 = Artist(first_name=u'fœnix', last_name=u'bobby', bio_en='yall',
        bio_fr=u'ıt')

artist2 = Artist(first_name=u'œdin', last_name=u'sandbox', bio_en='english bio', bio_fr=u'bio française')

artist1.save()
artist2.save()

# create a photo
photo1 = Photo(title="example_photo1.png", artist=artist1)
photo2 = Photo(title="example_photo2.png", artist=artist1)
photo3 = Photo(title="example_photo3.png", artist=artist2)
photo4 = Photo(title="example_photo4.png", artist=artist2)

photo1.save()
photo2.save()
photo3.save()
photo4.save()

artist1.photos = [photo1, photo2]
artist2.photos = [photo3, photo4]
# test
artist1.save()
artist2.save()

for photo in artist1.photos:
    print photo.title
    print photo.id
    print photo.artist.first_name


for photo in artist2.photos:
    print photo.title
    print photo.id
    print photo.artist.first_name

# destroy
artist1.delete()
artist2.delete()
