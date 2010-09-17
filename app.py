#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright © 2010 Faris Chebib
#
# This file is part of synapse.
#
# synapse is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# synapse is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with synapse; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

from flask import Flask, url_for, flash, escape, request, redirect,\
    render_template, session, abort, jsonify
from flaskext.markdown import Markdown
from settings import *
from forms import *
from strings import *
import hashlib
import datetime
from decorators import template, login_required
from werkzeug import SharedDataMiddleware, secure_filename
from models import Site, User, Post, TextPost, AudioPost, ImagePost
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

# META
class Meta:
    def __init__(self):
        self.logged_in = False
        self.loginform = LoginForm(request.form)
        if 'username' in session:
            self.username = escape(session['username'])
            self.user = User.objects(username=self.username).first()
            self.logged_in = True
        else:
            self.user = "anonymous"
        self.site = Site.objects.first()
        assert self.site is not None

# HOME PAGE
@app.route('/')
@template('index.html')
def index():
    meta = Meta()
    logged_in, loginform, user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    posts = Post.objects()
    users = User.objects()
    selfurl = url_for('index')
    return dict(loginform=loginform, current_user=user, users=users,\
            posts=posts, site=site, selfurl=selfurl, logged_in=logged_in)

# GETTERS
@app.route('/profile/<username>')
@app.route('/profile/id/<id>')
def profile(username=None, id=None):
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    if not (username == None and id == None):
        try:
            user = User.objects(username=username).get()
        except:
            try:
                user = User.objects(id=id).get()
            except:
                return abort(404)
    else:
        return abort(404)
    if session['username'] == user.username:
        user_is_home = True
    return render_template("home.html", current_user=current_user,user=user,
            loginform=loginform, site=site, logged_in=logged_in,
            user_is_home=user_is_home)

@template('home.html')
def user_by_id(id):
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    try:
        user = User.objects(id=id).first()
        ret = {
                'username': user.username,
                'id': user.id,
                }
    except:
        return abort(404)
    return dict(user=ret, loginform=loginform, site=site,\
            current_user=current_user)

# Image Getter
@app.route('/image/<title>')
def imagepage(title):
    image = Image.objects(title=title).first()
    if image is not None:
        return "Filename: %s, title: %s, id: %s" % (image.filename, photo.title,\
            image.id)
    else:
        return abort(404)

@app.route('/image/raw/<title>')
def raw_image(title):
    """
    The method to get images referred by the database and stored unto the
    machine
    """
    try:
        image = Image.objects(title=title).first()
    except:
        return "not found"
    return url_for('static', filename=image.filename)

# User Functions
@app.route('/admin/add/user', methods=['GET', 'POST'])
#@login_required
def register_user():
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    user_form = RegistrationForm(request.form)
    if user_form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        password = form.password.data
        user.hashedpassword = hash_it(form.username.data, form.password.data)
        try:
            user.save()
            session['username'] = user.username
            flash("user: %s was added successfully" % user.username)
            return redirect(url_for('profile', username=user.username))
        except:
            flash("could not find user after adding")
            return redirect(url_for('login'))
    else:
        return render_template('register.html', user_form=user_form,\
                loginform=loginform, site=site, current_user=current_user)

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
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        given_passhash = hash_it(username, password)
        user = User.objects(username=username, hashedpassword=given_passhash).first()
        if user is not None:
            flash("%s is logged in" % user.username)
            session['username'] = user.username
            return redirect(url_for('profile', username=user.username))
        else:
            flash("Not found")
            return redirect('login')
    if 'username' in session:
        user = User.objects(username=escape(session['username'])).first()
        if user is not None:
            return redirect(url_for('profile', username=user.username))
        else:
            abort(500)
    return render_template('login.html', form=form, loginform=form, site=site,\
            current_user=current_user)

#TODO
"""
make "user", "image"; etc in a tuple which is called by both the models and the view.
perhaps make a metafile to this effect.
or maybe put them in separate apps.
~foenix
"""
@app.route('/<year>/<month>/<day>/<slug>')
@template('text_post.html')
def single_text_post(year, month, day, slug):
    text_post = TextPost.objects(slug=slug).first()
    ret = {
            'title': text_post.title,
            'content': text_post.content,
            }
    return dict(text_post=ret)

@app.route('/admin')
@template('admin/admin.html')
def admin():
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    user_form = RegistrationForm(request.form)
    text_post_form = TextPostForm(request.form)
    audio_post_form = AudioPostForm(request.form)
    image_post_form = ImagePostForm(request.form)
    site_post_form = SitePostForm(request.form)
    return dict(user_form=user_form, text_post_form=text_post_form,\
            audio_post_form=audio_post_form, image_post_form=image_post_form,\
            site=site, loginform=loginform, current_user=current_user,\
            site_post_form=site_post_form, logged_in=logged_in)

