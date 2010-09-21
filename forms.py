from flaskext.wtf import Form, BooleanField, TextField, validators, PasswordField, FileField, TextAreaField

## still not working
# be careful of a circular import here
from form_helper import TagListField

class RegistrationForm(Form):
    username = TextField('Username', [validators.required(), validators.length(min=4, max=25)])
    email = TextField('Email', [validators.required(), validators.length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.required(),
        validators.equal_to('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    accept_tos = BooleanField('I accept the TOS', [validators.required()])

class GenericFormAbstract(Form):
    title = TextField('Entitle your work', [validators.required(),\
        validators.length(min=3, max=50)])
    author = TextField('Author')
##    taglist = TagListField('Enter some tags, separated with a comma.')

class TextPostForm(GenericFormAbstract):
    content = TextAreaField('Make your mark')

class AudioPostForm(TextPostForm):
    description = TextField("Describe the audio file")
    audio = FileField('Audio upload', [validators.required()])

class ImagePostForm(GenericFormAbstract):
    image = FileField(u'Image upload', [validators.required()])
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

