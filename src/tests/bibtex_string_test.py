import unittest
from entities.reference import Reference

class TestBibtexStrings(unittest.TestCase):
    def test_book_with_required_fields_only(self):
        myref = Reference(
            id=0,
            ref_type="book",
            author="author",
            title="title",
            year=1234
        )
        target = """@book{author1234,author = "author",title = "title",year = "1234"}"""
        self.assertEqual(myref.get_bibtex(), target)

    def test_article_with_required_fields_only(self):
        myref = Reference(
            id=0,
            ref_type="article",
            author="author",
            title="title",
            year=1234
        )
        target = """@article{author1234,author = "author",title = "title",year = "1234"}"""
        self.assertEqual(myref.get_bibtex(), target)

    def test_inproceedings_with_required_fields_only(self):
        myref = Reference(
            id=0,
            ref_type="inproceedings",
            author="author",
            title="title",
            year=1234
        )
        target = """@inproceedings{author1234,author = "author",title = "title",year = "1234"}"""
        self.assertEqual(myref.get_bibtex(), target)