@app.route('/admin/edit/<slug>/_title', methods=['POST', 'PUT', 'GET'])
def add_text__title(slug):
    """Ajax event to title"""
    try:
        text_post = TextPost.objects(slug=slug).first()
    except:
        return error(404)
    if request.method == "PUT" or request.method == "POST":
        title = request.values.get('title', type=str)
        text_post.title = title
        text_post.save()
        #return jsonify(text_post.title)
        return text_post.title
    elif request.method == "GET":
        return str(text_post.title)

@app.route('/admin/edit/<slug>/_content', methods=['POST', 'PUT', 'GET'])
def add_text__content(slug):
    """Ajax event & markdown for content"""
    try:
        text_post = TextPost.objects(slug=slug).first()
    except:
        return error(404)
    if request.method == "PUT" or request.method == 'POST':
        content = request.values.get('content', type=str)
        text_post.content = content
        text_post.save()
        return text_post.content
    elif request.method == "GET":
        try:
            return text_post.content
        except:
            return abort(500)

@app.route('/post/<slug>/edit')
def edit_text_ajax(slug):
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    try:
        text_post = TextPost.objects(slug=slug).first()
    except:
        return error(404)
    return render_template("add_text_post.html", text_post=text_post,\
            loginform=loginform, site=site, current_user=current_user,\
            logged_in=logged_in)

@app.route('/admin/add/site', methods=['POST'])
def add_site():
    form = SitePostForm(request.form)
    if form.validate_on_submit():
        site = Site(title=form.title.data, domain=form.domain.data)
        site.motto = form.motto.data
        if form.logo.file:
            filename = secure_filename(form.logo.file.filename)
            try:
                form.logo.file.save(os.path.join(UPLOAD_FOLDER, filename))
                site.logo = STATIC_PATH + filename
            except:
                flash("error in file %s upload" % filename)
        prev_site = Site.objects.first()
        if prev_site is not None:
            prev_site.title = site.title
            prev_site.motto = site.motto
            prev_site.domain = site.domain
            prev_site.logo = site.logo
            site = prev_site
        try:
            site.save()
            return redirect(url_for('admin'))
        except:
            flash("there was an error saving site %s" % site.title)
            return redirect(url_for('admin'))
    else:
        flash("There was an error with your submission")
        return redirect(url_for('admin'))


@app.route('/admin/add/text', methods=['POST', 'GET'])
def add_text_post():
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    form = TextPostForm(request.form)
    if form.validate_on_submit():
        text_post = TextPost(slug=slugfy(form.title.data))
        text_post.date_created = datetime.datetime.now()
        text_post.title = escape(form.title.data)
        text_post.content = escape(form.content.data)
        try:
            text_post.save()
            flash("%s was successfully saved as id %s" % (text_post.title,\
                text_post.id))
            return redirect(url_for('text_post', slug=text_post.slug))
        except:
            flash("DBG: slug not unique")
            return redirect(url_for('add_text_post', form=form, site=site,\
                    loginform=loginform))
    return render_template('admin/admin_entry.html', form=form, site=site,\
            loginform=loginform, current_user=current_user,\
            logged_in=logged_in)

@app.route('/post/<slug>')
def post(slug):
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    text_post = TextPost.objects(slug=slug).first()
    text_post['date_created'] =\
        datetime.datetime.strftime(text_post.date_created,\
                                "%Y-%m-%d @ %H:%M")
    return render_template('text_post.html', text_post=text_post,\
            loginform=loginform, site=site, current_user=current_user,\
            logged_in=logged_in)

@app.route('/admin/add/artist', methods=['POST', 'GET'])
def add_artist():
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    form = ArtistForm(request.form)
    if form.validate_on_submit():
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
    return render_template('add_artist.html', form=form, loginform=loginform,\
            logged_in=logged_in, current_user=current_user)

@app.route('/artist/<unique_name>')
def artistpage(unique_name):
    try:
        artist = Artist.objects(unique_name=unique_name).first()
    except:
        return abort(404)
    return "first name: %s" % artist.first_name

@app.route('/admin/add/image', methods=['POST', 'GET'])
def add_image():
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    form = UploadImage(request.form)
    if request.method == "POST":
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image = Image(title=form.title_en.data,\
                    title_en=form.title_en.data, title_fr=form.title_fr.data,\
                    filename=filename)
            try:
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                image.path = unicode(STATIC_PATH) + unicode(filename)
                image.save()
                return redirect(url_for('imagepage', title=photo.title))
            except:
                return "Error of some sort"
    return render_template('add_image.html', form=form, loginform=loginform,\
            logged_in=logged_in, current_user=current_user)

if __name__ == "__main__":
    app.debug = True
    Markdown(app)
    app.run(host="0.0.0.0", port=5002)

