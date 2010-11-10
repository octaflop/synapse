#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# bootstrap module
from flask import Module

admin = Module(__name__)

# Meta
from synapse.views.meta import Meta

from flask import url_for, flash, escape, request, redirect,\
    render_template, session, abort, jsonify
from werkzeug import SharedDataMiddleware, secure_filename
from urlparse import urljoin
import hashlib
import datetime
import os
from markdown import markdown as markdown
from PIL import Image as Picture
# internal deps
from synapse.settings import *
from synapse.forms import *
from synapse.strings import *
from synapse.decorators import *
# Models
from synapse.models import Site, User, Post, TextPost, Media, FlatPage,\
        Dependency, Image, Wall

# markdown extensions
#extensions = ['footnotes', 'fenced_code']
extensions = ['footnotes', 'codehilite']

# Authentication Methods

##@admin.route('/login/<url:next>', methods=['GET','POST'])
@admin.route('/login', methods=['GET','POST'])
def login(next=None):
    """Login Function. Upcoming "next" function"""
    meta = Meta()
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
    return render_template('login.html', meta=meta, form=form)


@admin.route('/logout')
def logout():
    if 'username' in session:
        user = escape(session['username'])
        session.pop('username', None)
    else:
        return "Not logged in"
    flash("logged out: %s" % user)
    return redirect(url_for('.index'))

# CRUD: Create Read Update Delete
# or CRRUMD: Create Read/Relate Update/Manage Delete
# User Functions
@admin.route('/admin/add/user', methods=['GET', 'POST'])
@login_required
def register_user():
    meta = Meta()
    user_form = RegistrationForm(request.form)
    if user_form.validate_on_submit():
        user = User(username=user_form.username.data, email=user_form.email.data)
        password = user_form.password.data
        user.hashedpassword = hash_it(user_form.username.data, password)
        try:
            user.save()
            if not 'username' in session:
                session['username'] = user.username
            flash("user: %s was added successfully" % user.username)
            return redirect(url_for('profile', username=user.username))
        except:
            flash("could not find user after adding")
            return redirect(url_for('login'))
    else:
        return render_template('register.html', meta=meta, user_form=user_form)

@admin.route('/admin/manage')
@login_required
@template('admin/manage.html')
def manage():
    flats = FlatPage.objects()
    posts = Post.objects()
    images = Image.objects()
    return dict(posts=posts, images=images, flats=flats)

@admin.route('/admin')
@login_required
@template('admin/admin.html')
def admin():
    meta = Meta()
    user_form = RegistrationForm(request.form)
    text_post_form = TextPostForm(request.form)
    audio_post_form = AudioPostForm(request.form)
    image_post_form = ImagePostForm(request.form)
    site_post_form = SitePostForm(request.form)
    return dict(meta=meta,user_form=user_form,\
            text_post_form=text_post_form,\
            audio_post_form=audio_post_form,\
            image_post_form=image_post_form,\
            site_post_form=site_post_form)

@admin.route('/edit/<slugid>/_title', methods=['POST', 'PUT', 'GET'])
@login_required
def add_text__title(slugid):
    """Ajax event to title"""
    try:
        text_post = TextPost.objects(slugid=slugid).first()
    except:
        return abort(404)
    if request.method == "PUT" or request.method == "POST":
        title = request.values.get('title', type=unicode)
        text_post.title = title
        if text_post.updated:
            text_post.updated.append(datetime.datetime.now())
        else:
            text_post.updated = [datetime.datetime.now()]
        text_post.slug = slugfy(unicode(title))
        text_post.save()
        return text_post.title
    elif request.method == "GET":
        return text_post.title

@admin.route('/admin/edit/<slugid>/_content', methods=['POST', 'PUT', 'GET'])
@login_required
def add_text__content(slugid):
    """Ajax event & markdown for content"""
    try:
        text_post = TextPost.objects(slugid=slugid).get()
    except:
        return abort(404)
    if request.method == "PUT" or request.method == 'POST':
        content = request.values.get('content')
        text_post.content = content
        text_post.html_content = markdown(content, extensions)
        text_post.updated.append(datetime.datetime.now())
        text_post.save()
        return text_post.html_content
    elif request.method == "GET":
        try:
            return text_post.content
        except:
            return abort(500)

@admin.route('/post/<slugid>/edit')
@admin.route('/post/<slugid>/<slug>/edit')
@admin.route('/post/<int:year>/<int:month>/<int:day>/<slugid>/<slug>/edit')
def edit_text_ajax(slugid, year=None, month=None, day=None, slug=None):
    meta = Meta()
    try:
        text_post = TextPost.objects(slugid=slugid).get()
    except:
        return abort(404)
    if (slug == None or year == None or month == None or day == None):
        return redirect(url_for('edit_text_ajax', slugid=slugid,\
            slug=text_post.slug, year=text_post.created.year,\
            month=text_post.created.month, day=text_post.created.day))
    return render_template("add_text_post.html", meta=meta,\
            text_post=text_post)

@admin.route('/<slugid>/delete')
@login_required
def delete_post(slugid):
    try:
        asset = Post.objects(slugid=slugid).get()
    except:
        error(404)
    try:
        slugid = asset.slugid
        title = asset.title
        asset.delete()
        flash("Post '%s'. With slugid '%s' was deleted." % (title, slugid))
    except:
        error(404)
    return redirect(url_for('admin'))

