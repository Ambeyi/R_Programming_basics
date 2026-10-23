# Construction Estimate Formula and Regression Audit

An analysis of 1,000 construction estimates from Derrick Achanga's existing Posit **Finc3017** project. The project name is finance-related, but its `main.R` analyses construction costs. This standalone portfolio project follows that actual code and data rather than the folder title.

## Question and findings

Do the recorded totals behave like a calculated pricing rule, and how well does the original additive regression describe them?

Every source row agrees, to within one cent, with:

```text
Total = (Material cost + Labor cost) × (1 + Profit rate / 100) + Discount or markup
```

The largest floating-point discrepancy is about 1.46e-11. Negative adjustments reduce the total; positive adjustments increase it. Profit rate is interpreted in percentage points by this matching formula. Currency is not documented.

The additive regression reproduces all five archived R coefficient estimates. Its in-sample R² is 0.99706 and RMSE is 946.52 in unspecified monetary units. Despite the high R², the additive model omits the cost-by-profit-rate interactions present in the exact pricing formula. These are descriptive results, not evidence that a pricing policy causes changes in outcomes or that a model will predict real projects well.

## Files

- `analyze.py`: validates finite numeric inputs and full regression rank, checks the pricing formula, and fits additive OLS using NumPy least squares.
- `test_analysis.py`: synthetic-fixture tests covering a changed total, known regression coefficients, missing/nonfinite inputs, small samples, and rank deficiency.
- `results/audit.json`: aggregate output from the actual 1,000-row source CSV.
- `results/verification.txt`: executed checks and comparison with the archived R output.

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

The original R script includes plots, a policy ANOVA and a proposed causal diagram. The diagram section contains an accidentally embedded URL that makes it invalid R. This release does not publish unsupported causal claims, p-values, the policy analysis or a purported validated DAG. It concentrates on the reproducible numerical audit. The original R script was not rerun; the archived coefficient output was compared numerically with the executed Python implementation.

The Python adaptation, organisation, tests and documentation were prepared with AI assistance from the owner's existing analysis. No claim is made that the data were independently collected or that these models have been validated for operational construction pricing.
