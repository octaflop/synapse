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
from flask import Flask, url_for, flash
from settings import SECRET_KEY, UPLOAD_FOLDER, SALT
from decorators import template, login_required
from werkzeug import SharedDataMiddleware, secure_filename

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
def home():
    ret = {}
    ret['user'] = 'test'
    ret['name'] = 'another test'
    ret['images'] = [{'src': 'static/img/pic1.jpg'}, \
            {'src': 'static/img/pic2.jpg'}]
    ret['url'] = url_for('home')
    flash('test')
    return ret

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        ''' l '''
        username = request.forms['username']
        password = request.forms['password']
        passhash = hash(username) * hash(password)
        if R.exists("user:%s" % passhash):
            sessions['user'] = username
    return'''
    <fieldset>
    <h1>login</h1>
    <form action="" method="POST">
    <input name='username' type='text'/>
    <input name='password' type='password' />
    </form>
    '''

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
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file></p>
      <p><input type=submit value=Upload></p>
    </form>
    '''

if __name__ == "__main__":
	app.debug = True
	app.run()

