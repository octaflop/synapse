import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
def after_install(options, home_dir):
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'yolk'])
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'flask'])
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'flask-wtf'])
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'unidecode'])
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'pymongo'])
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'mongoengine'])
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'gunicorn'])
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'markdown'])
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                    '-U', 'flask-openid'])
"""))

file = open('bootstrap.sh', 'w')
file.write(output)
file.close()

import subprocess
subprocess.call(['chmod', '+x', 'bootstrap.sh'])
subprocess.call(['./bootstrap.sh', '../'])
