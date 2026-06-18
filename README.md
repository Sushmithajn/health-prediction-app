# Health Prediction Application

A simple full-stack web application for managing patient blood test
records, with an external AI API generating a health remark for each
record automatically.

Built for the "Evaluation of AI/ML Skills" assignment.

## Tech Stack

| Layer        | Choice                          | Why |
|--------------|----------------------------------|-----|
| Backend      | Python + Flask                  | Lightweight, explicit routing, no hidden magic — easy to read and explain. |
| Frontend     | HTML + Jinja2 templates + Bootstrap 5 | A classic server-rendered web app keeps the whole request/response cycle in one place, no separate build step or API layer needed. |
| Database     | SQLite (`sqlite3`, built into Python) | Zero setup, file-based, fully persistent. No external DB server needed to run or demo the project. |
| AI/ML API    | Anthropic Claude API (`api.anthropic.com/v1/messages`) | A real, general-purpose AI API used as a clinical-style reasoning engine over the blood test values. Falls back to a local rule-based estimate if no key is configured, so the app always works end-to-end. |

## Features

- **Create / Read / Update / Delete** patient records
- **Server-side validation**: name format, valid email, date of birth
  cannot be in the future, blood test values must be numeric and within a
  sane clinical range
- **AI-generated remarks**: every time a record is created or updated, the
  app calls an external AI API with the patient's age and blood values and
  stores a one-line risk remark in the `Remarks` field
- **Graceful fallback**: if the AI API key isn't set (e.g. for reviewers
  who don't want to add their own key), a transparent local rule-based
  estimate is used instead, clearly labelled `[Offline estimate]`

## Project Structure

```
health-prediction-app/
├── app.py              # Flask routes (CRUD)
├── models.py           # SQLite schema + data access functions
├── validators.py       # All input validation logic
├── ai_service.py       # External AI API call + local fallback logic
├── templates/
│   ├── base.html        # Shared layout, navbar, Bootstrap
│   ├── index.html        # List of all patient records
│   ├── add_edit.html      # Create/Edit form (shared template)
│   └── view.html          # Single patient detail view
├── static/css/style.css  # Minor visual polish on top of Bootstrap
├── requirements.txt
├── .env.example          # Template for required environment variables
└── .gitignore             # Excludes .env and the local *.db file
```

## Setup & Run Locally

1. **Clone the repo and enter the folder**
   ```bash
   git clone <your-repo-url>
   cd health-prediction-app
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and paste in your own Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-own-key-here
   ```
   Get a key at https://console.anthropic.com/. If you skip this step, the
   app still runs fully — it will use the local fallback logic for the
   `Remarks` field instead of a live API call.

5. **Run the app**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

The SQLite database file (`patients.db`) is created automatically on first
run in the project folder.

## How the AI Integration Works

See `ai_service.py` for the full implementation. In short:

1. When a patient record is saved, `generate_health_remark()` is called
   with the date of birth and the three blood test values.
2. It builds a short, structured prompt describing the values against
   typical healthy reference ranges and sends it to Claude's `/v1/messages`
   endpoint via a plain `requests.post()` call.
3. The model's one-line response (e.g. *"Moderate risk: elevated glucose
   suggests possible pre-diabetes, recommend medical follow-up."*) is
   stored directly in the `remarks` column.
4. If the API key is missing or the request fails for any reason (network
   issue, rate limit, etc.), the function catches the error and falls back
   to a simple local rule-based check instead of crashing the request.

This keeps the "external API call" logic fully isolated from the Flask
routes and the database layer, so each piece can be read, tested, or
swapped independently.

## Notes on Validation

All validation lives in `validators.py` and runs server-side before any
database write:

- Full name: required, letters/spaces/`.`/`'`/`-` only
- Date of birth: required, valid date, cannot be in the future
- Email: required, must match a standard `local@domain.tld` pattern
- Glucose / Haemoglobin / Cholesterol: required, must be numeric, must be
  a positive number within a realistic clinical range

If validation fails, the form is re-rendered with the user's existing
input preserved and field-specific error messages shown inline.

## Disclaimer

This is a learning/assignment project. The AI-generated remarks are for
demonstration purposes only and are **not** a substitute for professional
medical advice or diagnosis.
