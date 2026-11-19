# Indicator Coverage Audit

Audit long-format indicator datasets before selecting series for analysis. This Python command-line tool measures year coverage, identifies internal gaps and flags duplicate keys and invalid values.

## Features

- Separate coverage reports for every country and indicator.
- First and last valid years, observed-year counts and internal coverage percentages.
- Explicit missing-year tables and duplicate-key counts.
- Annual counts of indicators with valid values.
- CSV and JSON exports, a synthetic example and eight automated tests.

## Run

Requires Python 3.10 or newer and no external packages. From this project directory:

```bash
python run.py examples/synthetic.csv --output output
python -m unittest -v
```

For your own dataset:

```bash
python run.py path/to/indicators.csv --output output
```

Required columns are `Country Code`, `Indicator Code`, `Year` and `Value`. See [METHODS.md](METHODS.md) for validation rules and calculation definitions.

## Historical snapshot results

| Measure | Count |
|---|---:|
| Input records | 14,319 |
| China indicator series | 782 |
| Series with internal year gaps | 309 |
| Duplicate keys | 0 |
| Rejected records | 0 |

Coverage describes the supplied snapshot, not current availability. Internal coverage uses each series' own first-to-last observed-year span; a short series can have 100% coverage. No missing values are filled.

## Outputs

- `results/series.csv`: coverage for each indicator.
- `results/gaps.csv`: missing years within observed spans.
- `results/duplicates.csv`: repeated country-indicator-year keys.
- `results/annual.csv`: indicator availability by year.
- `results/summary.json`: overall data-quality counts.
- `results/verification.txt`: test and reconciliation record.

The example data are fictional. Published historical outputs contain coverage metadata rather than source indicator values.
