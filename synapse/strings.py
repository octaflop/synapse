# -*- encoding: utf-8 -*-
# strings.py
# all of the fiddly bits.
from flask import url_for
from werkzeug.routing import BuildError
from settings import SALT, ALLOWED_EXTENSIONS

from unidecode import unidecode
import datetime
import hashlib
import random
import uuid
import re

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugfy(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return unicode(delim.join(result))

def slugidfy():
    return unicode(uuid.uuid1())[:8]

def permalink(function):
    """Build a permalink decorator for models"""
    def inner(*args, **kwargs):
        endpoint, values = function(*args, **kwargs)
        try:
            return url_for(endpoint, **values)
        except BuildError:
            return
    return inner

def stamp_time():
    """Format a timestamp for display."""
    return datetime.datetime.now().strftime('%Y-%m-%d @ %H:%M')

def hash_it(username, password):
    try:
        assert isinstance(username, unicode)
    except TypeError:
        raise TypeError
    try:
        assert isinstance(password, unicode)
        m = hashlib.sha1()
        m.update(username.encode('utf-8'))
        m.update(SALT)
        m.update(password.encode('utf-8'))
        ret = m.hexdigest()
        return ret
    except TypeError:
        return False


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
