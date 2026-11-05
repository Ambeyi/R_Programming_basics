# Monthly Temperature Explorer

A Python workflow for exploring annual and seasonal patterns in monthly temperature observations.

## Features

- Validates year-month keys, numeric values and duplicate records.
- Flags incomplete years without filling missing months.
- Summarizes annual means and monthly extremes.
- Reports seasonal means, sample standard deviations and observation counts.
- Includes a fictional demo and four automated tests.

## Results

The supplied series contains 936 monthly observations spanning 1947–2024. All 78 years contain 12 months. Aggregate annual and seasonal tables are included in `results`.

## Run

Requires Python 3.10 or later.

```bash
python -m pip install -r requirements.txt
python analyze.py examples/demo.csv --output demo-results
python -m unittest -v
python analyze.py data/CLMTEMP_HKO_MONTHLY.csv --output results
```

The demo is fictional. The source dataset is not bundled. Input columns are `Year`, `Month` and `Value`; extra columns are ignored. See `METHODS.md` for calculation details.
