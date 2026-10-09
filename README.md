# Clinical Cohort Explorer

A small Python project exploring how SNOMED CT hierarchies can be used to identify patient cohorts for clinical research.

Instead of relying on fixed lists of diagnosis codes, the tool lets users search for a clinical condition and retrieves its related concepts using SNOMED CT Expression Constraint Language (ECL).

### What it does

- Searches SNOMED CT through a FHIR terminology API.
- Retrieves a selected concept and its descendants using ECL.
- Stores the results in SQLite.
- Uses SQL to identify matching patients in a synthetic dataset.

### Technologies

Python, SQL, SQLite, SNOMED CT, ECL, HL7 FHIR

### How to run

```bash
python3 search_snomed.py
python3 create_patients.py
python3 assign_diagnoses.py
```

Run `cohort_query.sql` against `snomed.db` to extract matching patients.

### Next steps

- Add recursive SQL queries for SNOMED CT hierarchies.
- Improve the synthetic patient dataset.
- Add terminology version tracking and tests.

*This is a learning project using synthetic patient data, not a clinically validated cohort extraction tool.*