# -*- encoding: utf-8 -*-
# strings.py
# all of the fiddly bits.
import re
from settings import SALT
import datetime
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

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

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

