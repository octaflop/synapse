print "testing imports"
import models
from models import Thing, User

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

print "USER MODEL TESTS"
q = User('faris', 'test@example.com', 'password')
ret = q
print ret

print "post test"
ret = q.post()
print ret

print "get test"
ret = q.get()
print ret

print "password check test"
print "should be true: %s" % q._check_credentials('faris', 'password')

print "should be false: %s" % q._check_credentials('faris', 'passWord')
