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

#from passwd import *
DEV = True
SECRET_KEY = 'vba937ei38mq2'
SALT = 'vba937ei38mq2'
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

## RECAPTCHA SETTINGS
RECAPTCHA_PUBLIC_KEY = "6Lf0JL0SAAAAAG1SCgtzqjEyFhG63Xp0FtXmoktb"
RECAPTCHA_PRIVATE_KEY = "6Lf0JL0SAAAAAEVVxQaOrrZoZoEx8n1EaU0Ad_bQ"

