

import re
from datetime import date, datetime

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_full_name(name):
    if not name or not name.strip():
        return "Full name is required."
    if len(name.strip()) < 2:
        return "Full name must be at least 2 characters long."
    if not re.match(r"^[A-Za-z\s.'-]+$", name.strip()):
        return "Full name should only contain letters, spaces, and . ' -"
    return None


def validate_dob(dob_str):
    if not dob_str:
        return "Date of birth is required."
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
    except ValueError:
        return "Date of birth must be a valid date (YYYY-MM-DD)."
    if dob > date.today():
        return "Date of birth cannot be in the future."
   
    if dob.year < 1900:
        return "Date of birth is not realistic."
    return None


def validate_email(email):
    if not email or not email.strip():
        return "Email address is required."
    if not EMAIL_REGEX.match(email.strip()):
        return "Email address format is invalid."
    return None


def validate_numeric_field(value, field_label, min_value=0, max_value=2000):
    
    if value is None or str(value).strip() == "":
        return f"{field_label} is required."
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return f"{field_label} must be a numeric value."
    if numeric_value <= 0:
        return f"{field_label} must be a positive number."
    if numeric_value > max_value:
        return f"{field_label} value seems unrealistic (max {max_value})."
    return None


def validate_patient_form(form):
    
    errors = {}

    name_error = validate_full_name(form.get("full_name", ""))
    if name_error:
        errors["full_name"] = name_error

    dob_error = validate_dob(form.get("date_of_birth", ""))
    if dob_error:
        errors["date_of_birth"] = dob_error

    email_error = validate_email(form.get("email", ""))
    if email_error:
        errors["email"] = email_error

    glucose_error = validate_numeric_field(form.get("glucose"), "Glucose", max_value=1000)
    if glucose_error:
        errors["glucose"] = glucose_error

    haemoglobin_error = validate_numeric_field(form.get("haemoglobin"), "Haemoglobin", max_value=30)
    if haemoglobin_error:
        errors["haemoglobin"] = haemoglobin_error

    cholesterol_error = validate_numeric_field(form.get("cholesterol"), "Cholesterol", max_value=1000)
    if cholesterol_error:
        errors["cholesterol"] = cholesterol_error

    return errors
