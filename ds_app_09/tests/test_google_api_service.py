#from parent directory pcf-gcp-ml-apis run:
#python -m unittest pcf-gcp-ml-apis.tests.test_google_api_service
from __future__ import print_function
import unittest
import google_api.google_api_service as google_app
import json
vision_labels_request_fname = 'vision_request.json'


class Test(unittest.TestCase):

    def setUp(self):
        self.app = google_app.app.test_client()
        self.app.testing = True

    def test_main_page(self):
        """Test that the status code 200 is returned for get."""
        results = self.app.get("/")
        self.assertEqual(results.status_code,200)

    def test_nlp_status(self):
        """Test that the status code 200 is returned for post."""
        results = self.app.post('/nlp',data=json.dumps({"content":"test data content."}))
        self.assertEqual(results.status_code,200)

    #curl --data '{"content": "New Yorkers will choose one of five finalists for residents in all five boroughs to read as part of a city program."}' http://google-api-service.apps.pcfongcp.com/nlp"""
    # returns{"first_entity_string": "PERSON: New Yorkers"}
    def test_nlp_entity_string_results(self):
        """Test that the nlp app returns the correct entity string"""
        content="New Yorkers will choose one of five finalists for residents in all five boroughs to read as part of a city program."
        results = self.app.post('/nlp',data=json.dumps({"content":content}))

        results_dict = json.loads(results.get_data(as_text=True))
        # prediction = {"first_entity_string": "PERSON: New Yorkers"}
        self.assertEqual(results_dict['first_entity_string'], "PERSON: New Yorkers")


class TestVisionEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = google_app.app.test_client()
        with open(vision_labels_request_fname, 'rb') as f:
            self.vision_request = f.read()

    def test_vision_status(self):
        results = self.app.post('/vision', data=self.vision_request)
        self.assertEqual(results.status_code, 200)

    def test_vision_labels_request(self):
        results = self.app.post('/vision', data=self.vision_request)
        result_dict = json.loads(results.get_data())
        print(result_dict)
        result_list = result_dict['responses']
        self.assertIsInstance(
            result_list, list,
            "Expected result as list, got '{}'".format(type(result_list))
        )
        self.assertGreater(
            len(result_list), 0,
            "Expected results but got none"
        )
