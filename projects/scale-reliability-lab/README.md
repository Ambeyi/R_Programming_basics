# Scale Reliability Lab

A reproducible Python workflow for checking internal consistency in multi-item surveys. Configure item groups and scoring rules, then produce scale summaries and item diagnostics from a CSV.

## Features

- Explicit reverse scoring with configurable response bounds.
- Complete-case analysis separately for each scale, with exclusion counts.
- Raw Cronbach's alpha and mean scale scores.
- Item means, sample standard deviations, corrected item–total correlations and alpha if deleted.
- Validation of missing columns, duplicate headers, invalid numbers and out-of-range responses.
- Reproducible synthetic example and automated checks.

## Run

Requires Python 3.10 or later. No package installation is needed. From this project directory:

```bash
python run.py examples/responses.csv examples/scales.json --output results
python -m unittest -v
```

For your own data, supply a CSV and a JSON scale specification following the examples. Output files in the chosen directory are replaced on each run. Keep private input data outside the repository.

## Example results

The included synthetic example contains 12 responses and three items, with item `c` reverse scored. Ten complete responses contribute to the analysis; two are excluded. Cronbach's alpha is **0.9606**, and the mean scale score is **3.0667** on the 1–5 range.

See [scale results](results/scales.csv) and [item diagnostics](results/items.csv). These figures demonstrate the software on fictional responses; they are not survey findings. Alpha is a descriptive measure of internal consistency and does not establish validity or unidimensionality.

## Project files

| File | Purpose |
|---|---|
| reliability.py | Scoring, validation and statistical functions |
| run.py | CSV/JSON command-line workflow |
| test_reliability.py | Nine checks covering scoring and edge cases |
| examples/ | Synthetic responses and scale configuration |
| results/ | Reproducible example outputs |
| [METHODS.md](METHODS.md) | Formulae, missing-data rules and interpretation |
| [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Input and output schemas |
