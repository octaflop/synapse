import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'pip'])
    apps = ['flask', 'flask-wtf', 'unidecode', 'pymongo', 'mongoengine', 'gunicorn', 'markdown', 'flask-openid']
    for app in apps:
        subprocess.call([join(home_dir, 'bin', 'pip'),
                        'install', '-U', app])
"""))

file = open('bootstrap.sh', 'w')
file.write(output)
file.close()

import subprocess
subprocess.call(['chmod', '+x', 'bootstrap.sh'])
subprocess.call(['./bootstrap.sh', '../'])
