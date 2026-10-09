
import sqlite3
import urllib.error

from search_snomed import search_snomed, get_descendants
from cohort_database import save_cohort_concepts

DATABASE = "snomed.db"


def select_concept():
    """Search SNOMED CT and let the user choose a concept."""

    term = input("\nEnter a clinical condition: ").strip()

    if not term:
        print("Please enter a condition.")
        return None

    results = search_snomed(term)

    if not results:
        print("No matching concepts found.")
        return None

    choice = input("\nSelect a concept number: ").strip()

    if not choice.isdigit():
        print("Please enter a valid number.")
        return None

    index = int(choice) - 1

    if index < 0 or index >= len(results):
        print("Invalid selection.")
        return None

    concept = results[index]

    if concept.get("inactive"):
        print("Please select an active concept.")
        return None

    return concept


def extract_patients(root_concept_id):
    """Find patients whose diagnoses match the selected hierarchy."""

    conn = sqlite3.connect(DATABASE)

    try:
        rows = conn.execute("""
            SELECT DISTINCT
                p.patient_id,
                p.age,
                p.sex,
                c.term
            FROM patients AS p
            JOIN patient_diagnoses AS d
                ON p.patient_id = d.patient_id
            JOIN cohort_concepts AS c
                ON d.concept_id = c.concept_id
            WHERE c.root_concept_id = ?
            ORDER BY p.patient_id
        """, (root_concept_id,)).fetchall()

        return rows

    finally:
        conn.close()


def main():
    print("\n=== Clinical Cohort Explorer ===")

    concept = select_concept()

    if concept is None:
        return

    concept_id = concept["code"]
    concept_name = concept["display"]

    print(f"\nSelected condition: {concept_name}")

    # Retrieve hierarchy from SNOMED CT
    concepts = get_descendants(concept_id)

    # Save concepts to SQLite
    save_cohort_concepts(concept_id, concepts)

    # Find matching patients
    patients = extract_patients(concept_id)

    print("\n=== Cohort Results ===")

    if not patients:
        print("No matching patients found.")
        print(
            "Make sure you have created synthetic patients "
            "and assigned example diagnoses."
        )
        return

    for patient_id, age, sex, diagnosis in patients:
        print(
            f"Patient {patient_id} | "
            f"Age: {age} | "
            f"Sex: {sex} | "
            f"Diagnosis: {diagnosis}"
        )

    print(f"\nTotal matching records: {len(patients)}")


if __name__ == "__main__":
    try:
        main()
    except sqlite3.OperationalError as error:
        print(f"\nDatabase error: {error}")
        print(
            "Run create_patients.py and assign_diagnoses.py "
            "to set up the synthetic demonstration data."
        )
    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        TimeoutError,
        ValueError,
        RuntimeError
    ) as error:
        print(f"\nError: {error}")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
