# -*- encoding:utf-8 -*-
print "testing imports"
import models
from models import Thing, User, Photo, Artist
from pprint import pprint

print "testing objects"
t = Thing(kind='guy')
ret = t
print ret

print "post test"
ret = t.post()
print ret

print "get test"
ret = t.get()
print ret

attrs = {
        'uuid' : 'NEW UUID!'
        }
print "put test"
ret = t.put(attrs)
print ret

print "get test"
ret = t.get()
pprint("got: %s" % ret)

print "delete test"
ret = t.delete()
print ret

print "deleted get test (should return false)"
ret = t._exists(t.kind, t.uuid)
print ret

print "USER MODEL TESTS"
q = User('faris', 'test@example.com', 'password')
ret = q
pprint("User object is: %s" % ret)

print "post test"
ret = q.post()
pprint("Post test (true): %s" % ret)

print "get test"
ret = q.get()
pprint("got: %s" % ret)

user_attrs = {
        u"first_name": u"Faris",
        u"last_name": u"Chebib",
        u"languages": ['en', 'ar', 'fr', 'de']
        }

print "put test"
ret = q.put(attrs)
pprint("putted: %s" % ret)

print "get test"
ret = q.get()
pprint("got: %s" % ret)

print "password check test"
print "Credentials. Should be true: %s" % q._check_credentials('faris', 'password')

print "Credentials. Should be false: %s" % q._check_credentials('faris', 'passWord')

print "delete test"
ret = q.delete()
pprint("deleted: %s" % ret)

print "get deleted test: this should return false"
ret = q._exists(q.kind, q.uuid)
print "exists?. It shouldn't %s" % ret

print "BEGIN photo test"
p = Photo(u'What a wonderful Photo!', u"Qu'est-ce qu'un magnifique photo!")
photo_attrs = {
        u"description_en" : u"description english",
        u"description_fr" : u"description français",
        u"status_en" : u"For sale",
        u"status_fr" : u"à vendre",
        u"price" : 99.46
    }

ret = p.post()
pprint("photo object: %s" % ret)

ret = p.get()
pprint("got: %s" % ret)

ret = p.put(photo_attrs)
pprint("putting : %s" % ret)

print "deleting"
ret = p.delete()
pprint("deleted: %s" % ret)
ret = p._exists(p.kind, p.uuid)
print "Exists? Should be false: %s" % ret

print "BEGIN photo test"
a = Artist(u'some dude')
artist_attrs = {
    'bio_en' : "English BIO",
    'bio_fr' : u"Bio française",
    }

ret = a.post()
pprint("photo object: %s" % ret)

ret = a.get()
pprint("got: %s" % ret)

ret = a.put(artist_attrs)
pprint("putting : %s" % ret)

print "deleting"
ret = a.delete()
pprint("deleted: %s" % ret)
ret = a._exists(a.kind, a.uuid)
print "Exists? Should be false: %s" % ret

print "ONWARDS WITH THE RELATIONAL STUFF..."
print "creating test classes"

photo1 = Photo(u'Photo Title', u"Photö Title")
photo2 = Photo(u'Photo 2 Title', u"Photö duex Title")
photo1_attrs = {
        u"description_en" : u"description english",
        u"description_fr" : u"description français",
        u"status_en" : u"For sale",
        u"status_fr" : u"à vendre",
        u"price" : 99.46
        }

photo2_attrs = {
        u"description_en" : u"description 2 english",
        u"description_fr" : u"description 2 français",
        u"status_en" : u"For sale 2",
        u"status_fr" : u"à 2 vendre",
        u"price" : 87.88
        }

artist1 = Artist("Bob", photos=[photo1])
artist2 = Artist("Joe", photos=[photo1, photo2])

photo3 = Photo(u"Bob's second photo", u"Bob's duex photo!?", artists=[artist1])

photo1.post()
photo1.put(photo1_attrs)
photo2.post()
photo2.put(photo2_attrs)
artist1.post()
artist2.post()
photo3.post()

pprint(photo1.get())
pprint(photo2.get())
pprint(photo3.get())
pprint(artist1.get())
pprint(artist2.get())

print "Checking those relational methods"
pprint(photo1._artists())
pprint(photo2._artists())
pprint(photo3._artists())
pprint(artist1._photos())
pprint(artist2._photos())

print "grabbing an url from a relational method"
# TODO
art1 = artist1._photos()
pprint("url %s" % art1[0])
pprint(artist1._full_url())

print "Generate the urls"
for url in artist1._photo_urls():
    print url

for url in photo3._artist_urls():
    print url

print artist1._Photos()

photo1.delete()
photo2.delete()
photo3.delete()
artist1.delete()
artist2.delete()
