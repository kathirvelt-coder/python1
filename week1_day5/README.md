# Employee Data Analysis (Week 1 Weekly Project)

Cleans a small employee dataset (Task 1) and explores pay, departments, cities and budget use (Task 2).

## Project files
| File | Purpose |
|---|---|
| `clean_my_data.py` | Task 1: cleaning script (missing values, types, duplicates, outliers) |
| `employees_messy.csv` | Raw input data |
| `clean_data.csv` | Cleaned output used for analysis |
| `cleaning_summary.csv`, `decisions_log.csv` | Before/after table and reason for each cleaning decision |
| `task2_exploratory_analysis_final.ipynb` | Task 2: statistics, groupby, correlations, merge, business questions, pivot |
| `make_charts.py` | Builds the 3 presentation charts |
| `findings_summary.md` | One-page report |
| `requirements.txt` | Python packages needed |

## How to run (Windows PowerShell)
1. Clone the repo and go into the project folder:
   ```
   git clone <repo-url>
   cd <repo-folder>\week1_day5
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
4. Clean the data (creates `clean_data.csv`, summary and log):
   ```
   python clean_my_data.py employees_messy.csv
   ```
5. Open `task2_exploratory_analysis_final.ipynb` in VS Code, select the `.venv` kernel and choose **Run All**.
6. Create the charts:
   ```
   python make_charts.py
   ```
7. Export the notebook as the HTML report:
   ```
   jupyter nbconvert --to html task2_exploratory_analysis_final.ipynb
   ```

On Mac/Linux, activate with `source .venv/bin/activate`.

## Notes
- The department budget table in the notebook is sample data, and salary is assumed to be monthly (INR).
- `clean_data.csv` must be in the same folder as the notebook.