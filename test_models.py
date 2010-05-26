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
print "First, all the members"

