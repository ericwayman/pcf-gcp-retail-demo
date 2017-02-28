# pcf-gcp-ml-apis
Access to Google Cloud APIs provided from endpoints in Pivotal Cloud Foundry.

## Python dependencies:

- googleapiclient

`pip install --upgrade googleapiclient`

## Cloud Foundry setup

    cf push --no-start
    cf create-service google-ml-apis default google-ml
    cf bind-service google-api-service google-ml -c '{"role": "viewer"}'
    cf start APP_NAME

## Google API credential setup

 1. Create a new service account in GCP
 2. Authorize the above service account for editor access to the desired GCP storage container
 3. Add OAuth JSON to `VCAP_SERVICES` in a field within `credentials` called `PrivateKeyData` using the output from the following command:

```
    cat <FILENAME FROM GCP>.json | base64
```

For local testing, create a file call `vcap_local.json` formatted like this:

```
{
  "google-ml-apis" :[{
    "name": "google-ml",
    "credentials": {
     "Email": "<YOUR SERVICE ACCOUNT EMAIL>",
     "Name": "pcf-binding-kdunn",
     "PrivateKeyData": "<OUTPUT FROM COMMAND ABOVE>",
     "ProjectId": "<YOUR PROJECT NAME>",
     "UniqueId": "<YOUR PROJECT ID>",
     "bucket_name": "<YOUR STORAGE BUCKET URL>"
    }
  }]
}
```

where `google-ml-apis` and `google-ml` match the global variables in `helper_functions.py` (SERVICE_NAME and SERVICE_INSTANCE_NAME respectively)

then store this data in an environment variable:

    export VCAP_SERVICES=`cat vcap_local.json`

## Test NLP with curl:

