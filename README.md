# Hospital Revenue and Performance Analysis

Dataset for a mid-sized (340-bed) multispecialty private hospital, covering **January to October 2026**.

**File:** `Hospital_Revenue_Performance_RAW_Data_clean.csv` (1 sheets x 98 rows)

## Sheets

### 1. `Patient_Admissions` (13 columns)
One row per admission.

| Column | Description |
|---|---|
| Admission_ID | Unique admission key (e.g. ADM-2026-0001) |
| Patient_ID | Fictional patient identifier |
| Age, Gender | Patient demographics |
| Department | One of 10 departments |
| Admission_Type | Emergency / Elective |
| Admission_Date, Discharge_Date | Stay dates |
| Length_of_Stay_Days | Formula: Discharge - Admission |
| Ward_Type | General / Semi-Private / Private / ICU |
| Attending_Doctor_ID | Fictional doctor code |
| Payer_Type | Self-Pay / Private Insurance / Corporate / Government Scheme |
| Outcome | Recovered / Improved / Referred / LAMA / Deceased |
