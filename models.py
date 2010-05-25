import redis
import re
import hashlib
import uuid as ui
import datetime
from settings import REDIS_SERVER, REDIS_PASSWD, DEV, SALT

if DEV:
        R = redis.Redis()
elif not DEV:
	R = redis.Redis(host=REDIS_SERVER, password=REDIS_PASSWD)

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

class Thing():
    def __init__(self, kind=None):
        if kind is None:
            self.kind = 'thing'
        elif type(kind) is str:
            self.kind = kind
        else:
            raise TypeError("got " + kind + " as type:" + type(kind) + ". Need\
                    str")
        self.creation = str(datetime.datetime.now())
        self.uuid = str(ui.uuid1())
        self.attrs = {}

    def _exists(self, kind, uuid):
        if not R.sismember("%s" % kind, uuid):
            print "not in database"
            return False
        elif R.sismember("%s" % kind, uuid):
            return True

    def _checkid(self, kind, uuid):
        if self.kind is None:
            if kind is None:
                self.kind = 'thing'
            elif type(kind) is str:
                self.kind = kind
            else:
                print "input a proper kind"
                return False
        elif type(self.kind) is str:
            kind = self.kind
        if self.uuid is None:
            if uuid is None:
                print "Error. Instantiate a uuid or supply one."
                return False
            elif isinstance(uuid, str):
                self.uuid = uuid
                return True
        elif isinstance(self.uuid,  str):
            uuid = self.uuid
            return True
        else:
            print "Some sort of error occurred"
            return False

    def get_tid(self, kind=None, uuid=None):
        assert self._checkid(kind, uuid)
        self.tid = R.get("%s:%s:tid" % (self.kind, self.uuid))
        return self.tid

    def get(self, kind=None, uuid=None):
        assert self._checkid(kind, uuid)
        assert self._exists(self.kind, self.uuid)
        self.tid = self.get_tid(self.kind, self.uuid)
        redkey = "%s:%s" % (self.kind, self.tid)
        ret = R.hgetall(redkey)
        return ret

    def post(self, attrs=None):
        if not R.sadd("%s" % self.kind, self.uuid):
            print "already in database"
            return False
        self.tid = R.zincrby("global:%s:tid" % self.kind, 1) # tid = "thing id"
        R.set("%s:%s:tid" % (self.kind, self.uuid), self.tid)
        redkey = "%s:%s" % (self.kind, self.tid)
        if attrs and self.attrs is None:
            self.attrs = {}
        elif isinstance(attrs, dict):
            self.attrs = attrs
        elif isinstance(self.attrs, dict):
            attrs = self.attrs
        else:
            print "Attrs are invalid type"
            return False
        self.attrs['creation'] = self.creation
        self.attrs['uuid'] = self.uuid
        R.hmset(redkey, self.attrs)
        for attr in self.attrs.keys():
            key = redkey + ":" + attr
            R.set(key, self.attrs[attr])
        return True

    def put(self, attrs, kind=None, uuid=None):
        assert isinstance(attrs, dict)
        assert self._checkid(kind, uuid)
        assert self._exists(self.kind, self.uuid)
        self.tid = self.get_tid(self.kind, self.uuid)
        self.attrs = attrs
        redkey = "%s:%s" % (self.kind, self.tid)
        ret = ""
        ret += R.hmset(redkey, self.attrs)
        for attr in attrs.keys():
            key = redkey + ":" + attr
            R.set(key, attrs[attr])
            ret += R.hset(redkey, attr, attrs[attr])
        R.bgsave()
        return ret

    def delete(self, kind=None, uuid=None):
        assert self._checkid(kind, uuid)
        assert self._exists(self.kind, self.uuid)
        self.tid = self.get_tid(self.kind, self.uuid)
        redkey = "%s:%s" % (self.kind, self.tid)
        R.srem("%s" % self.kind, self.uuid)
        R.delete(redkey)
        return True


class User(Thing):
    def __init__(self, username, email, password, kind='user'):
        self.username = username
        self.email = email
        self.kind = kind
        self.creation = str(datetime.datetime.now())
        self.uuid = str(ui.uuid1())
        m = hashlib.sha1()
        self.shapassword = hash_it(self.username, password)
        self.attrs = {
                'username' : self.username,
                'slug' : slugfy(self.username),
                'email' : self.email,
                'creation' : self.creation,
                'uuid' : self.uuid,
                'shapassword' : self.shapassword,
                }
    def _check_credentials(self, username, password):
        if hash_it(username, password) ==\
            self.get(self.kind, self.uuid)['shapassword']:
            return True
        else:
            return False

"""
class Photo(Thing):
    def __init__(self, title_en, title_fr, kind='photo'):
        self.title_en = title_en
        self.title_fr = title_fr
        self.attr = {}
        self.attr = {
                'title_en' : self.title_en,
                'slug' : slugfy(self.title_en)
                'title_fr' : self.title_fr,
                'description_en' : self.description_en,
                'description_fr' : self.description_fr,
                'creation' : self.creation,
                'uuid' : self.uuid,
                'photo_url' : "%s/%s" % (self.type, self.slug),
                'status_en' : self.status_en,
                'status_fr' : self.status_fr,
                'price' : self.price
                }
"""

class Artist(Thing):
    def __init__(self, name, type='artist'):
        self.name = name

#class ArtistForm(Form):
#    name = TextField(u"The full author's name", [validators.Length(min=3,
#    max=65)]))
#    bio_en = TextAreaField(u"Artist's biography in English")
#    bio_fr = TextAreaField(u"Artist's biography in French")

