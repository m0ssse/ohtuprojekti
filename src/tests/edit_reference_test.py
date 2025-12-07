import unittest
from entities.reference import Reference
from db_helper import reset_db
from repositories.reference_repository import create_reference, delete_reference, get_references, get_one_reference
from app import app



class EditReferenceTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        reset_db()

    def tearDown(self):
        reset_db()
        self.app_context.pop()

    def test_edit_reference_valid_data(self):
        ref = Reference(
            1,
            ref_type="article",
            author="Original Author",
            title="Original Title",
            year="2000",
            journal="Original Journal",
            volume="1",
            publisher="",
            booktitle="",
            edition="",
            chapter="",
            pages="",
            doi="",
            address=""
        )
        create_reference(ref)
        ref_id = get_references()[0].id

        response = self.client.post(
            f"/update_reference/{ref_id}",
            data={
                "ref_type": "article",
                "author": "Updated Author",
                "title": "Updated Title",
                "year": "2021",
                "journal": "Updated Journal",
                "volume": "2",
                "publisher": "",
                "booktitle": "",
                "edition": "",
                "chapter": "",
                "pages": "",
                "doi": "",
                "address": ""
            },
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)

        updated_ref = get_references()[0]
        self.assertEqual(updated_ref.author, "Updated Author")
        self.assertEqual(updated_ref.title, "Updated Title")
        self.assertEqual(updated_ref.year, 2021)
        self.assertEqual(updated_ref.journal, "Updated Journal")
        self.assertEqual(updated_ref.volume, "2")

    def test_cannot_clear_publisher(self):
        ref = Reference(
            1,
            ref_type="book",
            author="Author",
            title="Title",
            year="2010",
            journal="",
            volume="",
            publisher="Some Publisher",
            booktitle="",
            edition="",
            chapter="",
            pages="",
            doi="",
            address=""
        )
        create_reference(ref)
        ref_id = get_references()[0].id

        response = self.client.post(
            f"/update_reference/{ref_id}",
            data={
                "ref_type": "book",
                "author": "Author",
                "title": "Title",
                "year": "2010",
                "journal": "",
                "volume": "",
                "publisher": "",
                "booktitle": "",
                "edition": "",
                "chapter": "",
                "pages": "",
                "doi": "",
                "address": ""
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Publisher is required for books.", response.data)

        updated_ref = get_references()[0]
        self.assertEqual(updated_ref.publisher, "Some Publisher")

    def test_year_must_be_valid_integer(self):
        ref = Reference(
            1,
            ref_type="article",
            author="Author",
            title="Title",
            year="2015",
            journal="Journal",
            volume="1",
            publisher="",
            booktitle="",
            edition="",
            chapter="",
            pages="",
            doi="",
            address=""
        )
        create_reference(ref)
        ref_id = get_references()[0].id

        response = self.client.post(
            f"/update_reference/{ref_id}",
            data={
                "ref_type": "article",
                "author": "Author",
                "title": "Title",
                "year": "invalid_year",
                "journal": "Journal",
                "volume": "1",
                "publisher": "",
                "booktitle": "",
                "edition": "",
                "chapter": "",
                "pages": "",
                "doi": "",
                "address": ""
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Year must be a valid integer.", response.data)

        updated_ref = get_references()[0]
        self.assertEqual(updated_ref.year, 2015)
