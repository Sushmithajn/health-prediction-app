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
├── app.py              
├── models.py           
├── validators.py       
├── ai_service.py       
├── templates/
│   ├── base.html       
│   ├── index.html       
│   ├── add_edit.html      
│   └── view.html          
├── static/css/style.css  
├── requirements.txt
├── .env         
└── .gitignore             
```

## Setup & Run Locally

1. **Clone the repo and enter the folder**
   ```bash
   git clone <github.com/Sushmithajn/health-prediction-app>
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
   GEMINI_API_KEY=sk-ant-your-own-key-here
   ``` 

5. **Run the app**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

The SQLite database file (`patients.db`) is created automatically on first
run in the project folder.

