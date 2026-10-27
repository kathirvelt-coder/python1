# Employee Data Analysis: Summary of Findings

**Author:** Kathirvel T  |  **Date:** 27 Oct 2026  |  **Project:** Week 1 Weekly Project (Part 1 and 2)

## Problem
How is pay distributed across departments and cities, and does payroll fit within each department's budget? The goal is to give HR a clear, number-backed view of where pay and budget pressure sit.

## Data
- Source: employee file with `id, name, department, salary, city` (16 raw rows).
- Cleaning (Task 1): 16 rows -> 13, missing values 4 -> 0, duplicates 1 -> 0 (2 more found after standardising text, plus 1 row dropped for a missing id).
- Choices: text trimmed and title-cased, salary text converted to numbers, missing department/city filled with the mode, missing salary with the department median, one extreme salary (950,000) flagged using the IQR rule and capped at 98,000.
- Salary is treated as monthly (INR). A department budget table was merged in (sample values).

## Key insights
1. **Pay differs sharply by department.** Finance averages 94,000 per month, more than double Sales at 40,000 (a gap of 54,000). Sales also has the widest spread (std about 11,100).
2. **Budget headroom is uneven.** HR uses 93% of its annual budget on payroll, Finance and IT about 90%, and Sales 80%. IT takes 48% of total payroll, in line with having 6 of 13 employees (46%).
3. **Staff are concentrated in Chennai.** 7 of 13 employees (54%) work there. Mumbai has the highest city average (64,333), but this follows the department mix (it includes a Finance employee earning 90,000), not a location effect.

## Recommendations
1. **Plan HR hiring and raises carefully.** With 93% of budget already used, any new headcount or increment needs extra budget. Review Sales pay (lowest average, 80% budget used) before turnover becomes a problem.
2. **Fix data collection.** Enforce validation at entry (numeric salary, standard department/city names, mandatory id) and capture gender, join date and contract type. That would allow real tenure and equity analysis.

## Limitations
- Only 13 employees after cleaning, so averages and correlations are indicative, not conclusive.
- The budget table is sample data and salary is assumed monthly. Budget percentages change if either assumption is wrong.
- Three values were imputed (one salary, one department, one city) and one salary was capped, which slightly shapes the averages (Finance's 94,000 includes the capped value).
- No dates, gender or contract type, so no time trend or pay-equity analysis was possible.