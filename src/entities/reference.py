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

    def get_alias(self) -> str:
        return f"{self.author[:3]}{self.title[:3]}"

    def check_attribute(self, attribute: str) -> bool:
        if attribute.startswith("__"):
            return False
        if attribute in ("id", "ref_type"):
            return False
        if callable(getattr(self, attribute)):
            return False
        return getattr(self, attribute) is not None

    def get_bibtex(self) -> str:
        res = f"@{self.ref_type}"+"{"+f"{self.get_alias()}"
        for attribute in dir(self):
            if not self.check_attribute(attribute):
                continue
            if attribute=="year":
                res+=f",\nyear = {self.year}"
            else:
                res+=f",\n{attribute} = '{getattr(self, attribute)}'"
        res+="\n}"
        return res