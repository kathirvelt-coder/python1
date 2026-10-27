"""
Week 1 - Day 5 | Data Cleaning for columns: id, name, department, salary, city
Usage:  python clean_my_data.py employees_messy.csv
Outputs: clean_data.csv, cleaning_summary.csv, decisions_log.csv, outliers_boxplot.png
"""
import sys
import pandas as pd

path = sys.argv[1] if len(sys.argv) > 1 else "employees_messy.csv"
raw = pd.read_csv(path)
df = raw.copy()
log = []


def note(column, issue, action, reason):
    log.append({"column": column, "issue": issue, "action": action, "reason": reason})


# 1. BEFORE snapshot ---------------------------------------------------------
before = {
    "Rows": len(raw),
    "Missing values": int(raw.isna().sum().sum()),
    "Duplicates": int(raw.duplicated().sum()),
}

# 2. Standardise text --------------------------------------------------------
for col in ["name", "department", "city"]:
    df[col] = df[col].astype("string").str.strip().str.title()
df["department"] = df["department"].replace({"Hr": "HR", "It": "IT"})  # acronyms stay uppercase
note("name, department, city", "Extra spaces and mixed case (' priya ', 'RAHUL', 'hr')",
     "strip + Title Case (HR and IT kept uppercase)",
     "One spelling per value so grouping and duplicate checks work")

# 3. Fix data types ----------------------------------------------------------
df["salary"] = pd.to_numeric(
    df["salary"].astype("string").str.replace(r"[^0-9.]", "", regex=True), errors="coerce")
note("salary", "Text such as '₹45,000' or '58,000'", "remove symbols/commas, convert to number",
     "Needed for median, IQR and any maths")
df["id"] = pd.to_numeric(df["id"], errors="coerce")

# 4. Missing id -> drop (before duplicates, so rows can be identified) --------
n_missing_id = int(df["id"].isna().sum())
df = df.dropna(subset=["id"])
df["id"] = df["id"].astype(int)
note("id", f"{n_missing_id} missing", "drop rows",
     "id is the identifier; a row with no id can't be traced or matched")

# 5. Duplicates --------------------------------------------------------------
# a) same person entered twice with a different id, b) same id twice
n0 = len(df)
df = df.drop_duplicates(subset=["name", "department", "salary", "city"], keep="first")
df = df.drop_duplicates(subset=["id"], keep="first")
note("all columns", f"{n0 - len(df)} duplicate rows (found after standardising text)",
     "drop, keep first", "Duplicates would double-count people and distort averages")

# 6. Missing values ----------------------------------------------------------
n_name = int(df["name"].isna().sum())
df["name"] = df["name"].fillna("Unknown")
note("name", f"{n_name} missing", "fill with 'Unknown'", "Name is a label, not used in calculations")

n_dep = int(df["department"].isna().sum())
df["department"] = df["department"].fillna(df["department"].mode()[0])
note("department", f"{n_dep} missing", "fill with mode",
     "Categorical: most common department changes the data least")

n_city = int(df["city"].isna().sum())
df["city"] = df["city"].fillna(df["city"].mode()[0])
note("city", f"{n_city} missing", "fill with mode", "Categorical: use the most frequent city")

n_sal = int(df["salary"].isna().sum())
df["salary"] = df["salary"].fillna(df.groupby("department")["salary"].transform("median"))
df["salary"] = df["salary"].fillna(df["salary"].median())
note("salary", f"{n_sal} missing", "fill with department median (overall median as fallback)",
     "Salary is skewed so median beats mean, and department gives context")

# 7. Outliers (IQR rule) -----------------------------------------------------
raw_salary = df["salary"].copy()  # for the box plot
q1, q3 = df["salary"].quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
mask = (df["salary"] < low) | (df["salary"] > high)
df["salary_outlier"] = mask
df["salary"] = df["salary"].clip(low, high)
note("salary", f"{int(mask.sum())} outliers outside [{low:,.0f}, {high:,.0f}] (IQR x 1.5)",
     "flag in salary_outlier and cap at the bound",
     "Employee is real, so keep the row, but an extreme value would distort the mean")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.figure(figsize=(4, 4))
    plt.boxplot(raw_salary)
    plt.title("Salary box plot (before capping)")
    plt.tight_layout()
    plt.savefig("outliers_boxplot.png", dpi=120)
except ImportError:
    print("matplotlib not installed - skipping box plot")

# 8. AFTER snapshot and save -------------------------------------------------
after = {
    "Rows": len(df),
    "Missing values": int(df.drop(columns="salary_outlier").isna().sum().sum()),
    "Duplicates": int(df.duplicated().sum()),
}
summary = pd.DataFrame({"Metric": list(before), "Before": list(before.values()),
                        "After": list(after.values())})

df = df.sort_values("id").reset_index(drop=True)
df.to_csv("clean_data.csv", index=False)
summary.to_csv("cleaning_summary.csv", index=False)
pd.DataFrame(log).to_csv("decisions_log.csv", index=False)

print(summary.to_string(index=False))
print(f"\nRows {before['Rows']} -> {after['Rows']} | "
      f"Missing values {before['Missing values']} -> {after['Missing values']} | "
      f"Duplicates {before['Duplicates']} -> {after['Duplicates']}")
print("\nDecisions:")
print(pd.DataFrame(log).to_string(index=False))