# Mailing split audit

Create reproducible stratified train, validation and test partitions and audit their class balance, coverage and overlap.

## Features

- Splits binary-labelled records without replacement using a configurable seed.
- Allocates approximately 70% to training, 15% to validation and the remainder to testing within each class.
- Verifies that each source-row position is assigned once.
- Reports feature-pattern overlap separately from row-position overlap.
- Reports missing features without imputing them.
- Exports aggregate reports and includes a synthetic example and seven tests.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python -m pip install -r requirements.txt
python run.py
python -m unittest -v
python run.py --input /path/to/mailing.csv --output results/custom --seed 43
```

Input requires a binary `class` column and at least ten rows of each class. Other columns are treated as features. The default command uses the synthetic example and writes to `results/demo`. Source-row indices are available through the `partition` function; the CLI exports only aggregate reports.

## Included mailing-data results

The audit covers **191,779 records**, including **9,716 class-1 records**. Every row is assigned exactly once, and no row position appears in two partitions.

There are **21,937 duplicate feature rows** beyond first occurrences. The split has shared feature hashes across partitions: **1,394** train/validation, **1,441** train/test and **704** validation/test. These are distinct shared patterns, not counts of shared people. This audit therefore does not certify that the split is free of entity or duplicate-pattern leakage.

| Output | Contents |
| --- | --- |
| `results/partitions.csv` | Partition sizes and class proportions |
| `results/overlap.csv` | Row-position and feature-pattern overlap |
| `results/missingness.csv` | Missing-value counts by column |
| `results/summary.json` | Coverage, class counts and duplicate count |
| `results/verification.txt` | Seven passing tests |

See [METHODS.md](METHODS.md) for rounding rules and interpretation.
