from sqlalchemy import text
from config import db
from entities.reference import Reference
from util import valid_criteria

class DeleteFailureError(Exception):
    pass

class SelectFailureError(Exception):
    pass

def get_references(order_field = "author", order_dir = "ASC") -> list[Reference]:
    if not valid_criteria(order_field, order_dir):
        order_field = "author"
        order_dir = "ASC"
    result = db.session.execute(
        text(f"SELECT * FROM reference ORDER BY {order_field} {order_dir}")
    )
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
def create_reference(ref: Reference) -> bool:
    if check_key_exists(citation_key=ref.citation_key):
        return False

    fields = vars(ref)
    fields = { key: value for key, value in fields.items() if key != "id" }
    columns = ", ".join(fields.keys())
    placeholders = ", ".join([f":{param}" for param in fields.keys()])

    sql = text(f"INSERT INTO reference ({columns}) VALUES ({placeholders})")
    db.session.execute(sql, fields)
    db.session.commit()
    return True


def check_key_exists(citation_key: "text") -> bool:
    sql = text("""SELECT EXISTS (
        SELECT 1 FROM reference WHERE citation_key = :citation_key
        )""")
    result = db.session.execute(sql, { "citation_key": citation_key })
    result = result.fetchone()
    print(result[0])
    return result[0]
