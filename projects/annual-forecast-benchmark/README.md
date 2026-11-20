# Annual Forecast Benchmark

Compare three simple annual forecasting methods through expanding-window evaluation. Every prediction uses only observations earlier than its test year.

## Features

- Last-value, drift and least-squares linear-trend baselines.
- Configurable initial training window.
- Per-year predictions and signed errors.
- MAE, RMSE and mean-error comparison.
- Input validation, synthetic example and eight automated tests.

## Run

Requires Python 3.10 or newer, with no external packages. From this directory:

```bash
python run.py examples/synthetic.csv --output output
python -m unittest -v
```

For your own annual series:

```bash
python run.py path/to/annual.csv --min-train 4 --output output
```

See [data dictionary](DATA_DICTIONARY.md) and [methods](METHODS.md).

## Historical benchmark

The supplied annual births snapshot contains eight years, 2007–2014. Four expanding-window folds predict 2011–2014.

| Model | MAE | RMSE |
|---|---:|---:|
| Last value | 30,775.00 | 37,579.65 |
| Drift | 80,413.37 | 84,772.22 |
| Linear trend | 115,921.78 | 125,929.25 |

Errors are in annual birth-count units. Last value has the lowest error in these four test years; the small sample does not establish general forecasting superiority. The project provides retrospective evaluation, not a current demographic forecast.

## Files

`forecast.py` contains validation and evaluation; `run.py` produces reports; `test_forecast.py` checks known calculations, input errors and exclusion of future observations. `results/` contains historical predictions, metrics and verification. `examples/synthetic.csv` is fictional demonstration data.
