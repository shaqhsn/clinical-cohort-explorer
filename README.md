# Clinical Cohort Explorer

**A Python-based clinical cohort extraction prototype using SNOMED CT, FHIR terminology services, Expression Constraint Language (ECL), SQLite, and SQL.**

## Project Overview

Clinical research often requires identifying patients with a particular medical condition. However, patients may be diagnosed using different levels of specificity within a clinical terminology.

For example, searching only for the SNOMED CT concept *Diabetes mellitus* may miss patients whose diagnoses are recorded using more specific descendant concepts.

This project demonstrates how SNOMED CT's hierarchical relationships can support more comprehensive, terminology-driven cohort identification.

Rather than maintaining manually hardcoded lists of diagnosis codes, the application dynamically retrieves relevant concepts from a FHIR terminology server.

## Objectives

- Search SNOMED CT concepts using clinical terms.
- Allow researchers to select the intended clinical concept.
- Retrieve the selected concept and its descendants using ECL.
- Handle paginated FHIR ValueSet expansion responses.
- Store retrieved concept sets in SQLite.
- Create synthetic patient and diagnosis records.
- Identify matching patients using SQL joins.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Application logic and API requests |
| SNOMED CT | Clinical terminology and concept hierarchy |
| ECL | Hierarchical concept selection |
| HL7 FHIR | Terminology service API |
| Ontoserver | FHIR terminology server |
| SQLite | Local relational database |
| SQL | Patient cohort extraction |
| Git/GitHub | Version control |

## Architecture

The current workflow consists of two stages.

**Terminology extraction**

1. A researcher enters a clinical condition.
2. The application searches SNOMED CT through the FHIR terminology API.
3. The researcher selects the intended concept.
4. The application generates an ECL expression using the selected concept ID.
5. The terminology server returns the concept and its descendants.
6. Python retrieves paginated results and stores the concept set in SQLite.

**Patient cohort extraction**

1. Synthetic patient records are created.
2. SNOMED CT concepts from a selected hierarchy are assigned as fictional diagnoses.
3. SQL joins patient diagnoses with the stored concept set.
4. Patients with matching diagnosis codes are returned.

## SNOMED CT Hierarchy and ECL

SNOMED CT supports hierarchical relationships between clinical concepts.

The application uses the ECL operator:

`<<conceptId`

This expression selects the specified concept and all its descendants.

The concept ID is obtained dynamically from the terminology server rather than hardcoded in the Python application.

For example, the Diabetes mellitus hierarchy can be explored using:

`<<73211009`

The number of matching concepts depends on the terminology edition and version available on the server.

## Project Files

| File | Description |
|---|---|
| `search_snomed.py` | Searches SNOMED CT and retrieves hierarchical concept sets |
| `cohort_database.py` | Saves retrieved concepts into SQLite |
| `create_patients.py` | Creates synthetic patient records |
| `assign_diagnoses.py` | Assigns example diagnoses to synthetic patients |
| `cohort_query.sql` | Identifies patients matching a selected concept set |
| `snomed_loader.py` | Initial local SNOMED CT RF2 loading prototype |

## Running the Project

### Requirements

- Python 3
- Internet access to the configured FHIR terminology server
- SQLite

The current Python implementation uses standard-library modules and does not require third-party Python packages.

### 1. Clone the repository

```bash
git clone https://github.com/shaqhsn/clinical-cohort-explorer.git
cd clinical-cohort-explorer
```

### 2. Search SNOMED CT and save a concept set

```bash
python3 search_snomed.py
```

Enter a clinical condition and select a concept from the results.

The application retrieves the concept hierarchy and saves it to the local SQLite database.

### 3. Create synthetic patients

```bash
python3 create_patients.py
```

### 4. Assign example diagnoses

```bash
python3 assign_diagnoses.py
```

Select a previously saved concept set.

### 5. Run a cohort query

Open the database:

```bash
sqlite3 snomed.db
```

Set the root concept ID to the selected concept set and execute the query:

```sql
.parameter init
.parameter set :root_concept_id '73211009'
.headers on
.mode column
.read cohort_query.sql
```

The result contains synthetic patients whose recorded diagnoses match the selected SNOMED CT concept set.

## Current Limitations

This project is an educational prototype and is not intended for clinical decision-making or production research.

- Patient records are entirely synthetic.
- The current diagnosis assignment script selects example concepts automatically; it does not simulate clinically realistic diagnosis assignment.
- Cohort extraction currently uses SQL joins against a concept set previously expanded by the terminology server.
- Recursive SQL traversal of locally stored SNOMED CT IS-A relationships is not yet implemented.
- Terminology edition and version metadata are not yet persistently recorded.
- Clinical validation, reproducibility checks, and broader automated testing remain future work.
- Terminology availability and API behavior depend on the external FHIR server.

## Planned Enhancements

- Implement recursive SQL queries for local hierarchy traversal.
- Add more realistic synthetic patient diagnoses and negative test cases.
- Record terminology edition and version information.
- Add automated tests and validation.
- Export cohort results to CSV.
- Improve reproducibility and documentation.

## Data Privacy and Licensing

The project uses fictional patient records only.

SNOMED CT terminology content is retrieved through a terminology service. Licensed SNOMED CT release files and terminology databases are not distributed in this repository. SNOMED CT use remains subject to applicable licensing conditions.

## Purpose

This project is part of a hands-on portfolio exploring the intersection of clinical data management, health informatics, terminology services, interoperability, and research data extraction.

Its primary focus is demonstrating how structured clinical terminologies and software engineering techniques can support reusable, more complete clinical cohort definitions.