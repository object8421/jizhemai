# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bottle import Bottle, request, route, run,template
import sae
import sae.kvdb
sae.add_vendor_dir('vendor')
from qiniu import Auth
from qiniu import BucketManager


app = Bottle()

@app.route('/')
def aaa():
	return ('111')

application = sae.create_wsgi_app(app)
