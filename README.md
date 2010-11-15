# Synapse

![synapse logo](./raw/master/synapse.png)

## Description 
Synapse is a simple blogging application written in
[Flask](http://flask.pocoo.com/) and supported by
[MongoDB](http://www.mongodb.org/). As a bonus, it "bootstraps" itself to build
a [gunicorn](http://gunicorn.org/) server backend for speedy production!

## Caveats

***Synapse* is currently in its pre-alpha stages and is *not meant for public
use***. Be sure to report any bugs, and feel free to write your own patches.

As this is the first software I've ever distributed freely (and I'm not a
programmer by profession --- a painfully clear point when sees the 'ol git logs), there may be a few issues with the code. I have tried
to automate most of the install process (which is documented below) and wrote
some very basic tests (which sometimes don't pass). I could really use some help
in writing tests and documentation.

# Getting Started

## Requirements:
* mongodb
* virtualenv

## Steps
0. Start mongodb

1. Run 
        python bootstrap.py
   **You will likely need to hand-pick missing dependencies as this script does
   not always work.**

2. Then run
        source bin/activate

3. Get database settings in order:
        cp synapse/passwd-example.py synapse/passwd.py
        vim passwd.py

4. For development, run:
        python run.py dev 
    or, for production, run:
        python run.py prod
    be sure to edit usr/conf/gunicorn.conf and change the static routing to your absolute directory location.

## When things go wrong.
Something will likely go wrong when using the bootstrap. It´s a good idea to
have a look at the script and download things by hand. Usually this will simply
involve
    bin/pip install -U <app>

If you have other issues, I´ll have a look-see at the github page.
