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

__VERSION__ = '0.2'
__AUTHOR__ = 'Faris Chebib'

# external deps
from flask import Flask, url_for, flash, escape, request, redirect,\
    render_template, session, abort, jsonify
from werkzeug import SharedDataMiddleware, secure_filename
from werkzeug.contrib.atom import AtomFeed
from urlparse import urljoin
import hashlib
import datetime
import os
from markdown import markdown as markdown
from PIL import Image
## from flaskext.markdown import Markdown # because I want an ajax loader...

# internal deps
from settings import *
from forms import *
from strings import *
from decorators import template, login_required
from models import Site, User, Post, TextPost, Media, FlatPage,\
        Dependency

# markdown extensions
extensions = ['footnotes', 'fenced_code']

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': UPLOAD_FOLDER,
    })

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
            self.user = None
        self.site = Site.objects.first()
        assert self.site is not None
        ## this should probably be somewhere else (in the model?)
        self.copyrightinfo = \
u"""
<a rel="license"
href="http://creativecommons.org/licenses/by-sa/2.5/ca/"><img
alt="Creative Commons License" style="border-width:0"
src="http://i.creativecommons.org/l/by-sa/2.5/ca/88x31.png" /></a><br
/>Content is released under a
[Creative Commons Attribution-ShareAlike 2.5 Canada License](http://creativecommons.org/licenses/by-sa/2.5/ca/)
"""

# Atom feed
@app.route('/feed.atom')
def atom_feed():
    meta = Meta()
    feed = AtomFeed(u'%s feed' % meta.site,
            feed_url=request.url, url=request.url_root)
    posts = Posts.query.order_by(Article.created.desc()).all()
    for post in posts:
        feed.add(post.title, unicode(post.html_content),
                content_type='html',
                author=post.author.username,
                url=make_external(post.permalink),
                updated=post.updated[0],
                published=article.created)
        return feed.get_response()

# HOME PAGE
@app.route('/')
@template('index.html')
def index():
    meta = Meta()
    posts = Post.objects()
    users = User.objects()
    selfurl = url_for('index')
    return dict(meta=meta, users=users, posts=posts)

# FLATPAGE
@app.route('/about')
@template('base.html')
def about():
    meta = Meta()
    try:
        flatpage, created = FlatPage.objects.get_or_create(title='About',\
            defaults =\
                {'content' : u"**Synapse** is a prototype of a new blogging\
                        platform. It is very alpha.",
                'created' : datetime.datetime.now(),
                'slug' : 'about',
                'slugid' : slugidfy(),
                })
        if created:
            flatpage.html_content = markdown(flatpage.content, extensions)
            flatpage.save()
    except:
        abort(404)
    return dict(meta=meta, flatpage=flatpage)

# Meta-flatpage
# Includes credits
@app.route('/cleft')
@template('cleft.html')
def cleft():
    meta = Meta()
    flatpage = FlatPage.objects
    dependencies = Dependency.objects()
    copyrightinfo = markdown(meta.copyrightinfo)
    return dict(meta=meta, flatpage=flatpage, dependencies=dependencies,\
            copyrightinfo=copyrightinfo)

# GETTERS
@app.route('/profile/<username>')
@app.route('/profile/id/<id>')
def profile(username=None, id=None):
    meta = Meta()
    user_is_home=False
    if not (username == None and id == None):
        try:
            userpage = User.objects(username=username).get()
        except:
            try:
                userpage = User.objects(id=id).get()
            except:
                return abort(404)
    else:
        return abort(404)
    if 'username' in session:
        if session['username'] == userpage.username:
            user_is_home = True
    return render_template("home.html", meta=meta,\
            userpage=userpage,user_is_home=user_is_home)

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

@app.route('/logout')
def logout():
    if 'username' in session:
        user = escape(session['username'])
        session.pop('username', None)
    else:
        return "Not logged in"
    flash("logged out: %s" % user)
    return redirect(url_for('index'))

