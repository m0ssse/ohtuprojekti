# pylint: disable=redefined-builtin

class Reference:
    def __init__(self, id, ref_type, author,
        title, year, citation_key=None,
        booktitle=None, publisher=None, journal=None,
        pages=None, volume=None, edition=None,
        doi=None, chapter=None, address=None):

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
        self.citation_key = self.get_citation_key(citation_key)

    def get_citation_key(self, citation_key: str) -> str:
        if citation_key:
            return citation_key
        surname = self.author.lower().split()[0]
        new_citation_key = f"{surname}{self.year}"
        return new_citation_key

    def check_attribute(self, attribute: str) -> bool:
        if attribute.startswith("__"): #filter out built-ins
            return False
        if attribute in ("id", "ref_type"):
            return False
        if callable(getattr(self, attribute)): #filter out methods
            return False
        return getattr(self, attribute) is not None

    def get_bibtex(self) -> str:
        res = f"@{self.ref_type}"+"{"+f"{self.citation_key}"
        for attribute in dir(self):
            if not self.check_attribute(attribute):
                continue
            if attribute=="year":
                res+=f",\nyear = {self.year}"
            else:
                res+=f",\n{attribute} = '{getattr(self, attribute)}'"
        res+="\n}"
        return res