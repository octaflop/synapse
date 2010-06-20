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

class UploadPhoto(Form):
    photo = FileField(u'Photo upload', [validators.Required()])
    title_en = TextField(u"English title", [validators.Required(), validators.Length(min=3, max=50)])
    title_fr = TextField(u"French title", [validators.Required(), validators.Length(min=3, max=50)])
    description_en = TextAreaField(u"English description")
    description_fr = TextAreaField(u"French description")
    status_en = TextField(u'Current status of work in English')
    status_fr = TextField(u'Current status of work in French')
    price = TextField(u'Current price of work (leave blank if unknown)')

class ArtistForm(Form):
    unique_name = TextField(u"The unique artist's name",\
            [validators.Length(min=3, max=65)])
    first_name = TextField(u"The artist's first name",\
            [validators.Length(min=3, max=65)])
    last_name = TextField(u"The artist's last name",\
            [validators.Length(min=3, max=65)])
    bio_en = TextAreaField(u"Artist's biography in English")
    bio_fr = TextAreaField(u"Artist's biography in French")

