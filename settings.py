from passwd import *
DEV = True
SECRET_KEY = 'vba937ei38mq2'
SALT = 'vba937ei38mq2'
UPLOAD_FOLDER = '/tmp/uploads/'
g = {}
g['user'] = None
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

TIME_ZONE = 'America/Vancouver' # Doesn't do anything, yet
