# App Info
__VERSION__ = '0.2'
__AUTHOR__ = 'Faris Chebib'

try:
    from simplejson import dumps as dump_json
except ImportError:
    from json import dumps as dump_json

from flask import Flask
from jinja2 import Environment, BaseLoader, TemplateNotFound

from synapse.settings import THEME
from flaskext.themes import setup_themes
from flaskext.babel import format_timedelta
from synapse.filters import format_date, format_datetime

#import synapse.views
from synapse.views.admin import admin
from synapse.views.frontend import frontend
#import synapse.filters

app = Flask(__name__)

class ThemeLoader(BaseLoader):
    """Forwards theme lookups to currently active theme. Ripped from zine."""
    def __init__(self, app):
        BaseLoader.__init__(self)
        self.app = app

    def get_source(self, environment, name):
        rv = self.app.theme.get_source(name)
        if rv is None:
            raise TemplateNotFound(name)
        return rv

env = Environment(loader=ThemeLoader(app),
                  extensions=['jinja2.ext.i18n'])
env.filters.update(
        json=dump_json,
        datetimeformat=format_datetime,
        dateformat=format_date,
        timedeltaformat=format_timedelta
    )

setup_themes(app)
app.register_module(admin, url_prefix="/admin")
app.register_module(frontend, url_prefix="")

from synapse.settings import SECRET_KEY, UPLOAD_FOLDER
from synapse.settings import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY
from werkzeug import SharedDataMiddleware
app.secret_key = SECRET_KEY
app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': UPLOAD_FOLDER,
    })
app.config.update(
    RECAPTCHA_PUBLIC_KEY = RECAPTCHA_PUBLIC_KEY,
    RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PRIVATE_KEY
    )

from flaskext.babel import Babel
babel = Babel(app)

