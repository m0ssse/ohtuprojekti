from sqlalchemy import text
from config import db
from entities.reference import Reference
from util import valid_criteria

class DeleteFailureError(Exception):
    pass

class SelectFailureError(Exception):
    pass

def get_references(sorting_criteria = "author") -> list[Reference]:
    if not valid_criteria(sorting_criteria):
        sorting_criteria = "author"
    result = db.session.execute(text(f"SELECT * FROM reference ORDER BY {sorting_criteria}"))
    rows = result.fetchall()
    # rows are casted into Reference objects
    references = [Reference(**dict(row._mapping)) for row in rows]
    return references


def get_one_reference(ref_id: int) -> Reference:
    sql = text("SELECT * FROM reference WHERE id = :id")
    result = db.session.execute(sql, { "id": ref_id })
    row = result.fetchone()
    if row is None:
        raise SelectFailureError(f"Failed to get a reference with id {ref_id}")
    reference = Reference(**dict(row._mapping))
    return reference


def delete_reference(ref_id: int):
    sql = text("DELETE FROM reference WHERE id = :id")
    result = db.session.execute(sql, { "id": ref_id })
    db.session.commit()
    if result.rowcount == 0:
        raise DeleteFailureError(f"Failed to delete a reference with id {ref_id}")

# create_reference takes a parameter of class Reference and inserts all of it's variables
# into the reference table.
def create_reference(ref: Reference):
    fields = vars(ref)
    fields = { key: value for key, value in fields.items() if key != "id" }
    columns = ", ".join(fields.keys())
    placeholders = ", ".join([f":{param}" for param in fields.keys()])
    sql = text(f"INSERT INTO reference ({columns}) VALUES ({placeholders})")
    db.session.execute(sql, fields)
    db.session.commit()
