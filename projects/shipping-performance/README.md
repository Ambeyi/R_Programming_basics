# Shipping Performance

Order-level analysis of actual versus scheduled shipping duration, with summaries by shipping mode.

## Features

- Collapses repeated order lines to one observation per order.
- Rejects conflicting shipping attributes within an order.
- Computes mean durations, delay distributions and over-schedule rates.
- Exports aggregate CSV tables and a JSON summary.
- Includes a fictional example and four unit tests.

## Results

The analyzed file contains 180,519 rows representing 65,752 unique orders. Of these, 37,698 have actual shipping duration greater than scheduled duration. Counts use unique orders, not order lines.

## Run

Python 3.10 or later:

```bash
python -m pip install -r requirements.txt
python analyze.py examples/demo.csv --output demo-results
python -m unittest -v
python analyze.py data/DataCoSupplyChainDataset.csv --output results
```

The demo is fictional. Source customer and order records are not bundled; only aggregate results are published. See `METHODS.md` for definitions and assumptions.
