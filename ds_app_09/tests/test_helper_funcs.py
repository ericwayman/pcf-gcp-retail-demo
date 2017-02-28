import unittest
import requests

from google.cloud.language.entity import Entity
from google.cloud.vision.entity import EntityAnnotation

from google_api import helper_functions

test_text = (
    ("New Yorkers will choose one of five finalists for residents in all "
     "five boroughs to read as part of a city program."),
)

image_urls = (
    "https://upload.wikimedia.org/wikipedia/commons/b/b1/High-speed_train_warning_sign_at_Kingston%2C_RI%2C_train_station.jpg",
    "https://i0.wp.com/evobsession.com/wp-content/uploads/2016/09/Chevy-Jolt.png",
)


class TestMlApiFuncs(unittest.TestCase):
    def test_entities_from_text(self):
        entities = helper_functions.get_text_entities(test_text[0])
        self.assertTrue(len(entities) > 0, "Got no entities from text")
        for entity in entities:
            self.assertIsInstance(
                entity, Entity,
                "Expected type <google.cloud.language.entity.Entity>, got: {}".format(
                    type(entity)
                )
            )

    def test_image_labels_from_url_has_annotations(self):
        labels = helper_functions.get_image_labels_from_url(image_urls[0])
        self.assertTrue(len(labels) > 0, "Got no labels from image")
        for label in labels:
            self.assertIsInstance(
                label, EntityAnnotation,
                "Expected type <google.cloud.vision.entity.EntityAnnotation>, got: {}".format(
                    type(label)
                )
            )

    def test_image_labels_from_bytes_has_annotations(self):
        response = requests.get(image_urls[0])
        labels = helper_functions.get_image_labels_from_bytes(response.content)
        self.assertTrue(len(labels) > 0, "Got no labels from image")
        for label in labels:
            self.assertIsInstance(
                label, EntityAnnotation,
                "Expected type <google.cloud.vision.entity.EntityAnnotation>, got: {}".format(
                    type(label)
                )
            )
