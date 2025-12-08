# pylint: disable=redefined-builtin
from reference_types import get_supported_fields

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
        if attribute in ("id", "ref_type", "citation_key"):
            return False
        if callable(getattr(self, attribute)): #filter out methods
            return False
        return bool(getattr(self, attribute))

    def get_bibtex(self) -> str:
        fields = get_supported_fields(self.ref_type)
        res = f"@{self.ref_type}{{{self.citation_key}"

        for field in fields:
            value = getattr(self, field, None)
            if not value:
                continue

            if field == "year":
                res += f",year = {value}"
            else:
                res += f",{field} = '{value}'"

        res += "}"
        return res