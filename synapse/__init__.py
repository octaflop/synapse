# App Info
__VERSION__ = '0.2'
__AUTHOR__ = 'Faris Chebib'

from flask import Flask
from synapse.views.frontend import frontend
from flaskext.babel import Babel

from synapse.settings import SECRET_KEY, UPLOAD_FOLDER
from synapse.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
from werkzeug import SharedDataMiddleware

#import synapse.views

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': UPLOAD_FOLDER,
    })
app.config.update(
    RECAPTCHA_PUBLIC_KEY = RECAPTCHA_PUBLIC_KEY,
    RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PRIVATE_KEY
    )

babel = Babel(app)

app.register_module(frontend)
