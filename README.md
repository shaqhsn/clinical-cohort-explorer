## How to run

Run the application:

```bash
python3 main.py
```

Enter a clinical condition and select a SNOMED CT concept. The application retrieves its descendants through a FHIR terminology service and matches them against the local synthetic patient dataset.

To set up the demonstration patient data for the first time, run:

```bash
python3 create_patients.py
python3 assign_diagnoses.py
```

The project uses synthetic patient data only.