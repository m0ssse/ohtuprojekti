from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from config import app, test_env
from entities.reference import Reference
from repositories.reference_repository import (
    get_references, create_reference, delete_reference)
from util import validate_reference

@app.route("/")
def index():
    n = len(get_references())
    return render_template("index.html", ref_count = n)

@app.route("/new_reference")
def new_reference():
    return render_template("new_reference.html")

@app.route("/references")
def references():
    all_references = get_references()
    return render_template("references.html", references = all_references)

@app.route("/delete_reference/<int:ref_id>", methods=["POST"])
def remove_reference(ref_id):
    delete_reference(ref_id)
    return redirect("/")

@app.route("/make_reference", methods=["POST"])
def make_reference():
    form_ok, missing_fields = validate_reference(request.form)
    if not form_ok:
        flash(f"The following required fields are missing: {', '.join(missing_fields)}")
        return redirect("/new_reference")
    ref_id = len(get_references()) + 1
    fields = [
        "ref_type", "citation_key", "author", "title", "year", "journal", "volume",
        "publisher", "booktitle", "edition", "chapter", "pages",
        "doi", "address"
    ]
    data = {f: request.form.get(f) for f in fields}

    reference = Reference(ref_id, **data)
    create_reference(reference)
    return redirect("/")

@app.route("/show_reference/<int:ref_id>")
def show_reference(ref_id):
    all_references = get_references()
    for ref in all_references:
        if ref.id == int(ref_id):
            return render_template("show_reference.html", reference = ref)
    return redirect("/")

#@app.route("/create_todo", methods=["POST"])
#def todo_creation():
#    content = request.form.get("content")

#    try:
#        validate_todo(content)
#        create_todo(content)
#        return redirect("/")
#    except Exception as error:
#        flash(str(error))
#        return  redirect("/new_todo")

#@app.route("/toggle_todo/<todo_id>", methods=["POST"])
#def toggle_todo(todo_id):
#    set_done(todo_id)
#    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
