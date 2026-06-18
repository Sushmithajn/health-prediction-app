
import os
from datetime import date

from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, flash

import models
import validators
import ai_service



app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")


models.init_db()


@app.context_processor
def inject_today():
   
    return {"today": date.today().isoformat()}


@app.route("/")
def index():
   
    patients = models.get_all_patients()
    return render_template("index.html", patients=patients)


@app.route("/patients/new", methods=["GET", "POST"])
def create_patient():
    
    if request.method == "POST":
        errors = validators.validate_patient_form(request.form)

        if errors:
           
            return render_template(
                "add_edit.html",
                patient=request.form,
                errors=errors,
                form_action=url_for("create_patient"),
                page_title="Add Patient",
            )

        full_name = request.form["full_name"].strip()
        dob = request.form["date_of_birth"]
        email = request.form["email"].strip()
        glucose = float(request.form["glucose"])
        haemoglobin = float(request.form["haemoglobin"])
        cholesterol = float(request.form["cholesterol"])

       
        remarks = ai_service.generate_health_remark(dob, glucose, haemoglobin, cholesterol)

        models.create_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        flash(f"Patient '{full_name}' added successfully.", "success")
        return redirect(url_for("index"))

  
    return render_template(
        "add_edit.html",
        patient={},
        errors={},
        form_action=url_for("create_patient"),
        page_title="Add Patient",
    )


@app.route("/patients/<int:patient_id>")
def view_patient(patient_id):
    """Shows full detail for a single patient (a focused 'Read' view)."""
    patient = models.get_patient_by_id(patient_id)
    if patient is None:
        flash("Patient record not found.", "danger")
        return redirect(url_for("index"))
    return render_template("view.html", patient=patient)


@app.route("/patients/<int:patient_id>/edit", methods=["GET", "POST"])
def edit_patient(patient_id):
    """Handles the 'Update' part of CRUD."""
    patient = models.get_patient_by_id(patient_id)
    if patient is None:
        flash("Patient record not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        errors = validators.validate_patient_form(request.form)

        if errors:
            return render_template(
                "add_edit.html",
                patient=request.form,
                errors=errors,
                form_action=url_for("edit_patient", patient_id=patient_id),
                page_title="Edit Patient",
            )

        full_name = request.form["full_name"].strip()
        dob = request.form["date_of_birth"]
        email = request.form["email"].strip()
        glucose = float(request.form["glucose"])
        haemoglobin = float(request.form["haemoglobin"])
        cholesterol = float(request.form["cholesterol"])

        remarks = ai_service.generate_health_remark(dob, glucose, haemoglobin, cholesterol)

        models.update_patient(
            patient_id, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks
        )
        flash(f"Patient '{full_name}' updated successfully.", "success")
        return redirect(url_for("index"))

    return render_template(
        "add_edit.html",
        patient=patient,
        errors={},
        form_action=url_for("edit_patient", patient_id=patient_id),
        page_title="Edit Patient",
    )


@app.route("/patients/<int:patient_id>/delete", methods=["POST"])
def delete_patient(patient_id):
   
    patient = models.get_patient_by_id(patient_id)
    if patient is not None:
        models.delete_patient(patient_id)
        flash(f"Patient '{patient['full_name']}' deleted.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)
