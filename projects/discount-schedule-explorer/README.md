# Discount Schedule Explorer

Calculate present values for labelled cash-flow scenarios and compare totals across user-specified discount rates.

## Features

- Signed cash flows and fractional elapsed years.
- Configurable annual rates, including zero and valid negative rates.
- Per-flow discounted values and scenario totals.
- CSV input/output, synthetic examples and eight automated tests.

## Run

Requires Python 3.10 or newer with no external packages. From this directory:

```bash
python run.py examples/cashflows.csv --rates 0 0.03 0.05 --output output
python -m unittest -v
```

Use your own CSV with `scenario`, `year` and `amount` fields. See [data dictionary](DATA_DICTIONARY.md) and [calculation rules](METHODS.md).

## Demonstration

Two fictional scenarios contain eight cash flows in unspecified currency units. At a zero rate, Alpha totals 200 and Beta totals 250. The committed results evaluate both scenarios at 0%, 3% and 5%, producing 24 discounted-flow rows and six scenario/rate totals. These examples demonstrate arithmetic and do not represent investment recommendations.

`discount.py` provides calculations, `run.py` exports reports, and `test_discount.py` covers known values and invalid inputs. All eight tests passed. Independent Decimal calculations matched all six example totals within 1e-10.
