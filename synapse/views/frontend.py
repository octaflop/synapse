#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# bootstrap module
from flask import Module

frontend = Module(__name__)
admin = Module(__name__)

# external deps
from flask import url_for, flash, escape, request, redirect,\
    render_template, session, abort, jsonify
from werkzeug.contrib.atom import AtomFeed
from urlparse import urljoin
import hashlib
import datetime
import os
from markdown import markdown as markdown
## from flaskext.markdown import Markdown # because I want an ajax loader...

# internal deps
from synapse.settings import *
from synapse.forms import *
from synapse.strings import *
from synapse.decorators import template, login_required
# Meta
from synapse.views.meta import Meta

from synapse.models import Site, User, Post, TextPost, Media, FlatPage,\
        Dependency, Image, Wall

# markdown extensions
#extensions = ['footnotes', 'fenced_code']
extensions = ['footnotes', 'codehilite']

# Atom feed
@frontend.route('/feed.atom')
def atom_feed():
    def make_external(url):
        return urljoin(request.url_root, url)
    meta = Meta()
    feed = AtomFeed(u'%s feed' % meta.site,\
            feed_url=request.url, url=request.url_root)
    posts = Post.objects()
    for post in posts:
        feed.add(post.title, unicode(post.html_content),\
                content_type='html',\
                author=post.author.username,\
                url=make_external(url_for('post_by_slugid',\
                    slugid=post.slugid)),
                updated=post.updated[0],\
                published=post.created)
    return feed.get_response()

# HOME PAGE
@frontend.route('/')
@template('index.html')
def index():
    meta = Meta()
    posts = Post.objects()
    #posts = Post.live()
    users = User.objects()
    images = Image.objects()
    return dict(meta=meta, users=users, posts=posts, images=images)

# FLATPAGE
@frontend.route('/about')
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

# Wall
@frontend.route('/wall')
@template('wall.html')
def wall():
    meta = Meta()
    walls = Wall.objects()
    wall_form = WallForm(request.form)
    return dict(meta=meta, walls=walls, wall_form=wall_form)

# Wall Form
@frontend.route('/wall/add', methods=['GET', 'POST'])
@template('wall_form.html')
def add_wall():
    meta = Meta()
    wall_form = WallForm(request.form)
    if wall_form.validate_on_submit():
        wall = Wall(username=wall_form.username.data,\
                content = wall_form.content.data)
        wall.html_content = markdown(wall.content, extensions)
        wall.created = datetime.datetime.now()
        try:
            wall.save()
            return redirect(url_for('wall'))
        except:
            return abort(500)
    return dict(meta=meta, wall_form=wall_form)


# Meta-flatpage
# Includes credits for hosting.
## TODO
"""
@frontend.route('/cleft')
@template('cleft.html')
def cleft():
    meta = Meta()
    flatpage = FlatPage.objects(title=Dep
    dependencies = Dependency.objects()
    copyrightinfo = markdown(meta.copyrightinfo)
    return dict(meta=meta, flatpage=flatpage, dependencies=dependencies,\
            copyrightinfo=copyrightinfo)
"""

# GETTERS
@frontend.route('/profile/<username>')
@frontend.route('/profile/id/<id>')
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

# Image deleter
@frontend.route('/image/<slugid>/delete')
@login_required
def delete_image(slugid):
    try:
        image = Image.objects(slugid=slugid).get()
    except:
        return abort(404)
    try:
        slugid = image.slugid
        title = image.title
        image.delete()
        flash("The image '%s' with slugid '%s' was deleted." % (title, slugid))
    except:
        flash("Could not delete image")
    return redirect(url_for('admin'))

# Image Getter
@frontend.route('/image/<title>')
def imagepage(title):
    image = Image.objects(title=title).first()
    if image is not None:
        return "Filename: %s, title: %s, id: %s" % (image.filename, photo.title,\
            image.id)
    else:
        return abort(404)

@template('text_post.html')
def single_text_post(year, month, day, slugid, slug=None):
    meta = Meta()
    text_post = TextPost.objects(slugid=slugid).get()
    return dict(meta=meta, text_post=text_post)

@frontend.route('/image/<slugid>/url')
def slugid_to_url(slugid):
    """
    Get the slugid from a GET request and return the url
    """
    meta = Meta()
    try:
        image = Image.objects(slugid=slugid).get()
    except:
        return abort(404)
    return jsonify(slugid=image.slugid, title=image.title, url=image.medium,\
            filename=image.filename)

@frontend.route('/media/<slugid>')
@frontend.route('/media/<slugid>/<slug>')
def image_by_slugid(slugid, slug=None):
    """Get the image by the slugid"""
    meta = Meta()
    try:
        image = Image.objects(slugid=slugid).get()
    except:
        return abort(404)
    if slug == None:
        return redirect(url_for('image_by_slugid', slugid=slugid,\
            slug=image.slug))
    return render_template('image_page.html', meta=meta, image=image)

# Most reliable post retrieval url
@frontend.route('/post/<slugid>')
@frontend.route('/post/<slugid>/')
@frontend.route('/post/<slugid>/<slug>')
@frontend.route('/post/<int:year>/<int:month>/<int:day>/<slugid>/')
@frontend.route('/post/<int:year>/<int:month>/<int:day>/<slugid>')
@frontend.route('/post/<int:year>/<int:month>/<int:day>/<slugid>/<slug>')
def post_by_slugid(slugid, slug=None, year=None, month=None, day=None):
    meta = Meta()
    try:
        post = Post.objects(slugid=slugid).get()
    except:
        return abort(404)
    if (slug == None or year == None or month == None or day == None):
        return redirect(url_for('post_by_slugid', slugid=slugid,\
            slug=post.slug, year=post.created.year,\
            month=post.created.month, day=post.created.day))
    post['created'] =\
        datetime.datetime.strftime(post.created, "%y-%m-%d @ %H:%m")
    updated = []
    if post.updated:
        for date in post.updated:
            updated.append(datetime.datetime.strftime(date, "%y-%m-%d @ %H:%m"))
        post['updated'] = updated
    showedit = True
    return render_template("text_post.html", meta=meta, text_post=post,\
            showedit=showedit)

## TK returns possible collisions in slug name
@frontend.route('/post/<slug>')
def post_by_slug(slug):
    meta = Meta()
    text_post = TextPost.objects(slug=slug).first()
    text_post['created'] =\
        datetime.datetime.strftime(text_post.created,\
                                "%Y-%m-%d @ %H:%M")
    return render_template('text_post.html', meta=meta, text_post=text_post)

