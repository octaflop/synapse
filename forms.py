from flaskext.wtf import Form, BooleanField, TextField, validators, PasswordField, FileField, TextAreaField

class RegistrationForm(Form):
    username = TextField('Username', [validators.required(), validators.length(min=4, max=25)])
    email = TextField('Email', [validators.required(), validators.length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.required(),
        validators.equal_to('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    accept_tos = BooleanField('I accept the TOS', [validators.required()])

class TextPostForm(Form):
    title = TextField('Entitle your work', [validators.required()])
    content = TextAreaField('Make your mark')
    author = TextField('Author')

class AudioPostForm(Form):
    title = TextField('Entitle your work', [validators.required(),\
        validators.length(min=3, max=50)])
    description = TextField("Describe the audio file")
    audio = FileField('Audio upload', [validators.required()])

class ImagePostForm(Form):
    image = FileField(u'Image upload', [validators.required()])
    title = TextField(u"Title", [validators.required(), validators.length(min=3, max=50)])
    description = TextAreaField(u"English")

class LoginForm(Form):
    username = TextField(u'Username', [validators.required()])
    password = PasswordField(u'Password')
