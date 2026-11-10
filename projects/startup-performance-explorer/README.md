# Startup performance explorer

Explore startup performance by city and founding cohort, and examine associations between spending, sales and profit.

## Features

- Validates required fields, success labels, founding years and numeric values.
- Summarizes record counts, success rates, profit and sales by city and cohort.
- Calculates spending–profit and sales–profit Pearson correlations.
- Handles undefined correlations explicitly and supports negative profits.
- Accepts CSV or the assessment workbook's Excel sheet.
- Exports reusable CSV tables and a JSON summary.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python -m pip install -r requirements.txt
python run.py
python -m unittest -v
python run.py --input /path/to/DPBS.xlsx --output results/workbook
```

The default command uses the included synthetic example and writes to `results/demo`. The workbook command reads the sheet `DPBS 1190 Assessment Dataset`. The workbook itself is not included.

## Included workbook results

The aggregate analysis covers **1,539 records across three cities**, with founding years from **2005 to 2012**. Of these, **298 records have a success label of 1**, a rate of **19.36%**. Mean profit is **107,532.55 in the source units**.

| Output | Contents |
| --- | --- |
| `results/city_summary.csv` | City counts, label rates, profit and sales |
| `results/cohort_summary.csv` | Founding-year cohort summaries |
| `results/profit_correlations.csv` | Pearson coefficients and calculation status |
| `results/summary.json` | Overall record coverage and headline metrics |
| `results/verification.txt` | Tests and source-total checks |

Founding-year comparisons describe cohorts rather than changes over time within the same businesses. Correlations describe association, not causation. See [METHODS.md](METHODS.md) for input rules and interpretation.
