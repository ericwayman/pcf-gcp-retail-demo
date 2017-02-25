#!/usr/bin/env python

import os
import json
from flask import (Flask, request, jsonify)

app = Flask(__name__)
port = int(os.getenv("PORT", 18080))

def logMsg(args):
    print "[Instance: %s] %s" % (str(os.getenv("CF_INSTANCE_INDEX", 0)), args)

# Handle JSON
# Simple No-Op which just logs the input and passes it back to the caller
@app.route('/', methods = ['POST', 'GET'])
def jsonHandler():
  obj = request.get_json(force=True)
  logMsg(json.dumps(obj))
  return json.dumps(obj)

@app.route('/status')
def test():
    return "STATUS_OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, threaded=True, debug=False)

