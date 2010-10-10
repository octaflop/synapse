def prod():
    import subprocess
    import os
    from multiprocessing import Process

    Process(target=subprocess.call, args=(
        (os.path.join('bin', 'gunicorn'), '-b',\
        'localhost:8000', 'synapse:app'),
        )).start()

    Process(target=subprocess.call, args=(
        (os.path.join('usr', 'sbin', 'nginx'), '-c',\
        os.path.join('conf', 'gunicorn.conf')),
        )).start()

if __name__ == "__main__":
    from synapse import app
    app.run(debug=True)
    #print prod()
