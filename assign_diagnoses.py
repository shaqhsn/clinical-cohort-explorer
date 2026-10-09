
import sqlite3

DATABASE = "snomed.db"


def assign_diagnoses():
    conn = sqlite3.connect(DATABASE)

    try:
        # Find the available concept sets
        roots = conn.execute("""
            SELECT root_concept_id, COUNT(*)
            FROM cohort_concepts
            GROUP BY root_concept_id
        """).fetchall()

        if not roots:
            print("No SNOMED CT concept sets found.")
            return

        print("\nAvailable concept sets:")

        for index, (root_id, count) in enumerate(roots, 1):
            print(f"{index}. {root_id} ({count} concepts)")

        choice = int(input("\nSelect concept set number: ")) - 1

        if choice < 0 or choice >= len(roots):
            print("Invalid selection.")
            return

        root_id = roots[choice][0]

        # Retrieve concepts from the selected hierarchy
        concepts = conn.execute("""
            SELECT concept_id, term
            FROM cohort_concepts
            WHERE root_concept_id = ?
              AND concept_id != ?
            ORDER BY term
            LIMIT 4
        """, (root_id, root_id)).fetchall()

        if len(concepts) < 4:
            print("Not enough descendant concepts for this demo.")
            return

        # Assign four different descendants to four patients
        conn.execute("DELETE FROM patient_diagnoses")

        diagnoses = [
            (1, concepts[0][0]),
            (2, concepts[1][0]),
            (3, concepts[2][0]),
            (4, concepts[3][0])
        ]

        conn.executemany("""
            INSERT INTO patient_diagnoses
            (patient_id, concept_id)
            VALUES (?, ?)
        """, diagnoses)

        conn.commit()

        print("\nAssigned diagnoses:")

        for patient_id, concept_id in diagnoses:
            term = next(
                name for code, name in concepts
                if code == concept_id
            )
            print(f"Patient {patient_id}: {term}")

        print("\nPatient 5 has no diagnosis recorded.")

    finally:
        conn.close()


if __name__ == "__main__":
    assign_diagnoses()
