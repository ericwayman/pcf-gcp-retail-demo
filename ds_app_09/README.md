# Data Science Interrogator App

This is item 9 in our diagram

## Initial version
* Just accepts JSON as HTTP GET or POST (set MIME type to `application/json`)

## Test via Curl
`curl -H "Content-Type: application/json" -X POST -d '{"source":"mock","date_time":"02/25/17 10:15:27","days_until_message":"10 days until GCP NEXT"}' http://localhost:18080/`

