import unittest
from app import app
from db_helper import reset_db
from entities.reference import Reference
from repositories.reference_repository import create_reference


class TestReferenceViews(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        reset_db()
        self.client = app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_new_reference_contains_type_specific_field_groups(self):
        response = self.client.get("/new_reference")
        self.assertEqual(response.status_code, 200)

        html = response.data.decode("utf-8")

        self.assertIn('id="ref_type"', html)
        self.assertIn('value="book"', html)
        self.assertIn('value="article"', html)
        self.assertIn('value="inproceedings"', html)

        self.assertIn('data-type-only="article"', html)
        self.assertIn('name="journal"', html)

        self.assertIn('data-type-only="book"', html)
        self.assertIn('name="publisher"', html)

        self.assertIn('data-type-only="inproceedings"', html)
        self.assertIn('name="booktitle"', html)

        self.assertIn('name="author"', html)
        self.assertIn('name="title"', html)
        self.assertIn('name="year"', html)

    def test_show_reference_article_shows_article_fields_only(self):
        ref = Reference(
            id=1,
            ref_type="article",
            author="Author A",
            title="Title T",
            year=2010,
            journal="Journal J",
            volume="11",
            pages="23-56",
        )
        create_reference(ref)

        response = self.client.get("/show_reference/1")
        self.assertEqual(response.status_code, 200)

        html = response.data.decode("utf-8")

        self.assertIn("Author A", html)
        self.assertIn("Title T", html)
        self.assertIn("2010", html)
        self.assertIn("Journal J", html)

        self.assertNotIn("Publisher P", html)
        self.assertNotIn("Conference C", html)
