REFERENCE_FIELDS = {
    "article": ["author", "title", "journal", "year", "volume", "pages"],
    "inproceedings": ["author", "title", "year", "booktitle"],
    "book": ["author", "title", "year", "publisher"]
}


def get_supported_fields(ref_type:str):
    return REFERENCE_FIELDS.get(ref_type, ["author", "title", "year"])