import os
from flask import app
from forms import LoginForm

"""
NOTE
For full settings ups: be sure to set up the "site" document along with
ininitialing the database with the init_db() command:

    >>>> from app import init_db()
    >>>> init_db()
"""

"""
Make a 'passwd.py' file and add the following
constants:
"""
from passwd import *
SECRET_KEY = 'vba937ei38mq2' ## CHANGE THIS
SALT = 'vba937ei38mq2' ## CHANGE THIS
#UPLOAD_FOLDER = '/tmp/uploads/'
UPLOAD_FOLDER = '%s/synapse/static/uploads/' % os.getcwd()
STATIC_PATH = '/static/uploads/'
USER = None
## Flask-upload manager SETTINGS
UPLOADS_DEFAULT_DEST = '/static/%s/media' % os.getcwd()
UPLOADS_DEFAULT_URL = '/static/media'

#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

TIME_ZONE = 'America/Vancouver' # Doesn't do anything, yet


