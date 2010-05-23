#! /usr/bin/env python
# -*- coding: utf8 -*-
# -*- coding: utf-8 -*-
# Copyright © 2010 Faris Chebib
#
# This file is part of aliendog.
#
# aliendog is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# aliendog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with aliendog; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

from models import R
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	if R.exists('testincr'):
		incr = R.zincr('testincr', 1)
		return u"Success with increment! We are now at %i" % incr
	else:
		incr = R.zincr('testincr', 1)
		return u"Started increment. We are now at %i" % incr

if __name__ == "__main__":
	app.debug = True
	app.run()

