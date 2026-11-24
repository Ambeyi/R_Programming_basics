# Dated Alias Resolver

Map historical names to canonical labels using date-specific rules. Suitable for cleaning changing organisation, team or product names when an explicit mapping table is available.

## Features

- Inclusive validity periods and exact name matching.
- Explicit matched, ambiguous and unmatched outcomes.
- Distinct-candidate counting for overlapping rules.
- CSV results and JSON status totals.
- Synthetic examples and eight automated tests.

## Run

Requires Python 3.10 or newer; no external packages are needed. From this directory:

```bash
python run.py examples/mappings.csv examples/events.csv --output output
python -m unittest -v
```

The demonstration has four mapping rules and eight events: four matched, one ambiguous and three unmatched. All bundled data and results are fictional. No historical accuracy is implied.

See [schemas](DATA_DICTIONARY.md) and [resolution rules](METHODS.md). `resolver.py` contains the lookup logic; `run.py` generates reports. `results/` contains reproducible example outputs. Eight tests cover boundaries, overlap, duplicate targets, case, invalid dates and intervals, and whitespace.
