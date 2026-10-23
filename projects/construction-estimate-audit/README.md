# Construction Estimate Formula and Regression Audit

An analysis of 1,000 construction estimates that validates inputs, checks a pricing formula, fits an additive regression and exports aggregate audit results.

## Question and findings

Do the recorded totals behave like a calculated pricing rule, and how well does an additive regression describe them?

Every source row agrees, to within one cent, with:

```text
Total = (Material cost + Labor cost) × (1 + Profit rate / 100) + Discount or markup
```

The largest floating-point discrepancy is about 1.46e-11. Negative adjustments reduce the total; positive adjustments increase it. Profit rate is interpreted in percentage points by this matching formula. Currency is not documented.

The additive regression estimates the associations between total cost and four pricing inputs. Its in-sample R² is 0.99706 and RMSE is 946.52 in unspecified monetary units. Despite the high R², the additive model omits the cost-by-profit-rate interactions present in the exact pricing formula. These are descriptive results, not evidence that a pricing policy causes changes in outcomes or that a model will predict real projects well.

## Files

- `analyze.py`: validates finite numeric inputs and full regression rank, checks the pricing formula, and fits additive OLS using NumPy least squares.
- `test_analysis.py`: synthetic-fixture tests covering a changed total, known regression coefficients, missing/nonfinite inputs, small samples, and rank deficiency.
- `results/audit.json`: aggregate output from the actual 1,000-row source CSV.
- `results/verification.txt`: executed numerical checks and validation details.

## Reproduce

Python 3.10+:

```bash
python -m pip install -r requirements.txt
python -m unittest -v
python analyze.py /path/to/construction_estimates.csv --output results/audit.json
```

Tests run without the original data. Reproducing the source-data results requires an authorised copy of the original CSV, with columns `Material_Cost`, `Labor_Cost`, `Profit_Rate`, `Discount_or_Markup`, and `Total_Estimate`. Extra columns are ignored. Use an output path outside the checked-in results when testing another dataset.

## Provenance, scope and limitations

The source is `construction_estimates.csv` and `main.R` exported from the owner's Posit project on 23 October 2026. The upstream producer, licence, currency and whether the records are synthetic are not documented. Exact formula agreement suggests mechanically calculated totals, but does not establish provenance. Raw records, policy narratives, unrelated finance files and account/session files are excluded from this repository. Only aggregate audit results are included; no redistribution permission is assumed for the dataset.

The workflow supports numerical data auditing and descriptive regression analysis. Validation covers formula agreement across all 1,000 rows, regression coefficient accuracy and three automated test cases. The Python implementation was executed successfully.

Implementation, tests and documentation were prepared with AI assistance. No claim is made that the data were independently collected or that these models have been validated for operational construction pricing.
