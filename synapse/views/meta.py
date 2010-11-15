from flask import session, escape, request
from flaskext.themes import Theme, render_theme_template
# from synapse.strings import *
from synapse.forms import LoginForm
from synapse.models import User, Site
from synapse.settings import THEME

def get_current_theme():
    if THEME is not None:
        ident = THEME
    else:
        ident = 'plain'
    return get_theme(ident)

def render(template, **context):
    return render_theme_template(get_current_theme(), template, **context)

# META
class Meta:
    """
    The meta class is called for all base-page requests.
    This includes the theme mangement options
    """
    def __init__(self):
        self.logged_in = False
        self.loginform = LoginForm(request.form)
        if 'username' in session:
            self.username = escape(session['username'])
            self.user = User.objects(username=self.username).first()
            if not self.user == None:
                self.logged_in = True
        else:
            self.user = None
        self.site = Site.objects.first()
        ## this should probably be somewhere else (in the model?)
        self.footy = {}
        copyrightinfo_html = \
u"""
<a rel="license"
href="http://creativecommons.org/licenses/by-sa/2.5/ca/"><img
alt="Creative Commons License" style="border-width:0"
src="http://i.creativecommons.org/l/by-sa/2.5/ca/88x31.png" /></a><br
/>Content is released under a
<a href='http://creativecommons.org/licenses/by-sa/2.5/ca/'>Creative Commons
Attribution-ShareAlike 2.5 Canada License</a>
"""
        self.footy['copyrightinfo'] = copyrightinfo_html
        # May want to set up a model from the flatpages.
        self.footy['links'] = [{\
                'title' : u"github page",
                'url' : u"http://github.org/octaflop/synapse"
                }]

