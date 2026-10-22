# ESG and Systemic Risk Exploration

A distinct portfolio project adapted from Derrick Achanga's Posit Cloud **ESG impact** project. It audits a firm-year panel and explores associations between ESG scores and three systemic-risk measures. The published Python pipeline was executed on the exported workbook; aggregate outputs are included.

## Findings

The workbook contains 1,210 rows for 110 entities from 2011–2021, with no duplicate entity-year keys and no missing values in the seven analyzed metrics. These checks establish internal consistency, not authenticity or accuracy of the underlying measurements.

| ESG Combined Score association | Pooled Pearson correlation |
|---|---:|
| Delta-CoVaR | 0.068729 |
| MES | −0.097842 |
| NSRISK | 0.064073 |

These small pooled correlations do not establish that ESG causes higher or lower risk. Repeated observations from the same entity are not independent. Country, time and entity differences may confound the associations. Sign conventions and units of the risk measures were not verified, so neither positive nor negative coefficients are interpreted as a risk improvement.

## Reproduce

Python with pandas, numpy and openpyxl is required. Install dependencies from `requirements.txt`, then run:

```sh
python analyze.py /path/to/ESG_Data.xlsx
```

Use `--output /path/to/output` to select a different destination. Existing generated files at that destination are overwritten. No network calls occur during analysis. Input checks reject missing identifiers, duplicate panel keys, noninteger years, infinite values and nonnumeric metrics. Missing metric values are reported; correlations use available pairs with at least three observations, and pair counts are exported.

## Results directory

- `audit.json`: panel dimensions and missingness.
- `descriptive_statistics.csv`: counts, mean, standard deviation and quantiles.
- `pearson_correlations.csv`: exploratory pooled correlations.
- `correlation_pair_counts.csv`: sample size behind each correlation.
- `annual_means.csv` and `annual_counts.csv`: yearly means and nonmissing counts.
- `verification.txt`: executed checks and limits.

## Data access and provenance

The source is `ESG_Data.xlsx` in Posit project 6461967. The original data vendor, collection methods, measurement definitions and redistribution rights were not documented in the reviewed export. The workbook, entity identifiers and original reports are therefore excluded. Reproduction of the committed results requires lawful access to that workbook; the repository does not include a substitute dataset or claim independently verified market evidence.

## Review decisions

The original R script mixed inconsistent column naming, contained an extra comma in its IV call, and labelled the same panel LM-test call as two different diagnostics. Its GMM section was commented out. This release deliberately limits its claims to executed data auditing and descriptive analysis; none of the original regression, IV, GMM or diagnostic results is presented as validated. This is a new Python adaptation, not a claim that the complete R analysis was reproduced.

AI assistance was used to restructure the workflow, prepare documentation and verify numerical outputs. On 22 October 2026, checks passed for correlation symmetry/diagonal, an independent centered-vector calculation of the Delta-CoVaR/MES correlation, and rejection of an intentionally duplicated entity-year record. There are no causal, forecasting or investment-performance claims.
