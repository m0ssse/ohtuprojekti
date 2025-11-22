# pylint: disable=redefined-builtin

class Reference:
    def __init__(self, id,
        ref_type, author, title,
        year, booktitle=None, publisher=None,
        journal=None, pages=None, volume=None,
        edition=None, doi=None, chapter=None, address=None):

        self.id = id
        self.ref_type = ref_type
        self.author = author
        self.title = title
        self.year = year
        self.booktitle = booktitle
        self.publisher = publisher
        self.journal = journal
        self.pages = pages
        self.volume = volume
        self.edition = edition
        self.doi = doi
        self.chapter = chapter
        self.address = address