`curl --data '{"content": "New Yorkers will choose one of five finalists for residents in all five boroughs to read as part of a city program."}' http://127.0.0.1:5000/nlp`
```
    {
      "entites": {
        "documentSentiment": {
          "magnitude": 0.3,
          "score": 0.3
        },
        "entities": [
          {
            "mentions": [
              {
                "text": {
                  "beginOffset": 0,
                  "content": "New Yorkers"
                },
                "type": "PROPER"
              }
            ],
            "metadata": {
              "mid": "/m/02_286",
              "wikipedia_url": "http://en.wikipedia.org/wiki/New_York_City"
            },
            "name": "New Yorkers",
            "salience": 0.28529522,
            "type": "PERSON"
          },
          {
            "mentions": [
              {
                "text": {
                  "beginOffset": 24,
                  "content": "one"
                },
                "type": "COMMON"
              }
            ],
            "metadata": {},
            "name": "one",
            "salience": 0.1990818,
            "type": "OTHER"
          },
          {
            "mentions": [
              {
                "text": {
                  "beginOffset": 50,
                  "content": "residents"
                },
                "type": "COMMON"
              }
            ],
            "metadata": {},
            "name": "residents",
            "salience": 0.14333345,
            "type": "PERSON"
          },
          {
            "mentions": [
              {
                "text": {
                  "beginOffset": 36,
                  "content": "finalists"
                },
                "type": "COMMON"
              }
            ],
            "metadata": {},
            "name": "finalists",
            "salience": 0.13830818,
            "type": "PERSON"
          },
          {
            "mentions": [
              {
                "text": {
                  "beginOffset": 72,
                  "content": "boroughs"
                },
                "type": "COMMON"
              }
            ],
            "metadata": {},
            "name": "boroughs",
            "salience": 0.118380435,
            "type": "OTHER"
          },
          {
            "mentions": [
              {
                "text": {
                  "beginOffset": 102,
                  "content": "city program"
                },
                "type": "COMMON"
              }
            ],
            "metadata": {},
            "name": "city program",
            "salience": 0.065964274,
            "type": "OTHER"
          },
          {
            "mentions": [
              {
                "text": {
                  "beginOffset": 92,
                  "content": "part"
                },
                "type": "COMMON"
              }
            ],
            "metadata": {},
            "name": "part",
            "salience": 0.049636636,
            "type": "OTHER"
          }
        ],
        "language": "en",
        "sentences": [
          {
            "sentiment": {
              "magnitude": 0.3,
              "score": 0.3
            },
            "text": {
              "beginOffset": 0,
              "content": "New Yorkers will choose one of five finalists for residents in all five boroughs to read as part of a city program."
            }
          }
        ],
        "tokens": [
          {
            "dependencyEdge": {
              "headTokenIndex": 1,
              "label": "NN"
            },
            "lemma": "New",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "SINGULAR",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NOUN",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 0,
              "content": "New"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 3,
              "label": "NSUBJ"
            },
            "lemma": "Yorkers",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "SINGULAR",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NOUN",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 4,
              "content": "Yorkers"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 3,
              "label": "AUX"
            },
            "lemma": "will",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "VERB",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 12,
              "content": "will"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 3,
              "label": "ROOT"
            },
            "lemma": "choose",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "VERB",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 17,
              "content": "choose"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 3,
              "label": "DOBJ"
            },
            "lemma": "one",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NUM",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 24,
              "content": "one"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 4,
              "label": "PREP"
            },
            "lemma": "of",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "ADP",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 28,
              "content": "of"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 7,
              "label": "NUM"
            },
            "lemma": "five",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NUM",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 31,
              "content": "five"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 5,
              "label": "POBJ"
            },
            "lemma": "finalist",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "PLURAL",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NOUN",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 36,
              "content": "finalists"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 7,
              "label": "PREP"
            },
            "lemma": "for",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "ADP",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 46,
              "content": "for"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 8,
              "label": "POBJ"
            },
            "lemma": "resident",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "PLURAL",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NOUN",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 50,
              "content": "residents"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 9,
              "label": "PREP"
            },
            "lemma": "in",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "ADP",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 60,
              "content": "in"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 13,
              "label": "DET"
            },
            "lemma": "all",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "DET",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 63,
              "content": "all"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 13,
              "label": "NUM"
            },
            "lemma": "five",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NUM",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 67,
              "content": "five"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 10,
              "label": "POBJ"
            },
            "lemma": "borough",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "PLURAL",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NOUN",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 72,
              "content": "boroughs"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 15,
              "label": "AUX"
            },
            "lemma": "to",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "PRT",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 81,
              "content": "to"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 7,
              "label": "VMOD"
            },
            "lemma": "read",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "VERB",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 84,
              "content": "read"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 15,
              "label": "PREP"
            },
            "lemma": "as",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "ADP",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 89,
              "content": "as"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 16,
              "label": "POBJ"
            },
            "lemma": "part",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "SINGULAR",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NOUN",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 92,
              "content": "part"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 17,
              "label": "PREP"
            },
            "lemma": "of",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "ADP",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 97,
              "content": "of"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 21,
              "label": "DET"
            },
            "lemma": "a",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "DET",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 100,
              "content": "a"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 21,
              "label": "NN"
            },
            "lemma": "city",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "SINGULAR",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NOUN",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 102,
              "content": "city"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 18,
              "label": "POBJ"
            },
            "lemma": "program",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "SINGULAR",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "NOUN",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 107,
              "content": "program"
            }
          },
          {
            "dependencyEdge": {
              "headTokenIndex": 3,
              "label": "P"
            },
            "lemma": ".",
            "partOfSpeech": {
              "aspect": "ASPECT_UNKNOWN",
              "case": "CASE_UNKNOWN",
              "form": "FORM_UNKNOWN",
              "gender": "GENDER_UNKNOWN",
              "mood": "MOOD_UNKNOWN",
              "number": "NUMBER_UNKNOWN",
              "person": "PERSON_UNKNOWN",
              "proper": "PROPER_UNKNOWN",
              "reciprocity": "RECIPROCITY_UNKNOWN",
              "tag": "PUNCT",
              "tense": "TENSE_UNKNOWN",
              "voice": "VOICE_UNKNOWN"
            },
            "text": {
              "beginOffset": 114,
              "content": "."
            }
          }
        ]
      }
    }
```

