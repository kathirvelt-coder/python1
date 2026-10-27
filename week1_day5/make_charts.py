"""Creates the 3 presentation charts from clean_data.csv -> chart1/2/3 PNG files."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = Path(__file__).parent
df = pd.read_csv(here / "clean_data.csv")

# Sample budget table (replace with the real one if you have it) - annual, INR
budget = pd.DataFrame({"department": ["Sales", "HR", "IT", "Finance"],
                       "annual_budget": [1_800_000, 1_200_000, 5_000_000, 2_500_000]})

# Chart 1: average monthly salary by department
by_dept = df.groupby("department")["salary"].mean().sort_values()
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(by_dept.index, by_dept.values, color="#3B6EA8")
ax.bar_label(bars, labels=[f"{v:,.0f}" for v in by_dept.values], padding=3)
ax.set_xlabel("Average monthly salary (INR)")
ax.set_title("Finance pays more than double Sales on average")
ax.set_xlim(0, by_dept.max() * 1.15)
plt.tight_layout(); plt.savefig(here / "chart1_avg_salary_by_department.png", dpi=150); plt.close()

# Chart 2: share of annual budget used by payroll
m = df.groupby("department")["salary"].sum().mul(12).rename("annual_payroll").reset_index().merge(budget, on="department")
m["used_pct"] = m["annual_payroll"] / m["annual_budget"] * 100
m = m.sort_values("used_pct")
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(m["department"], m["used_pct"], color="#D9822B")
ax.bar_label(bars, labels=[f"{v:.1f}%" for v in m["used_pct"]], padding=3)
ax.axvline(100, color="red", linestyle="--", linewidth=1)
ax.set_xlim(0, 110)
ax.set_xlabel("Annual payroll as % of department budget (budget = sample data)")
ax.set_title("HR has the least budget headroom")
plt.tight_layout(); plt.savefig(here / "chart2_budget_used_by_department.png", dpi=150); plt.close()

# Chart 3: headcount and average salary by city
c = df.groupby("city")["salary"].agg(employees="count", avg="mean").sort_values("employees")
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(c.index, c["employees"], color="#4C9F70")
ax.bar_label(bars, labels=[f"{n} staff | avg {a:,.0f}" for n, a in zip(c["employees"], c["avg"])], padding=3)
ax.set_xlim(0, c["employees"].max() * 1.6)
ax.set_xlabel("Number of employees")
ax.set_title("Over half the staff are in Chennai")
plt.tight_layout(); plt.savefig(here / "chart3_employees_by_city.png", dpi=150); plt.close()
print("Saved 3 charts")