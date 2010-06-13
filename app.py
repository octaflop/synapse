#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright © 2010 Faris Chebib
#
# This file is part of aliendog.
#
# aliendog is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# aliendog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with aliendog; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

from models import R
from flask import Flask, url_for, flash, escape, request, redirect,\
    render_template, session
from settings import *
from forms import *
from strings import uurl2uuid, hash_it
import hashlib
from decorators import template, login_required
from werkzeug import SharedDataMiddleware, secure_filename
from flaskext.csrf import csrf
from models import User, Artist, Photo
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': UPLOAD_FOLDER,
    })

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# HOME PAGE
@app.route('/')
@template('index.html')
def index():
    ret = {}
    ret['user'] = 'test'
    ret['name'] = 'another test'
    #ret['images'] = [{'src': 'static/img/pic1.jpg'}, \
    #        {'src': 'static/img/pic2.jpg'}]
    files = os.listdir(UPLOAD_FOLDER)
    ret['images'] = []
    for f in files:
        ret['images'].append({'src':'/uploads/%s' % f})
    ret['url'] = url_for('index')
    flash('test')
    return ret

# GETTERS
@app.route('/user/<uurl>')
def userpage(uurl):
    uuid = uurl2uuid('user', uurl)
    if uuid is None:
        return "uuid not found"
    user = User(unicode(uurl))
    user.kind = 'user'
    user.uuid = str(uuid)
    user.get(user.kind, user.uuid)
    username = user.attrs['username']
    uuid = user.attrs['uuid']
    if session['username'] == username:
        return "Why hello there, %s. id:%s" % (username, uuid)
    else:
        return "This is %s's page. id:%s" % (username, uuid)

#@template('home.html')
@app.route('/home')
def home():
    username = "anon"
    if 'username' in session:
        username = escape(session(username))
        return "Why hello there, %s." % (username)
    else:
        return "This is %s's page." % (username)

# Photo Getter
@app.route('/photo/raw/<uuid>')
def raw_photo(uuid):
    """
    The method to get photos referred by the database and stored unto the
    machine
    """
    photo = Photo()
    photo.get(kind='photo', uuid=uuid)
    return photo._full_url()

# User Functions
@app.route('/admin/add/user', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, form.password.data)
        if user.post():
            if user.get():
                session['username'] = user.username
                session['uuid'] = user.uuid
                return redirect(url_for('user'), uurl=user.uurl)
            else:
                return "could not find user after adding"
        else:
            return "could not add user to server"
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    if 'username' in session:
        user = escape(session['username'])
    else:
        session['username'] = 'anon'
    flash("logged out: %s" % user)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    ret = {}
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        given_passhash = hash_it(username, password)
        # pseudouser = an unverified user
        pseudouser = User(username)
        pseudouser.kind = 'user'
        pseudouser.password = password
        pseudouser.uuid = uurl2uuid('user', pseudouser.username)
        if pseudouser._check_credentials():
            # TODO: THIS MAY NOT WORK
            # (naming conflicts may happen with the same username;
            # going to resolve with intersecting sets)
            pseudouser.get()
            # user => the server's gotten and verified user
            user = pseudouser
            session['username'] = user.username
            session['uuid'] = user.uuid
            return redirect(url_for('user'), uurl=user.uurl)
    return render_template('login.html', ret=ret)


#TODO
"""
make "user", "photo"; etc in a tuple which is called by both the models and the view.
perhaps make a metafile to this effect.
or maybe put them in separate apps.
~foenix
"""
@app.route('/admin')
@template('admin.html')
def admin():
    artist_form = ArtistForm(request.form)
    photo_form = UploadPhoto(request.form)
    user_form = RegistrationForm(request.form)

    return dict(artist_form=artist_form, photo_form=photo_form,\
            user_form=user_form)

@app.route('/admin/add/artist', methods=['POST'])
def add_artist():
    kwargs = {}
    return render_template('add_artist.html', kwargs)

@app.route('/admin/add/photo', methods=['POST'])
def add_photo():
    form = UploadPhoto(request.form)
    photo = Photo(form.title_en.data, form.title_fr.data)
    if request.method == "POST":
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            photo.attrs = {
                    'description_en' : form.description_en.data,
                    'description_fr' : form.description_fr.data,
                    'status_en' : form.status_en.data,
                    'status_fr' : form.status_fr.data,
                    'price' : form.price.data
                    }
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            photo.post()
            return redirect(url_for('raw_photo', uuid=photo.uuid))
    return render_template('add_photo.html')

if __name__ == "__main__":
    app.debug = True
    ## csrf(app) TODO
    app.run(host="0.0.0.0", port=5002)

