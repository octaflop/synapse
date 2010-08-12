from wtforms import Form, BooleanField, TextField, validators, PasswordField, FileField, TextAreaField

class RegistrationForm(Form):
    username = TextField('Username', [validators.Required(), validators.Length(min=4, max=25)])
    email = TextField('Email', [validators.Required(), validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    accept_tos = BooleanField('I accept the TOS', [validators.required()])

class TextPostForm(Form):
    title = TextField('Entitle your work', [validators.required()])
    content = TextAreaField('Make your mark')
    author = TextField('Author')

class AudioPostForm(Form):
    title = TextField('Entitle your work', [validators.required(),\
        validators.Length(min=3, max=50)])
    description = TextField("Describe the audio file")
    audio = FileField('Audio upload', [validators.Required()])

class ImagePostForm(Form):
    image = FileField(u'Image upload', [validators.Required()])
    title = TextField(u"Title", [validators.Required(), validators.Length(min=3, max=50)])
    description = TextAreaField(u"English")

