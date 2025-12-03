from datetime import datetime
from flask import redirect, render_template, request, jsonify, flash
import markupsafe
from db_helper import reset_db
from config import app, test_env
from entities.reference import Reference
from repositories.reference_repository import (
    get_references, create_reference, get_one_reference,
    delete_reference, DeleteFailureError, SelectFailureError)
from util import validate_reference

# pylint: disable=too-many-branches,too-many-statements,too-many-nested-blocks
@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def validate_reference_data(data, original=None):
    errors = {}

    if not data.get("author") or data["author"].strip() == "":
        errors["author"] = "Author is required."

    if not data.get("title") or data["title"].strip() == "":
        errors["title"] = "Title is required."

    year = data.get("year")
    if not year:
        errors["year"] = "Year is required."
    else:
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 0 or year_int > current_year:
                errors["year"] = (
                    f"Year must be between 0 and {current_year}."
                )
        except ValueError:
            errors["year"] = "Year must be a valid integer."

    ref_type = data.get("ref_type")

    if original and ref_type == "article":
        if (
            original.journal
            and (not data.get("journal") or data["journal"].strip() == "")
        ):
            errors["journal"] = "Journal is required for articles."
        if (
            original.volume
            and (not data.get("volume") or data["volume"].strip() == "")
        ):
            errors["volume"] = "Volume is required for articles."

    if original and ref_type == "book":
        if (
            original.publisher
            and (not data.get("publisher") or data["publisher"].strip() == "")
        ):
            errors["publisher"] = "Publisher is required for books."

    if original and ref_type == "inproceedings":
        if (
            original.booktitle
            and (not data.get("booktitle") or data["booktitle"].strip() == "")
        ):
            errors["booktitle"] = (
                "Booktitle is required for inproceedings."
            )

    return errors


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

@app.route("/bibtex")
def bibtex_listing():
    references_to_show = get_references()
    return render_template("bibtex.html", references = references_to_show)

@app.route("/delete_reference/<int:ref_id>", methods=["POST"])
def remove_reference(ref_id):
    try:
        delete_reference(ref_id)
        return redirect("/")
    except DeleteFailureError:
        flash(f"id ${ref_id} does not exist in the database")
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



@app.route("/edit_reference/<int:ref_id>")
def edit_reference_form(ref_id):
    all_references = get_references()
    for ref in all_references:
        if ref.id == int(ref_id):
            return render_template("edit_reference.html", reference = ref, errors={})
    return redirect("/")

@app.route("/update_reference/<int:ref_id>", methods=["POST"])
def update_reference(ref_id):
    original = None
    for ref in get_references():
        if ref.id == int(ref_id):
            original = ref
            break

    fields = [
        "ref_type", "author", "title", "year", "journal", "volume",
        "publisher", "booktitle", "edition", "chapter", "pages",
        "doi", "address"
    ]
    data = {f: request.form.get(f) for f in fields}
    errors = validate_reference_data(data, original)
    if errors:
        temp_reference = Reference(ref_id, **data)
        return render_template("edit_reference.html",
                                reference = temp_reference, errors=errors)

    updated_reference = Reference(ref_id, **data)
    delete_reference(ref_id)
    create_reference(updated_reference)
    return redirect("/")


@app.route("/show_reference/<int:ref_id>")
def show_reference(ref_id):
    try:
        reference = get_one_reference(ref_id)
        return render_template("show_reference.html", reference = reference)
    except SelectFailureError:
        flash(f"id {ref_id} does not exist in the database")
        return redirect("/")



# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
