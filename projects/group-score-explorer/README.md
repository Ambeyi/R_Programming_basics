# Group Score Explorer

Summarise numeric scores by group and compare group means with a lightweight Python command-line tool.

## Features

- Counts, means, medians, sample standard deviations and ranges.
- Pairwise mean differences with explicit subtraction direction.
- Input validation and deterministic group ordering.
- CSV reports, a synthetic example and six automated tests.

## Run

Requires Python 3.10 or newer; no external packages are needed. From this directory:

```bash
python analyze.py examples/synthetic.csv --output output
python -m unittest -v
```

For your own CSV, supply `group` and `y` columns:

```bash
python analyze.py path/to/scores.csv --output output
```

## Supplied score results

| Group | Observations | Mean | Median | Sample SD |
|---|---:|---:|---:|---:|
| group-1 | 100 | 9.38 | 10 | 3.584 |
| group-2 | 100 | 10.32 | 10 | 3.228 |
| group-3 | 100 | 22.67 | 23 | 2.767 |

Results describe 300 observations. Group meanings and score units are unspecified, so these differences are not interpreted as treatment effects or statistical significance.

`results/groups.csv` contains group summaries; `results/differences.csv` contains pairwise mean differences. The example data are fictional. See [METHODS.md](METHODS.md) for validation rules and calculations.

All six tests passed. Independent pandas calculations matched group counts, means, medians and sample standard deviations to tolerance 1e-12 on 21 November 2026.