@app.route('/login/<next>', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login(next=None):
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

#TODO
"""
make "user", "image"; etc in a tuple which is called by both the models and the view.
perhaps make a metafile to this effect.
or maybe put them in separate apps.
~foenix
"""
@template('text_post.html')
def single_text_post(year, month, day, slugid, slug=None):
    meta = Meta()
    text_post = TextPost.objects(slugid=slugid).get()
    return dict(meta=meta, text_post=text_post)

@app.route('/admin')
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

@app.route('/admin/edit/<slugid>/_title', methods=['POST', 'PUT', 'GET'])
@login_required
def add_text__title(slugid, ):
    """Ajax event to title"""
    try:
        text_post = TextPost.objects(slugid=slugid).first()
    except:
        return abort(404)
    if request.method == "PUT" or request.method == "POST":
        title = request.values.get('title', type=str)
        text_post.title = title
        text_post.updated.append(datetime.datetime.now())
        text_post.slug = slugfy(text_post.title)
        text_post.save()
        return escape(text_post.title)
    elif request.method == "GET":
        return str(text_post.title)

@app.route('/admin/edit/<slugid>/_content', methods=['POST', 'PUT', 'GET'])
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

@app.route('/post/<slugid>/<slug>/edit')
@app.route('/post/<int:year>/<int:month>/<int:day>/<slugid>/<slug>/edit')
def edit_text_ajax(slugid, year=None, month=None, day=None, slug=None):
    meta = Meta()
    try:
        text_post = TextPost.objects(slugid=slugid).first()
    except:
        return abort(404)
    return render_template("add_text_post.html", meta=meta,\
            text_post=text_post)

@login_required
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
@login_required
def add_text_post():
    meta = Meta()
    logged_in, loginform, current_user, site =\
            meta.logged_in, meta.loginform, meta.user, meta.site
    form = TextPostForm(request.form)
    if form.validate_on_submit():
        text_post = TextPost(slug=slugfy(form.title.data))
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
            flash("DBG: slug not unique")
            return redirect(url_for('add_text_post', meta=meta, form=form, site=site,\
                    loginform=loginform))
    return render_template('admin/admin_entry.html', meta=meta, form=form, site=site,\
            loginform=loginform, current_user=current_user,\
            logged_in=logged_in)

# Most reliable post retrieval url
@app.route('/post/<slugid>')
@app.route('/post/<slugid>/')
@app.route('/post/<slugid>/<slug>')
@app.route('/post/<int:year>/<int:month>/<int:day>/<slugid>/')
@app.route('/post/<int:year>/<int:month>/<int:day>/<slugid>')
@app.route('/post/<int:year>/<int:month>/<int:day>/<slugid>/<slug>')
def post_by_slugid(slugid, slug=None, year=None, month=None, day=None):
    meta = Meta()
    try:
        post = Post.objects(slugid=slugid).get()
    except:
        return abort(404)
    if (slug == None or year == None or month == None or day == None):
        return redirect(url_for('post_by_slugid', slugid=slugid,\
            slug=post.slug, year=post.created.year, month=post.created.month,
            day=post.created.day))
    post['created'] =\
        datetime.datetime.strftime(post.created,\
                                "%Y-%m-%d @ %H:%M")
    return render_template("text_post.html", meta=meta, text_post=post)

## TK returns possible collisions in slug name
@app.route('/post/<slug>')
def post_by_slug(slug):
    meta = Meta()
    text_post = TextPost.objects(slug=slug).first()
    text_post['created'] =\
        datetime.datetime.strftime(text_post.created,\
                                "%Y-%m-%d @ %H:%M")
    return render_template('text_post.html', meta=meta, text_post=text_post)

@app.route('/admin/add/image', methods=['POST', 'GET'])
def add_image():
    meta = Meta()
    form = ImagePostForm(request.form)
    if form.validate_on_submit():
        if form.image.file:
            filename = secure_filename(form.image.file.filename)
            try:
                form.image.file.save(os.path.join(UPLOAD_FOLDER, filename))
            except:
                return "error in file %s upload" % filename
            ## FIX THIS PART TK
            image = Media(title=form.title.data, author=form.author.data,\
                    description=form.description.data,\
                    slug=slugfy(form.title.data), slugid=slugidfy(),\
                    filename=filename, created=datetime.datetime.now(),\
                    published=datetime.datetime.now())
            try:
                image.save()
                return "Image uploaded successfully to slugid %s" %\
                    image.slugid
            except:
                return "Something went wrong while saving"
    return render_template('add_image.html', meta=meta, form=form)

# helper functions

# fill the initial database
def init_db():
    sites = Site.objects()
    sites.delete()
    # Should probably add something for setting up the site
    title = raw_input("What are you naming this site?\n")
    domain = raw_input("What is the site's domain?\n")
    motto = raw_input("What is the site's motto? (optional)\n")
    logo = raw_input("What is the relative path to the logo?\n \
            ex: '/static/uploads/brainBadge.png' \n")

    site = Site(title=title, motto=motto, domain=domain, logo=logo)
    try:
        site.save()
    except:
        print "Sorry, something went wrong..."
        userreponse = raw_input("try again? [Y,n]")
        if userresponse == 'Y' or userresponse == 'y' or userresponse == '\n':
            init_db()
    depends = [
            {   'title' : u'Flask',
                'url'   : u'http://flask.pocoo.org/',
                'imgurl': u'http://flask.pocoo.org/static/logo.png',
                'authors': ['Armin Ronacher'],
                },
            {   'title' : u'jQuery',
                'url'   : u'http://jquery.com/',
                'imgurl':
                u'http://static.jquery.com/files/rocker/images/logo_jquery_215x53.gif',
                'authors': ['John Resig'],
                },
            ]
    for dep in depends:
        dependency =\
        Dependency(title=dep['title'],authors=dep['authors'],url=dep['url'],\
            imgurl=dep['imgurl'])
        try:
            dependency.save()
        except:
            flash("problem")

# reset the database
def reset_db():
    try:
        posts = Post.objects()
        sites = Site.objects()
        users = User.objects()
        images = Image.objects()
        deps = Dependancy.objects()
        flatpages = FlatPage.objects()

        posts.delete()
        sites.delete()
        users.delete()
        deps.delete()
        flatpages.delete()
        return "all images, posts, sites, and users deleted successfully!"
    except:
        print "There was an error..."

# import database fixtures
def dev_site():
    """
    Deploys a "hello world" demo site with default settings
    """
    init_db()
    meta = Meta()
    # fix up a default user
    username = u'admin'
    password = u'password'
    hash = hash_it(username, password)
    email = u'admin@example.com'
    user = User(username=u'admin', hashedpassword=hash, email=email)
    user.first_name = u'Joe'
    user.last_name = u'Schmoe'
    user.save()

    # fix up a hello post
    content = u"""
**This** is an example post for the wonderful site of %s.  
This is a simple dev-post. Ready to be deleted at your leisure.  
[This](http://example.com/#) is a link.  
and  
""" % (meta.domain)
    html_content = markdown(content, extensions)
    title = u"Hello, World!"
    post = Post(title=title,content=content, html_content=html_content, author=user)
    post.slugid = slugidfy()
    post.slug = slugfy(title)
    post.save()

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5002)

