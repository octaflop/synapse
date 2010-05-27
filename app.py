#! /usr/bin/env python
# -*- coding: utf8 -*-
# -*- coding: utf-8 -*-
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
from flask import Flask, url_for, flash, escape, request, redirect, session, render_template
from settings import *
from forms import *
from decorators import template, login_required
from werkzeug import SharedDataMiddleware, secure_filename
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': UPLOAD_FOLDER
    })

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        passhash = hash(form.username.data) * hash(form.password.data)
        uid = R.zincr("global.uid", 1)
        username = R.set("user:%s:username" % uid, form.username.data)
        passhash = R.set("user:%s:passhash" % uid, passhash)
        email = R.set("user:%s:email" % uid, form.email.data)
        if not R.sadd('users', 'user:%s' % uid):
            return "username taken"
        else:
            R.set('user:%s' % passhash, uid)
            session['username'] = username
            flash("Thanks for registering")
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    user = session['username']
    if session['username'] == None:
        return "you are not logged in"
    else:
        session['username'] = None
        flash("logged out: %s" % user)
        return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    ret = {}
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        passhash = hash(unicode(username)) * hash(unicode(password))
        if R.exists("user:%s" % passhash):
            session['passhash'] = passhash
            uid = R.get('user:%s' % passhash)
            session['username'] = R.get("user:%s:username" % uid)
            flash("logged in successfully as: %s" % session['username'])
            return redirect(url_for('index'))
        else:
            flash("Wrong username or password")
            return redirect('login')
    return render_template('login.html', ret=ret)

@app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == "POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('upload', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new file</title>
    <h1>Upload a new file</h1>
    <form action="" method=post enctype='multipart/form-data'>
      <p><input type=file name='file'></p>
      <p><input type=submit value='Upload'></p>
    </form>
    '''

if __name__ == "__main__":
	app.debug = False
	app.run(host='0.0.0.0', port=5001)

