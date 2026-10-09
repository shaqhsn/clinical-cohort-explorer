
import sqlite3

DB_NAME = "snomed.db"


def create_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concepts (
            concept_id TEXT PRIMARY KEY,
            term TEXT,
            active INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            relationship_id TEXT PRIMARY KEY,
            source_id TEXT,
            destination_id TEXT,
            type_id TEXT,
            active INTEGER
        )
    """)

    connection.commit()
    connection.close()
    print("SNOMED database created successfully!")


if __name__ == "__main__":
    create_database()