## TK Fix this. Use the proper mongo method...
@login_required
@admin.route('/admin/add/site', methods=['POST'])
def add_site():
    form = SitePostForm(request.form)
    if form.validate_on_submit():
        prev_site = Site.objects.first()
        if prev_site is not None:
            prev_site.delete()
        site = Site(title=form.title.data, domain=form.domain.data,\
                motto=form.motto.data)
        if form.logo.file:
            filename = secure_filename(form.logo.file.filename)
            size = 190,190
            try:
                os.chdir(os.path.join(UPLOAD_FOLDER, 'orig'))
                form.logo.file.save(filename)
                image = Picture.open(filename)
                os.chdir('../medium')
                image.thumbnail(size, Picture.ANTIALIAS)
                image.save(filename)
                site.logo = os.path.join(STATIC_PATH, 'medium', filename)
            except:
                flash("error in file: %s's upload" % filename)
        try:
            site.save()
            return redirect(url_for('admin'))
        except:
            flash("there was an error saving site %s" % site.title)
            return redirect(url_for('admin'))
    else:
        flash("There was an error with your submission")
        return redirect(url_for('admin'))

@admin.route('/admin/add/text', methods=['POST', 'GET'])
@login_required
def add_text_post():
    meta = Meta()
    form = TextPostForm(request.form)
    if form.validate_on_submit():
        username = escape(session['username'])
        text_post = TextPost(slug=slugfy(form.title.data))
        text_post.is_published = form.is_published.data
        try:
            text_post.author = User.objects(username=username).get()
        except:
            flash("user not found")
            return redirect(url_for('add_text_post', meta=meta, form=form))
        # Media ripping method
        def rip_media(mediastr):
            try:
                assert len(mediastr) % 8 == 0
            except:
                flash("could not save media %s " % escape(form.media.data))
            ret = []
            for i in range(len(mediastr) / 8):
                ret.append(mediastr[i*8:(i+1)*8])
            return ret
        if form.media.data:
            media = rip_media(form.media.data)
            if media:
                for j in range(len(media)):
                    med = Media.objects(slugid=media[j]).get()
                    text_post.media.append(med)
        published_time = escape(form.published_time.data)
        published_date = escape(form.published_date.data)
        published = "%s %s" % (published_date, published_time)
        datetimeformat = "%Y-%m-%d %H:%M"
        published = datetime.datetime.strptime(published, datetimeformat)
        text_post.published = published
        text_post.created = datetime.datetime.now()
        text_post.title = escape(form.title.data)
        text_post.content = escape(form.content.data)
        text_post.html_content = markdown(text_post.content, extensions)
        text_post.slugid = slugidfy()
        try:
            text_post.save()
            flash("%s was successfully saved as slugid %s" % (text_post.title,\
                text_post.slugid))
            return redirect(url_for('post_by_slugid', slugid=text_post.slugid))
        except:
            flash("Error: Post was not saved")
            return redirect(url_for('add_text_post', meta=meta, form=form))
    return render_template('admin/admin_entry.html', meta=meta, form=form)

@admin.route('/admin/add/image', methods=['POST', 'GET'])
def add_image():
    meta = Meta()
    form = ImagePostForm(request.form)
    if form.validate_on_submit():
        if form.image.file:
            filename = secure_filename(form.image.file.filename)
            try:
                os.chdir(os.path.join(UPLOAD_FOLDER, 'orig'))
                slugid = slugidfy()
                filename = "%s_%s%s" % (filename[:-4], slugid, filename[-4:])
                form.image.file.save(filename)
                orig = os.path.join(STATIC_PATH, 'orig', filename)
                path = os.path.join(UPLOAD_FOLDER, 'orig', filename)
                image = Picture.open(path)
                # small images
                size = 100,100
                os.chdir('../small')
                image.thumbnail(size, Picture.ANTIALIAS)
                image.save(filename)
                small = os.path.join(STATIC_PATH, 'small', filename)
                image = Picture.open(path)
                # medium images
                size = 200,200
                os.chdir('../medium')
                image.thumbnail(size, Picture.ANTIALIAS)
                image.save(filename)
                medium = os.path.join(STATIC_PATH, 'medium', filename)
                image = Picture.open(path)
                # large images
                size = 650,650
                os.chdir('../large')
                image.thumbnail(size, Picture.ANTIALIAS)
                image.save(filename)
                large = os.path.join(STATIC_PATH, 'large', filename)
            except:
                return "error in file %s upload" % filename
            image = Image(
                title=form.title.data, \
                author=User.objects(username=form.author.data).get(),\
                description=form.description.data,\
                slug=slugfy(form.title.data), slugid=slugid,\
                filename=filename, created=datetime.datetime.now(),\
                published=datetime.datetime.now(),\
                path=path,\
                orig=orig,\
                small=small,\
                medium=medium,\
                large=large
                )
            try:
                image.save()
                #return jsonify(slugid=image.slugid)
                return image.slugid
            except:
                return "Something went wrong while saving"
    return render_template('add_image.html', meta=meta, form=form)


