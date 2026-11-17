# Return Alignment Explorer

Compare two price series over identical date intervals with a dependency-free Python command-line tool.

## Features

- Validates ISO dates and positive finite closing prices.
- Reports rejected rows, common dates and dates unique to each series.
- Aligns interval boundaries before calculating log returns.
- Summarises return means, sample variability, negative intervals and correlation.
- Exports JSON statistics and an interval-length frequency table.
- Includes synthetic example data and eight automated tests.

## Run

Requires Python 3.10 or newer. From this project directory:

```bash
python run.py examples/left.csv examples/right.csv --output output
python -m unittest -v
```

For your own CSVs:

```bash
python run.py path/to/left.csv path/to/right.csv --output output
```

Each file needs `Date` and `Close` columns. Additional columns are ignored. Example data are synthetic; the committed `results/` directory describes the supplied historical files.

## Historical results

| Measure | Value |
|---|---:|
| Common valid dates | 1,200 |
| Matched return intervals | 1,199 |
| Period | 13 March 2000–13 March 2023 |
| Pearson correlation | 0.625942 |
| Left / right negative intervals | 553 / 543 |
| Interval lengths | 7–14 days |
| Left / right rejected input rows | 1 / 0 |

The series are labelled left and right. Interval statistics are not annualised; missing dates can create longer intervals. See [METHODS.md](METHODS.md) for definitions and interpretation, and [verification](results/verification.txt) for validation.

## Project files

`alignment.py` contains validation and calculations; `run.py` generates reports; `test_alignment.py` exercises edge cases. `examples/` provides a runnable demonstration, while `results/` contains aggregate historical outputs.
