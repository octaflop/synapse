import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'easy_install'), '-U', 'pip'])
    apps = ['flask', 'werkzeug', 'jinja2', 'wtforms', 'flask-wtf',\
    'unidecode', 'pymongo', 'mongoengine', 'gunicorn', 'markdown',\
    'Flask-Babel','Flask-Themes','flask-openid', 'git']
    for app in apps:
        subprocess.call([join(home_dir, 'bin', 'pip'), 'install', '-U', app])
    print "Now downloading jQuery & jQueryUI"
    import os
    os.mkdir("src")
    os.chdir("src")
    repos = ["https://github.com/jquery/jquery.git",\
        "https://github.com/jquery/jquery-ui.git"]
    for repo in repos
        subprocess.call([join('usr','bin','git'), 'clone', repo])
    import shutil
    dirs = [('jquery','dist'), ('jquery-ui','ui')]
    for srcdir,builddir in dirs:
        os.chdir(os.path.join(home_dir, "src", srcdir))
        subprocess.call([join('usr','bin','make')])
        shutil.copy(builddir, os.path.join(home_dir,"static","js"))
    os.chdir(home_dir)

    subprocess.call([join('/usr/bin/', 'wget'),\
                    "http://sysoev.ru/nginx/nginx-0.8.52.tar.gz"])
    subprocess.call(['/bin/tar', 'zxvf', 'nginx-0.8.52.tar.gz'])
    os.chdir('nginx-0.8.52')
    try:
        subprocess.call(['./configure', '--prefix=%s/usr' % (home_dir),\
                        '--conf-path=%s/usr/conf/gunicorn.conf' % (home_dir)])
        subprocess.call(['make'])
        subprocess.call(['make', 'install'])
    except:
        print "some sort of error occurred when installing nginx"
"""))

file = open('bootstrap.sh', 'w')
file.write(output)
file.close()

import subprocess
subprocess.call(['chmod', '+x', 'bootstrap.sh'])
subprocess.call(['./bootstrap.sh', '../synapse/'])
