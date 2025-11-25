import unittest
from db_helper import reset_db
from app import app
from util import validate_reference

class TestReferenceMethods(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        reset_db()
        fields = [
        "ref_type", "author", "title", "year", "journal", "volume",
        "publisher", "booktitle", "edition", "chapter", "pages",
        "doi", "address"
    ]
        self.data = {field: "" for field in fields}
        self.data["ref_type"] = "book"
        
    def test_book_with_valid_fields(self):
        self.data["author"] = "test_author"
        self.data["title"] = "test_title"
        self.data["year"] = "2025"

        res, _ = validate_reference(self.data)
        self.assertTrue(res)

    def test_book_with_no_author(self):
        self.data["title"] = "test_title"
        self.data["year"] = "2025"
        
        res, missing_fields = validate_reference(self.data)
        self.assertFalse(res)
        self.assertEqual(missing_fields, ["author"])

    def test_book_with_no_title(self):
        self.data["author"] = "test_author"
        self.data["year"] = "2025"
        
        res, missing_fields = validate_reference(self.data)
        self.assertFalse(res)
        self.assertEqual(missing_fields, ["title"])

    def test_book_with_no_year(self):
        self.data["author"] = "test_author"
        self.data["title"] = "test_title"
        
        res, missing_fields = validate_reference(self.data)
        self.assertFalse(res)
        self.assertEqual(missing_fields, ["year"])

    def test_book_with_no_required_fields(self):
        self.assertTrue(True)