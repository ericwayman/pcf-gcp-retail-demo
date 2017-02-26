#!/usr/bin/env python

import os
import json
from flask import (Flask, request, jsonify)

app = Flask(__name__)
port = int(os.getenv("PORT", 18080))

def logMsg(args):
    print "[Instance: %s] %s" % (str(os.getenv("CF_INSTANCE_INDEX", 0)), args)

# Handle JSON
# Simulate adding a "sentiment" attribute
@app.route('/', methods = ['POST', 'GET'])
def jsonHandler():
  obj = request.get_json(force=True)
  obj['sentiment'] = { 'score': 0.4, 'magnitude': 0.9 }
  logMsg(json.dumps(obj))
  return json.dumps(obj)

@app.route('/status')
def test():
    return "STATUS_OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)

