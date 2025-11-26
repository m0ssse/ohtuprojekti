import unittest
from entities.reference import Reference
from db_helper import reset_db
from repositories.reference_repository import (
    create_reference, delete_reference,
    get_references, get_one_reference,
    DeleteFailureError, SelectFailureError
)
from app import app

class TestReferenceMethods(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        reset_db()

    def test_valid_reference_is_created(self):
        ref = Reference(id=1, ref_type="book", author="test", title="title", year=2003)
        create_reference(ref)
        references = get_references()
        self.assertEqual(len(references), 1)
        self.assertEqual(type(references[0]), type(ref))
        self.assertEqual(references[0].id, ref.id)
        self.assertEqual(references[0].author, ref.author)
        self.assertEqual(references[0].title, ref.title)
        self.assertEqual(references[0].year, ref.year)


    def test_get_references_returns_correct_amount(self):
        ref1 = Reference(id=1, ref_type="book", author="test", title="title", year=2003)
        create_reference(ref1)
        ref2 = Reference(id=2, ref_type="book", author="test2", title="title2", year=2004)
        create_reference(ref2)
        references = get_references()
        self.assertEqual(type(references), list)
        self.assertEqual(len(references), 2)

    def test_delete_reference_removes_references(self):
        ref1 = Reference(id=1, ref_type="book", author="test", title="title", year=2003)
        create_reference(ref1)
        ref2 = Reference(id=2, ref_type="book", author="test2", title="title2", year=2004)
        create_reference(ref2)
        delete_reference(ref_id=1)
        references = get_references()
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0].id, ref2.id)

    def test_get_one_reference_returns_correct_value(self):
        ref1 = Reference(id=1, ref_type="book", author="test", title="title", year=2003)
        create_reference(ref1)
        ref2 = Reference(id=2, ref_type="book", author="test2", title="title2", year=2004)
        create_reference(ref2)
        reference = get_one_reference(ref_id=2)
        self.assertEqual(type(reference), Reference)
        self.assertEqual(reference.id, ref2.id)
        self.assertEqual(reference.author, ref2.author)
        self.assertEqual(reference.title, ref2.title)
        self.assertEqual(reference.year, ref2.year)

    def test_invalid_delete_fails_and_raises_exception(self):
        ref1 = Reference(id=1, ref_type="book", author="test", title="title", year=2003)
        create_reference(ref1)

        with self.assertRaises(DeleteFailureError):
            delete_reference(ref_id=111112111114313209876)
        references = get_references()
        self.assertEqual(len(references), 1)

    def test_invalid_get_reference_raises_exception(self):
        ref1 = Reference(id=1, ref_type="book", author="test", title="title", year=2003)
        create_reference(ref1)

        with self.assertRaises(SelectFailureError):
            get_one_reference(ref_id=111112111114313209876)