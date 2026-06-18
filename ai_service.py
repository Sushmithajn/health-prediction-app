import os
from datetime import date, datetime

import google.generativeai as genai


def _calculate_age(date_of_birth_str):
    dob = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
    today = date.today()

    return (
        today.year
        - dob.year
        - ((today.month, today.day) < (dob.month, dob.day))
    )


def _local_fallback(glucose, haemoglobin, cholesterol):
    issues = []

    if glucose >= 126:
        issues.append("high glucose")
    elif glucose >= 100:
        issues.append("borderline glucose")

    if haemoglobin < 12:
        issues.append("low haemoglobin")
    elif haemoglobin > 17:
        issues.append("high haemoglobin")

    if cholesterol >= 240:
        issues.append("high cholesterol")
    elif cholesterol >= 200:
        issues.append("borderline cholesterol")

    if not issues:
        return "Low risk: Blood values appear to be within normal ranges."

    return (
        "Moderate to high risk: "
        + ", ".join(issues)
        + ". Medical follow-up is recommended."
    )


def generate_health_remark(
    date_of_birth,
    glucose,
    haemoglobin,
    cholesterol,
):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    print("Gemini API Key Found:", bool(api_key))

    if not api_key:
        return _local_fallback(
            glucose,
            haemoglobin,
            cholesterol,
        )

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.0-flash")

        age = _calculate_age(date_of_birth)

        prompt = f"""
You are a healthcare assistant.

Patient:
- Age: {age}
- Glucose: {glucose} mg/dL
- Haemoglobin: {haemoglobin} g/dL
- Cholesterol: {cholesterol} mg/dL

Return ONLY one concise sentence (maximum 25 words)
describing the possible health risk and whether medical
follow-up is advisable.
"""

        response = model.generate_content(prompt)

        if (
            hasattr(response, "text")
            and response.text
            and response.text.strip()
        ):
            return response.text.strip()

        return _local_fallback(
            glucose,
            haemoglobin,
            cholesterol,
        )


    except Exception as exc:
        
        return (
            _local_fallback(
                glucose,
                haemoglobin,
                cholesterol,
                )
                + " (Offline prediction generated)"
                )