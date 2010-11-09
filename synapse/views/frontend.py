#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# bootstrap module
from flask import Module

frontend = Module(__name__)

# external deps
from flask import url_for, flash, escape, request, redirect,\
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
from synapse.settings import *
from synapse.forms import *
from synapse.strings import *
from synapse.decorators import template, login_required
from synapse.models import Site, User, Post, TextPost, Media, FlatPage,\
        Dependency, Image, Wall
from PIL import Image as Picture

# App Info
__VERSION__ = '0.2'
__AUTHOR__ = 'Faris Chebib'

# markdown extensions
#extensions = ['footnotes', 'fenced_code']
extensions = ['footnotes', 'codehilite']

# META
class Meta:
    """
    The meta class is called for all base-page requests.
    This includes the theme mangement options
    """
    def __init__(self):
        self.logged_in = False
        self.loginform = LoginForm(request.form)
        if 'username' in session:
            self.username = escape(session['username'])
            self.user = User.objects(username=self.username).first()
            if not self.user == None:
                self.logged_in = True
        else:
            self.user = None
        self.site = Site.objects.first()
        ## this should probably be somewhere else (in the model?)
        self.footy = {}
        copyrightinfo_html = \
u"""
<a rel="license"
href="http://creativecommons.org/licenses/by-sa/2.5/ca/"><img
alt="Creative Commons License" style="border-width:0"
src="http://i.creativecommons.org/l/by-sa/2.5/ca/88x31.png" /></a><br
/>Content is released under a
<a href='http://creativecommons.org/licenses/by-sa/2.5/ca/'>Creative Commons
Attribution-ShareAlike 2.5 Canada License</a>
"""
        self.footy['copyrightinfo'] = copyrightinfo_html
        # May want to set up a model from the flatpages.
        self.footy['links'] = [{\
                'title' : u"github page",
                'url' : u"http://github.org/octaflop/synapse"
                }]

def make_external(url):
    return urljoin(request.url_root, url)

# Atom feed
@frontend.route('/feed.atom')
def atom_feed():
    meta = Meta()
    feed = AtomFeed(u'%s feed' % meta.site,
            feed_url=request.url, url=request.url_root)
    posts = Post.objects()
    for post in posts:
        feed.add(post.title, unicode(post.html_content),
                content_type='html',
                author=post.author.username,
                url=make_external(url_for('post_by_slugid',\
                    slugid=post.slugid)),
                updated=post.updated[0],
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

# User Functions
@frontend.route('/admin/add/user', methods=['GET', 'POST'])
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

@frontend.route('/logout')
def logout():
    if 'username' in session:
        user = escape(session['username'])
        session.pop('username', None)
    else:
        return "Not logged in"
    flash("logged out: %s" % user)
    return redirect(url_for('index'))

@frontend.route('/login/<next>', methods=['GET','POST'])
@frontend.route('/login', methods=['GET','POST'])
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

@template('text_post.html')
def single_text_post(year, month, day, slugid, slug=None):
    meta = Meta()
    text_post = TextPost.objects(slugid=slugid).get()
    return dict(meta=meta, text_post=text_post)

@frontend.route('/admin/manage')
@login_required
@template('admin/manage.html')
def manage():
    flats = FlatPage.objects()
    posts = Post.objects()
    images = Image.objects()
    return dict(posts=posts, images=images, flats=flats)

@frontend.route('/admin')
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

@frontend.route('/admin/edit/<slugid>/_title', methods=['POST', 'PUT', 'GET'])
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

@frontend.route('/admin/edit/<slugid>/_content', methods=['POST', 'PUT', 'GET'])
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

@frontend.route('/post/<slugid>/edit')
@frontend.route('/post/<slugid>/<slug>/edit')
@frontend.route('/post/<int:year>/<int:month>/<int:day>/<slugid>/<slug>/edit')
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

@frontend.route('/<slugid>/delete')
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
@frontend.route('/admin/add/site', methods=['POST'])
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


@frontend.route('/admin/add/text', methods=['POST', 'GET'])
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

@frontend.route('/admin/add/image', methods=['POST', 'GET'])
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

# HELPER FUNCTIONS
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
        deps = Dependency.objects()
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
""" % (meta.domain)
    html_content = markdown(content, extensions)
    title = u"Hello, World!"
    post = Post(title=title,content=content, html_content=html_content, author=user)
    post.slugid = slugidfy()
    post.slug = slugfy(title)
    post.published = datetime.datetime.now()
    post.created = datetime.datetime.now()
    post.is_published = True
    post.save()

