# Methods and review notes

## Model

`gini_index ~ demox_eiu + income_per_person + invest_pct_gdp + tax_pct_gdp`

The model includes an intercept and uses all 11 complete annual observations, 2006–2016. Reported standard errors and p-values are conventional OLS quantities, not heteroskedasticity- or autocorrelation-robust estimates. There is no train/test split or validated forecast.

## Input dictionary

| Column | Interpretation / caveat |
|---|---|
| country | Expected to be United Kingdom |
| year | Unique annual observation |
| demox_eiu | Democracy-related indicator; source scale unverified |
| income_per_person | Income indicator; currency and price basis undocumented |
| invest_pct_gdp | Investment indicator, labelled percentage of GDP |
| tax_pct_gdp | Tax indicator, labelled percentage of GDP |
| gini_index | Supplied inequality index; exact definition/source unverified |

## Changes from the 2023 script

- Replaced `/cloud/project` working-directory dependence with an explicit input argument.
- Moved package installation out of the analysis execution path.
- Added schema, type, missing-value, country and duplicate-year checks.
- Saved named outputs and R session information instead of relying on console history.
- Removed an invalid interpretation: calculating a Gini coefficient across annual national mean incomes measures dispersion across years, not inequality among households.
- Replaced an income line grouped by year with explicit chronological plotting.
- Retained the original regression specification and verified its coefficients independently.
- Excluded workspace caches, session history, the source workbook and the old Word transcript from publication.

The results should be read as a transparent demonstration of analytical workflow. Data provenance, sample size and temporal dependence limit substantive interpretation.
