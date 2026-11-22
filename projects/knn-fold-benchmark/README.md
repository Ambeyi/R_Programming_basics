# KNN Fold Benchmark

Evaluate nearest-neighbour classification using predefined cross-validation folds. The tool compares neighbour counts and exports fold-level accuracy and aggregate confusion counts.

## Features

- Euclidean distance on two numeric features.
- Supplied-fold evaluation with held-out rows excluded from training.
- Configurable neighbour counts and deterministic tie handling.
- CSV results, synthetic example and seven automated tests.

## Run

Requires Python 3.10 or newer and no external dependencies. From this directory:

```bash
python benchmark.py examples/synthetic.csv --k 1 3 --output output
python -m unittest -v
```

For a larger dataset:

```bash
python benchmark.py path/to/data.csv --k 1 3 5 --output output
```

Required fields are `x`, `y`, `myclass` and `fold`. See [METHODS.md](METHODS.md) for validation, tie rules and interpretation.

## Supplied dataset results

200 observations; five folds; 160 training and 40 held-out observations per fold.

| Neighbours | Overall held-out accuracy |
|---|---:|
| 1 | 79.0% |
| 3 | 85.0% |
| 5 | 84.0% |

These are configuration-comparison results, not an independent final test after choosing k. Features are not scaled. The synthetic example is fictional and separate from the supplied dataset.

`results/folds.csv` contains 15 fold/configuration evaluations. `results/confusion.csv` aggregates predictions across all folds. Seven tests passed, and an independent NumPy distance-matrix implementation matched all 15 correct-prediction counts on 22 November 2026.
