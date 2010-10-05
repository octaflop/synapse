# Synapse

## Requirements:
* virtualenv

# Getting Started
1. Run  
        ./bootstrap.sh

2. Then run
       source bin/activate

3. Get database settings in order:
       cp passwd-example.py passwd.py
       vim passwd.py

4. For development, 
        run python run.py  
    or, for production, run  
        bin/gunicord synapse:app


#!/usr/bin/python
# this
print "this should work"
