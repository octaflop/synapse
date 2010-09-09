import os
from flask import app
from forms import LoginForm

"""
NOTE
For full settings ups: be sure to set up the "site" document.

    >>>> from models import Site
    >>>> site = Site(title=u'<site title>', motto=u'<site motto>', logo=u'<logo>',\
    >>>> domain=u'<site domain>')
"""

#from passwd import *
DEV = True
SECRET_KEY = 'vba937ei38mq2'
SALT = 'vba937ei38mq2'
#UPLOAD_FOLDER = '/tmp/uploads/'
UPLOAD_FOLDER = '%s/static/photos/' % os.getcwd()
STATIC_PATH = '/static/photos/'
USER = None
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

TIME_ZONE = 'America/Vancouver' # Doesn't do anything, yet

