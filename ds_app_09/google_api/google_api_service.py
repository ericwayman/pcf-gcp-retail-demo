import os

from flask import Flask, request, jsonify 
import helper_functions
from helper_functions import DEFAULT_LIMIT

app = Flask(__name__)

@app.route("/")
def main():
    return "Hello World!"

@app.route('/api', methods=['POST','OPTIONS'])
#@helper_functions.crossdomain(origin='*')
def handle_google_api_request():
    req = request.get_json(force=True)
    return jsonify(req)

@app.route('/nlp', methods=['POST','OPTIONS'])
#@helper_functions.crossdomain(origin='*')
def handle_nlp_request():
    req = request.get_json(force=True)
    results = helper_functions.get_text_entities(req['content'])
    return jsonify({
        'entites': results
    })

@app.route('/vision/ocr', methods=['POST','OPTIONS'])
#@helper_functions.crossdomain(origin='*')
def handle_vision_text_request():
    text_list = helper_functions.get_image_text(request.data)

    print text_list

    return jsonify(text_list)

@app.route('/vision/logos', methods=['POST','OPTIONS'])
#@helper_functions.crossdomain(origin='*')
def handle_vision_logo_request():
    logo_list = helper_functions.get_image_logos(request.data)

    return jsonify(logo_list)

@app.route('/storage/<bucket>/<blob>', methods=['GET', 'POST', 'OPTIONS'])
#@helper_functions.crossdomain(origin='*')
def handle_storage_request(bucket, blob):
    if request.method == 'POST':
        new_blob = helper_functions.create_blob(request.data, blob, bucket, 
                                                request.headers['content-type'], 
                                                create_bucket=True)
        return jsonify({
            'created': '{0} in bucket {1}'.format(blob, bucket)
        })
    elif request.method == 'GET':
        requested_blob = helper_functions.get_blob(bucket, blob)
        return jsonify(requested_blob)
    else:
        return jsonify({
            'reponse' : "{0} method not supported".format(request.method)
        })

if __name__ == "__main__":
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        PORT = 5000
        DEBUG = True
        app.run(debug=DEBUG)
    else:                                       # running on CF
        PORT = int(os.getenv("PORT"))
        DEBUG = False
        app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

