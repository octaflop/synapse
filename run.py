import atexit
import subprocess
import os
def prod():
    from multiprocessing import Process

    Process(target=subprocess.call, args=(
        (os.path.join('bin', 'gunicorn'), '-b',\
        'localhost:8000', 'synapse:app'),
        )).start()

    Process(target=subprocess.call, args=(
        (os.path.join('usr', 'sbin', 'nginx'), '-c',\
        os.path.join('conf', 'gunicorn.conf')),
        )).start()

def cleanup():
    subprocess.call(['killall', 'gunicorn'])
    subprocess.call(['killall', 'nginx'])


if __name__ == "__main__":
    import sys
    if 'prod' in sys.argv:
        atexit.register(cleanup)
        print prod()
    elif 'dev' in sys.argv:
        from synapse import app
        app.run(debug=True)
    else:
        from synapse import app
        app.run(debug=True)

