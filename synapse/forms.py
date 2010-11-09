from flaskext.wtf import Form, BooleanField, TextField, validators,\
PasswordField, FileField, TextAreaField, DateTimeField, RecaptchaField,\
HiddenField, DateField

from flaskext.babel import gettext as _
from flaskext.babel import ngettext as _n

## still not working. wish it were. TK
# be careful of a circular import here
#from form_helper import TagListField

class RegistrationForm(Form):
    username_msg = _(u'Username')
    username = TextField(username_msg, [validators.required(), validators.length(min=4, max=25)])
    email_msg = _(u'Email')
    email = TextField(email_msg, [validators.required(), validators.length(min=6, max=35)])
    password_msg = _(u'Password')
    password = PasswordField(password_msg, [
        validators.required(),
        validators.equal_to('confirm', message='Passwords must match')
        ])
    repeat_password_msg = _(u'Please repeat the password')
    confirm = PasswordField(repeat_password_msg)
    accept_msg = _(u"I accept the <a href='/terms'>Terms of Registration</a>")
    accept_tos = BooleanField(accept_msg, [validators.required()])

class GenericFormAbstract(Form):
    title = TextField('Entitle your work', [validators.required(),\
        validators.length(min=3, max=50)])
    author = TextField('Author')
    #taglist = TagListField('Enter some tags, separated with a comma.')
    published_date = DateField('Date to publish');
    published_time = TextField('Time to publish, use 24-hour time.');
    is_published = BooleanField('Publish');

class TextPostForm(GenericFormAbstract):
    content = TextAreaField('Make your mark')
    media = HiddenField(u'')

class AudioPostForm(TextPostForm):
    description = TextField("Describe the audio file")
    audio = FileField('Audio upload', [validators.required()])

class ImagePostForm(GenericFormAbstract):
    image = FileField(u'Image upload')#, [validators.required()])
    description = TextAreaField(u"Image description")

class LoginForm(Form):
    username = TextField(u'Username', [validators.required()])
    password = PasswordField(u'Password')

class SitePostForm(Form):
    title = TextField(u'Site title (the banner)', [validators.required()])
    motto = TextField(u'Site motto (below the banner)')
    domain = TextField(u"domain of site (leave off 'http'; eg\
            example.com:5001)", [validators.required()])
    logo = FileField(u'Logo upload')

class DepPostForm(Form):
    title = TextField(u'Software title', [validators.required()])
    url = TextField(u"url of dependency", [validators.required()])
    imgurl = TextField(u"url of dependency logo")
    # authors = TagListField(u"Author names, separated with a comma")

class WallForm(Form):
    content = TextAreaField(u"", [validators.required()])
    username = TextField(u"please enter a username", [validators.required()])
    recaptcha = RecaptchaField(u"Mutually beneficial turing-test")
