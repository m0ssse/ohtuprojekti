from config import db
from sqlalchemy import text
from entities.reference import Reference

def get_references() -> list[Reference]:
    result = db.session.execute(text("SELECT * FROM reference"))
    rows = result.fetchall()
    # rows are casted into Reference objects
    references = [Reference(**dict(row._mapping)) for row in rows]
    return references

def delete_reference(ref_id: int):
    sql = text("DELETE FROM reference WHERE id = :id")
    db.session.execute(sql, { "id": ref_id })
    db.session.commit()


# create_reference takes a parameter of class Reference and inserts all of it's variables
# into the reference table, excluding the placeholder id.
def create_reference(ref: Reference):
    fields = vars(ref)
    fields = {key: value for key, value in fields.items() if key != "id"}
    columns = ", ".join(fields.keys())
    placeholders = ", ".join([f":{param}" for param in fields.keys()])
    sql = text(f"INSERT INTO reference ({columns}) VALUES ({placeholders})")
    db.session.execute(sql, fields)
    db.session.commit()
