# strings.py
# all of the fiddly bits.
import redis
import re
from settings import SALT

R = redis.Redis()
import hashlib

def slugfy(text, separator='-'):
  ret = ""
  for c in text.lower():
    try:
      ret += htmlentitydefs.codepoint2name[ord(c)]
    except:
      ret += c
  ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
  ret = re.sub("\W", " ", ret)
  ret = re.sub(" +", separator, ret)
  return ret.strip()

def hash_it(username, password):
    ret = ""
    m = hashlib.sha1()
    m.update(username)
    m.update(SALT)
    m.update(password)
    ret = m.digest()
    return ret

def add_uurl(kind, slug, tid, uuid):
    if not R.sadd("%s:slug" % kind, slug):
        slug += "_"
        return add_uurl(kind, slug, tid, uuid)
    else:
        R.set("%s:%s" % (kind, slug), tid)
        R.set("%s:%s" % (kind, uuid), slug)
        R.set("%s" % uuid, slug)
        R.set("%s:%s:uuid" % (kind, slug), uuid)
        R.set("%s:%s:uurl" % (kind, tid), slug)
        return slug

def slug2tid(kind, slug):
    tid = R.get("%s:%s" % (kind, slug))
    return tid

def tid2uurl(kind, tid):
    url = ""
    tid = slug2tid(kind, slug)
    url = R.get("%s:%s:uurl" % (kind, tid))
    return url

def slug2uurl(kind, slug):
    tid = slug2tid(kind, slug)
    uurl = R.get("%s:%s:uurl" % (kind, tid))
    return uurl

def uuid2uurl(uuid):
    uurl = R.get("%s" % uuid)
    return uurl

def uurl2uuid(kind, uurl):
    uuid = R.get("%s:%s:uuid" % (kind, uurl))
    return uuid

def build_url(kind, uuid):
    uurl = uuid2uurl(uuid)
    url = "%s/%s" % (kind, uurl)
    return url

