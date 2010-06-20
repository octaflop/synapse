#!/usr/bin/env python
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

from flask import Flask, url_for, flash, escape, request, redirect,\
    render_template, session, abort
from flaskext.csrf import csrf
from settings import *
from forms import *
from strings import uurl2uuid, hash_it
import hashlib
from decorators import template, login_required
from werkzeug import SharedDataMiddleware, secure_filename
from flaskext.csrf import csrf
from mongomodels import User, Photo, Artist
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
    if 'username' in session:
        username = escape(session['username'])
        user = User.objects(username=username).first()
        ret['user'] = user.username
        ret['name'] = user.first_name
    ret['images'] = []
    ret['paths'] = []
    for photo in Photo.objects():
        ret['images'].append({'src':'%s' % photo.path})
        ret['paths'].append(photo.path)
    ret['url'] = url_for('index')
    return ret

# GETTERS
@app.route('/user/<username>')
def userpage(username):
    try:
        user = User.objects(username=username).get()
    except:
        return abort(404)

    if 'username' in session:
        return "Why hello there, %s. id:%s" % (user.username, user.id)
    else:
        return "This is %s's page. id:%s" % (user.username, user.id)

#@template('home.html')
@app.route('/home')
def home():
    username = "anon"
    if 'username' in session:
        username = escape(session['username'])
        return "Why hello there, %s." % (username)
    else:
        return "This is %s's page." % (username)

# Photo Getter
@app.route('/photo/<title>')
def photopage(title):
    photo = Photo.objects(title=title).first()
    if photo is not None:
        return "Filename: %s, title: %s, id: %s" % (photo.filename, photo.title,\
            photo.id)
    else:
        return abort(404)


@app.route('/photo/raw/<title>')
def raw_photo(title):
    """
    The method to get photos referred by the database and stored unto the
    machine
    """
    try:
        photo = Photo.objects(title=title).first()
    except:
        return "not found"
    return url_for('static', filename=photo.filename)

# User Functions
@app.route('/admin/add/user', methods=['GET', 'POST'])
@login_required
def register_user():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        password = form.password.data
        user.hashedpassword = hash_it(form.username.data, form.password.data)
        if user.save():
            session['username'] = user.username
            flash("user: %s was added successfully" % user.username)
            return redirect(url_for('userpage', username=user.username))
        else:
            return "could not find user after adding"
    else:
        return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    if 'username' in session:
        user = escape(session['username'])
        session.pop('username', None)
    else:
        return "Not logged in"
    flash("logged out: %s" % user)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    ret = {}
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        given_passhash = hash_it(username, password)
        try:
            user = User.objects(username=username, hashedpassword=given_passhash).first()
        except:
            flash("Not found")
            return redirect('login')
        session['username'] = user.username
        return redirect(url_for('userpage', username=user.username))
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

@app.route('/admin/add/artist', methods=['POST', 'GET'])
def add_artist():
    form = ArtistForm(request.form)
    if request.method == 'POST' and form.validate():
        artist = Artist(unique_name=form.unique_name.data)
        artist.unique_name = form.unique_name.data
        artist.first_name = form.first_name.data
        artist.last_name = form.last_name.data
        artist.bio_en = form.bio_en.data
        artist.bio_fr = form.bio_fr.data
        if artist.save():
            flash("%s was saved successfully to id: %s" % (artist.unique_name,\
                artist.id))
            return redirect(url_for('artistpage', unique_name=artist.unique_name))
        else:
            flash("username not unique")
            return redirect(url_for('add_artist'))
    return render_template('add_artist.html', form=form)

@app.route('/artist/<unique_name>')
def artistpage(unique_name):
    try:
        artist = Artist.objects(unique_name=unique_name).first()
    except:
        return abort(404)
    return "first name: %s" % artist.first_name

@app.route('/admin/add/photo', methods=['POST', 'GET'])
def add_photo():
    form = UploadPhoto(request.form)
    if request.method == "POST":
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            photo = Photo(title=form.title_en.data,\
                    title_en=form.title_en.data, title_fr=form.title_fr.data,\
                    filename=filename)
            try:
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                photo.path = unicode(STATIC_PATH) + unicode(filename)
                photo.save()
                return redirect(url_for('photopage', title=photo.title))
            except:
                return "Error of some sort"
    return render_template('add_photo.html', form=form)

if __name__ == "__main__":
    app.debug = True
    csrf(app) #TODO
    app.run(host="0.0.0.0", port=5002)

