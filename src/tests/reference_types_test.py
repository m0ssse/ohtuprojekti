import unittest
from reference_types import get_supported_fields
from db_helper import reset_db



class TestReferenceTypes(unittest.TestCase):
    def test_get_supported_fields_article(self):
            fields = get_supported_fields("article")

            self.assertIn("author", fields)
            self.assertIn("title", fields)
            self.assertIn("journal", fields)
            self.assertIn("year", fields)

            self.assertNotIn("publisher", fields)
            self.assertNotIn("booktitle", fields)

    def test_get_supported_fields_book(self):
            fields = get_supported_fields("book")
            self.assertIn("author", fields)
            self.assertIn("title", fields)
            self.assertIn("year", fields)
            self.assertIn("publisher", fields)
            self.assertNotIn("journal", fields)
            self.assertNotIn("booktitle", fields)

    def test_get_supported_fields_inproceedings(self):
            fields = get_supported_fields("inproceedings")
            self.assertIn("author", fields)
            self.assertIn("title", fields)
            self.assertIn("year", fields)
            self.assertIn("booktitle", fields)
            self.assertNotIn("journal", fields)
            self.assertNotIn("publisher", fields)

    def test_get_supported_fields_unknown_type_uses_default(self):
            fields = get_supported_fields("unknown_type")

            self.assertIn("author", fields)
            self.assertIn("title", fields)
            self.assertIn("year", fields)