## Test Vision with curl

Note: watch out for this [bug](https://github.com/GoogleCloudPlatform/google-cloud-python/pull/2961) when using OCR.

Run from root directory of repo, because the command refers to the test JSON 
request included in the tests directory.

`curl -H "Content-Type:application/json" -X POST http://127.0.0.1:5000/vision/ocr --data-binary "@tests/coke.jpg"`
```
    [
      {
        "textAnnotations": [
          {
            "boundingPoly": {
              "vertices": [
                {
                  "x": 16,
                  "y": 121
                },
                {
                  "x": 383,
                  "y": 121
                },
                {
                  "x": 383,
                  "y": 235
                },
                {
                  "x": 16,
                  "y": 235
                }
              ]
            },
            "description": "CocaCola.\n\u00ae/MD\n",
            "locale": "gl"
          },
          {
            "boundingPoly": {
              "vertices": [
                {
                  "x": 17,
                  "y": 121
                },
                {
                  "x": 349,
                  "y": 123
                },
                {
                  "x": 348,
                  "y": 235
                },
                {
                  "x": 16,
                  "y": 233
                }
              ]
            },
            "description": "CocaCola"
          },
          {
            "boundingPoly": {
              "vertices": [
                {
                  "x": 351,
                  "y": 126
                },
                {
                  "x": 383,
                  "y": 126
                },
                {
                  "x": 382,
                  "y": 232
                },
                {
                  "x": 350,
                  "y": 232
                }
              ]
            },
            "description": "."
          },
          {
            "boundingPoly": {
              "vertices": [
                {
                  "x": 348,
                  "y": 219
                },
                {
                  "x": 357,
                  "y": 219
                },
                {
                  "x": 357,
                  "y": 229
                },
                {
                  "x": 348,
                  "y": 229
                }
              ]
            },
            "description": "\u00ae"
          },
          {
            "boundingPoly": {
              "vertices": [
                {
                  "x": 359,
                  "y": 219
                },
                {
                  "x": 363,
                  "y": 219
                },
                {
                  "x": 363,
                  "y": 227
                },
                {
                  "x": 359,
                  "y": 227
                }
              ]
            },
            "description": "/"
          },
          {
            "boundingPoly": {
              "vertices": [
                {
                  "x": 365,
                  "y": 220
                },
                {
                  "x": 378,
                  "y": 221
                },
                {
                  "x": 378,
                  "y": 229
                },
                {
                  "x": 365,
                  "y": 228
                }
              ]
            },
            "description": "MD"
          }
        ]
      }
    ]
```

`curl -H "Content-Type:application/json" -X POST http://127.0.0.1:5000/vision/logos --data-binary "@tests/coke.jpg"`
```
    [
      {
        "logoAnnotations": [
          {
            "boundingPoly": {
              "vertices": [
                {
                  "x": 53,
                  "y": 132
                },
                {
                  "x": 351,
                  "y": 132
                },
                {
                  "x": 351,
                  "y": 233
                },
                {
                  "x": 53,
                  "y": 233
                }
              ]
            },
            "description": "Coca-Cola",
            "mid": "/m/01yvs",
            "score": 0.7388113
          }
        ]
      }
    ]
```

## Test Storage with curl

`curl -H "Content-type: application/json" -d "test post" -X POST http://127.0.0.1:5000/storage/pde-kdunn.appspot.com/test`
```
    {
      "created": "test in bucket pde-kdunn.appspot.com"
    }
```

`curl -X GET http://127.0.0.1:5000/storage/pde-kdunn.appspot.com/test`
```
    "test post"
```
