import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'easy_install'), '-U', 'pip'])
    apps = ['flask', 'werkzeug', 'jinja2', 'wtforms', 'flask-wtf', 'unidecode', 'pymongo', 'mongoengine', 'gunicorn', 'markdown', 'flask-openid']
    for app in apps:
        subprocess.call([join(home_dir, 'bin', 'pip'), 'install', '-U', app])
    subprocess.call([join('/usr/bin/', 'wget'),\
                    "http://sysoev.ru/nginx/nginx-0.8.52.tar.gz"])
    subprocess.call(['/bin/tar', 'zxvf', 'nginx-0.8.52.tar.gz'])
    import os
    os.chdir('nginx-0.8.52')
    try:
        subprocess.call(['./configure', '--prefix=%s/usr' % (home_dir),\
                        '--conf-path=%s/usr/conf/gunicorn.conf' % (home_dir)])
        subprocess.call(['make'])
        subprocess.call(['make', 'install'])
    except:
        print "some sort of error occurred when installing nginx"

    try:
        os.chdir(join(home_dir, '/synapse'))
"""))

file = open('bootstrap.sh', 'w')
file.write(output)
file.close()

import subprocess
subprocess.call(['chmod', '+x', 'bootstrap.sh'])
subprocess.call(['./bootstrap.sh', '../synapse/'])
