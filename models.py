
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "patients.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def create_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO patients
            (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_patients():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM patients ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


def get_patient_by_id(patient_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM patients WHERE id = ?", (patient_id,)
    ).fetchone()
    conn.close()
    return row


def update_patient(patient_id, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_connection()
    conn.execute(
        """
        UPDATE patients
        SET full_name = ?, date_of_birth = ?, email = ?, glucose = ?,
            haemoglobin = ?, cholesterol = ?, remarks = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, patient_id),
    )
    conn.commit()
    conn.close()


def delete_patient(patient_id):
    conn = get_connection()
    conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()
