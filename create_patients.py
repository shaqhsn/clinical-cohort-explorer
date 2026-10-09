
import sqlite3

DATABASE = "snomed.db"


def create_synthetic_patients():
    conn = sqlite3.connect(DATABASE)

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY,
                age INTEGER,
                sex TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS patient_diagnoses (
                patient_id INTEGER,
                concept_id TEXT,
                FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id)
            )
        """)

        patients = [
            (1, 45, "Female"),
            (2, 62, "Male"),
            (3, 38, "Female"),
            (4, 71, "Male"),
            (5, 54, "Female")
        ]

        conn.executemany("""
            INSERT OR REPLACE INTO patients
            (patient_id, age, sex)
            VALUES (?, ?, ?)
        """, patients)

        conn.commit()

        print("Created 5 synthetic patients.")

    finally:
        conn.close()


if __name__ == "__main__":
    create_synthetic_patients()
