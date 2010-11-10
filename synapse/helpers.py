# -*- encoding:utf-8 -*-
# helpers.py
# database helper methods: init, reset, dev
from synapse.views.meta import Meta
from synapse.models import Site, Post, Dependency, User, Image, FlatPage

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

