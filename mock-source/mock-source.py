#!/usr/bin/env python

from datetime import datetime
import json
import urllib2
import time
import os, sys
from flask import (Flask, request)

"""
Setup:

(1) Deploy the SCDF stream
(2) Use `cf apps` to get the URI of the HTTP Source app
(3) Create a service named "http-hub" using this URI value:
    cf cups http-hub -p '{"uri": "THIS_URI_VALUE"}'
(4) `cf push --no-start` (this app)
(5) Bind to http-hub: `cf bs `

"""

# This is the name of the user-provided service in (3)
SERVICE_NAME = 'http-hub'

# Fetch the URI of the HTTP Source from VCAP_SERVICES
uri = None
USER_PROVIDED = 'user-provided'
SOURCE_NAME = 'mock'
vcap = json.loads(os.getenv('VCAP_SERVICES', '{}'))
if USER_PROVIDED in vcap:
  for cred in vcap[USER_PROVIDED]:
    if cred['name'] == SERVICE_NAME:
      uri = cred['credentials']['uri']
if uri is None:
  err_str = 'This app must be bound to a user-provided service named "%s"' % SERVICE_NAME
  raise BaseException(err_str)
print 'URI: %s' % uri

app = Flask(__name__)
port = int(os.getenv("PORT", 18080))

def logMsg(args):
    print "[Instance: %s] %s" % (str(os.getenv("CF_INSTANCE_INDEX", 0)), args)

def sendJson(msg):
  req = urllib2.Request(uri)
  req.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(req, json.dumps(msg))
  return "OK"

@app.route('/datetime')
def sendDate():
  d1 = datetime.now()
  data = { 'date_time': d1.strftime('%m/%d/%y %I:%M:%S'), 'source': SOURCE_NAME }
  return sendJson(data)

@app.route('/status')
def test():
  return "STATUS_OK"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port, threaded=True, debug=False)

