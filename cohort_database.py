
import sqlite3
from datetime import datetime, timezone

DATABASE = "snomed.db"


def save_cohort_concepts(root_concept_id, concepts):
    """Save the selected concept set into SQLite."""

    conn = sqlite3.connect(DATABASE)

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cohort_concepts (
                root_concept_id TEXT NOT NULL,
                concept_id TEXT NOT NULL,
                term TEXT,
                extraction_date TEXT NOT NULL,
                PRIMARY KEY (root_concept_id, concept_id)
            )
        """)

        extraction_date = datetime.now(timezone.utc).isoformat()

        for concept in concepts:
            conn.execute("""
                INSERT OR REPLACE INTO cohort_concepts
                (root_concept_id, concept_id, term, extraction_date)
                VALUES (?, ?, ?, ?)
            """, (
                root_concept_id,
                concept["code"],
                concept.get("display", ""),
                extraction_date
            ))

        conn.commit()
        print(f"\nSaved {len(concepts)} concepts to SQLite.")

    finally:
        conn.close()
