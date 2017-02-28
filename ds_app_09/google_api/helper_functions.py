# -*- coding: utf-8 -*-
import os
import json
from datetime import timedelta
from functools import update_wrapper
from operator import itemgetter
import base64
from io import StringIO

import httplib2
from flask import make_response, request, current_app, jsonify
from googleapiclient import discovery, errors, http 

"""
from google.cloud import language
#from google.cloud import vision
from google.cloud import storage
from google.cloud.vision.image import Image
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob
from google.cloud.exceptions import NotFound
"""; 

from google.oauth2.service_account import Credentials


DEFAULT_LIMIT = 10
SERVICE_NAME = 'google-ml-apis'
SERVICE_INSTANCE_NAME = 'google-ml'
CREDENTIALS = None
clients = {
    'language': None,
    'vision': None,
    'storage': None
}
vision_features = [
    {
        "type":"LABEL_DETECTION",
        "maxResults": 10
    },
    {
        "type":"TEXT_DETECTION",
        "maxResults": 10
    },
    {
        "type":"FACE_DETECTION",
        "maxResults": 20
    }
]
 
entity_annotation_fields = (
'bounds',
'description',
'locale',
'locations',
'mid',
'score'
)


def get_service_instance_dict():
    """Look in VCAP_SERVICES environment variable and get the dict describing
    a specific service and instance of that service.
    """
    vc_svcs_str = os.environ.get('VCAP_SERVICES')
    if vc_svcs_str is None:
        raise Exception('VCAP_SERVICES not found in environment variables (necessary for credentials)')
    vc_svcs_dict = json.loads(vc_svcs_str)
    svcs = filter(
        lambda s: s.get('name') == SERVICE_INSTANCE_NAME
        , vc_svcs_dict[SERVICE_NAME]
    )
    if not svcs:
        raise Exception(
            "No services matching {targ}. Options: {avail}".format(
                targ=SERVICE_INSTANCE_NAME,
                avail=tuple(map(itemgetter('name'), vc_svcs_dict[SERVICE_NAME]))
            )
        )
    return svcs[0]


def get_google_cloud_credentials():
    """Returns oauth2 credentials of type
    google.oauth2.service_account.Credentials
    """
    global CREDENTIALS
    if CREDENTIALS is None:
        service_info = get_service_instance_dict()
        pkey_data = base64.decodestring(service_info['credentials']['PrivateKeyData'])
        pkey_dict = json.loads(pkey_data)
        CREDENTIALS = Credentials.from_service_account_info(pkey_dict)
    return CREDENTIALS

def get_google_client(name, version='v1'):
    global clients
    if clients.get(name) is None:
        credentials = get_google_cloud_credentials()

        clients[name] = discovery.build(name, version, credentials=credentials)

    return clients[name]


def get_text_entities(text, content_type="PLAIN_TEXT", encoding='UTF8'):
    # content_types can be:
    # PLAIN_TEXT, HTML
    #

    # encodings can be: 
    # NONE, UTF8, UTF16, UTF32
    #

    client = get_google_client("language")

    body = { "encodingType": encoding, 
        "document" : {
            "content" : text,
            "type" : content_type
        },
        "features" : {
            "extractDocumentSentiment" : True,
            "extractEntities" : True,
            "extractSyntax" : True   
        }
    }

    resp = client.documents().annotateText(body=body).execute()
    return resp


"""
def entity_to_str(entity):
    return "{}: {}".format(entity.entity_type, entity.name)


def first_entity_str(text):
    entities = get_text_entities(text)
    if entities:
        entity = entities[0]
        return entity_to_str(entity)
    else:
        return ''
""";

def read_image_base64(image):
    if isinstance(image, basestring) and image.lower().startswith('http'):
        response = urllib.request.urlopen(url)
        data = response.read()
        return base64.b64encode(data.decode('utf-8'))

    else:
        return base64.b64encode(image)        

## Vision: Funcs to get labels

def get_image_feature(image_url_or_bytes, feature_list, limit=DEFAULT_LIMIT):
    """
    :param image_url: str URL
    :param limit: int Max number of results to return
    :return: list of annotation dictionaries
    """

    request = { "requests": [{
        "image": {
            "content": read_image_base64(image_url_or_bytes)
        },
        "features" : ""
      }]
    }

    request['requests'][0]['features'] = [{ 'type': f, "maxResults": limit } for f in feature_list]

    print request
    
    reponse_dict = get_google_client("vision").images().annotate(body=request).execute()

    annotation_list = []
    if 'responses' in reponse_dict:
        annotation_list = reponse_dict['responses']
    
    return annotation_list

def get_image_labels(image, l=DEFAULT_LIMIT):
    return get_image_feature(image, ["LABEL_DETECTION"], limit=l)

def get_image_text(image, l=DEFAULT_LIMIT):
    return get_image_feature(image, ["TEXT_DETECTION"], limit=l)

def get_image_logos(image, l=DEFAULT_LIMIT):
    return get_image_feature(image, ["LOGO_DETECTION"], limit=l)

def get_image_faces(image, l=DEFAULT_LIMIT):
    return get_image_feature(image, ["FACE_DETECTION"], limit=l)

## Storage

def get_storage_bucket(bucket_name, create_new=True):
    _request = get_google_client("storage").buckets().get(bucket=bucket_name)
    try:
        resp = _request.execute()
        return resp
    except errors.HttpError, e:
        if create_new:
            request = get_google_client("storage").buckets().insert(bucket=bucket_name)
            resp = request.execute()
            return resp

def get_blob(bucket_name, blob_name):
    req = get_google_client("storage").objects().get_media(bucket=bucket_name, object=blob_name)
    return req.execute()

def create_blob(payload, blob_name, bucket_name, content_type="text/plain", 
                create_bucket=True):

    # This is the request body as specified:
    # http://g.co/cloud/storage/docs/json_api/v1/objects/insert#request
    body = {
        'name': blob_name,
    }

    p = StringIO(unicode(payload, "utf-8"))
    req = get_google_client("storage").objects().insert(
        bucket=bucket_name, body=body,
        # You can also just set media_body=filename, but for the sake of
        # demonstration, pass in the more generic file handle, which could
        # very well be a StringIO or similar.
        media_body=http.MediaIoBaseUpload(p, 'application/octet-stream'))
    resp = req.execute()

    return resp
 
"""
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
""";
