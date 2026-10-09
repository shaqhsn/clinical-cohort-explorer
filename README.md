# Clinical Cohort Explorer

A Python project exploring how SNOMED CT hierarchies can be used to identify patient cohorts for clinical research.

Instead of relying on fixed lists of diagnosis codes, the tool allows users to search for a clinical condition and retrieve its related concepts using SNOMED CT Expression Constraint Language (ECL).

## What it does

- Searches SNOMED CT through a FHIR terminology API.
- Retrieves a selected concept and its descendants using ECL.
- Stores the concepts in SQLite.
- Uses SQL to identify matching patients in a synthetic dataset.

## Technologies

Python, SQL, SQLite, SNOMED CT, ECL, HL7 FHIR

## How to run

Clone the repository and open the project folder:

```bash
git clone https://github.com/shaqhsn/clinical-cohort-explorer.git
cd clinical-cohort-explorer
```

**1. Search for a clinical condition**

```bash
python3 search_snomed.py
```

Enter a condition, such as diabetes, and select the relevant SNOMED CT concept. The script retrieves the concept hierarchy and saves it in SQLite.

**2. Create synthetic patients**

```bash
python3 create_patients.py
```

Creates five fictional patients for testing.

**3. Assign example diagnoses**

```bash
python3 assign_diagnoses.py
```

Select a saved concept set. The script automatically assigns example descendant diagnoses to four patients.

**4. Extract the patient cohort**

Open SQLite:

```bash
sqlite3 snomed.db
```

Run the cohort query:

```sql
.parameter init
.parameter set :root_concept_id '73211009'
.headers on
.mode column
.read cohort_query.sql
.quit
```

Replace `73211009` with the SNOMED CT ID of the concept selected in Step 1.

The query returns patients whose recorded diagnoses match the selected concept hierarchy.


*This is a learning project using synthetic patient data. It is not intended for clinical use or validated research extraction.*