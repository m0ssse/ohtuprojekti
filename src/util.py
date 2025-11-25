from constants import REQUIRED_FIELDS

class UserInputError(Exception):
    pass

def validate_reference(form_contents) -> tuple:
    missing = []
    form_ok = True
    print(form_contents)
    ref_type = form_contents["ref_type"]
    for field in REQUIRED_FIELDS[ref_type]:
        if field not in form_contents or not form_contents[field]:
            form_ok = False
            missing.append(field)
    return form_ok, missing
