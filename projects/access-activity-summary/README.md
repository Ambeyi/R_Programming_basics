# Access Activity Summary

Summarise product-access events by day, hour and category. This Python command-line tool exports aggregate activity counts and input-quality totals without retaining IP addresses or URLs.

## Features

- Daily event totals and a complete 24-hour activity profile.
- Ranked category counts with whitespace and case normalisation.
- Invalid-date and missing-category accounting.
- CSV and JSON exports, synthetic example and seven automated tests.

## Run

Requires Python 3.10 or newer; no external packages are needed. From this directory:

```bash
python run.py examples/synthetic.csv --output output
python -m unittest -v
```

For your own CSV:

```bash
python run.py path/to/access.csv --output output
```

Input needs `Date` and `Category` columns. Date format is month/day/year hour:minute, for example `9/1/2017 6:00`. Additional fields are ignored.

## Synthetic demonstration

All bundled results are generated from the fictional example CSV. Five input rows produce four accepted events across two dates, one invalid timestamp and one missing category. The three aggregate tables each total four events.

Counts represent events, not unique visitors or purchases. Timezone is unspecified. The tool does not filter bots or deduplicate events. See [METHODS.md](METHODS.md) for calculation rules.

## Outputs and validation

`results/daily.csv`, `results/hourly.csv` and `results/categories.csv` contain demonstration reports. `results/summary.json` records input totals and time span. All seven tests passed; see [verification](results/verification.txt).
