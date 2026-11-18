# Product Preference Explorer

Explore product importance ratings with a dependency-free Python reporting tool. It ranks seven product attributes and exports aggregate summaries suitable for product research and descriptive analysis.

## Features

- Attribute means, medians and complete rating distributions.
- Missing and invalid response counts without imputation.
- Top-choice percentages that explicitly include ties.
- CSV and JSON reports, synthetic example data and seven automated tests.

## Quick start

Requires Python 3.10 or newer. From this project directory:

```bash
python run.py examples/synthetic.csv --output output
python -m unittest -v
```

To analyze your own data:

```bash
python run.py path/to/ratings.csv --output output
```

See [input schema](DATA_DICTIONARY.md) for the seven required columns and [methods](METHODS.md) for calculation details.

## Survey results

The committed reports summarize 105 complete responses with no missing or invalid importance ratings.

| Attribute | Mean rating (1–7) |
|---|---:|
| Nutrition | 5.495 |
| Brand | 5.352 |
| Taste | 5.019 |
| Format | 4.638 |
| Convenience | 4.552 |
| Price | 4.457 |
| Sport specificity | 3.886 |

Nutrition and taste each appear among the highest-rated attributes for 47 respondents. There are 59 responses with tied top ratings, so top-choice percentages can total more than 100%. These are descriptive sample results, not estimates of purchase likelihood.

## Files

`preferences.py` performs the calculations; `run.py` exports reports; `test_preferences.py` covers validation, ties and known results. `examples/synthetic.csv` is a small fictional demonstration. `results/` contains aggregate survey summaries and verification details; respondent-level source data are not included.
