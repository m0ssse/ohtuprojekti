import unittest
from entities.reference import Reference

class TestBibtexStrings(unittest.TestCase):
    def test_book_with_required_fields_only(self):
        myref = Reference(id=0, ref_type="book", citation_key="", author="author", title="title", year=1234)
        target = """@book{auttit,author = 'author',title = 'title',year = 1234}"""
        self.assertEqual(myref.get_bibtex(), target)

    def test_article_with_required_fields_only(self):
        myref = Reference(id=0, ref_type="article", citation_key="", author="author", title="title", year=1234)
        target = """@article{auttit,author = 'author',title = 'title',year = 1234}"""
        self.assertEqual(myref.get_bibtex(), target)

    def test_inproceedings_with_required_fields_only(self):
        myref = Reference(id=0, ref_type="inproceedings", citation_key="", author="author", title="title", year=1234)
        target = """@inproceedings{auttit,author = 'author',title = 'title',year = 1234}"""
        self.assertEqual(myref.get_bibtex(), target)