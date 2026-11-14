# Survey component explorer

Summarize 28 five-point survey items and explore their shared variation using standardized principal component analysis.

## Features

- Validates complete integer responses from 1 through 5.
- Reports item means, medians and sample standard deviations.
- Exports all 28 eigenvalues and explained-variance proportions.
- Provides item–component loadings for the first five components.
- Reports the component count needed to explain at least 80% of standardized variance.
- Includes synthetic data and seven automated checks.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python -m pip install -r requirements.txt
python run.py
python -m unittest -v
python run.py --input /path/to/Data1.csv --output results/custom
```

Input must contain Q1 through Q28. Additional columns are ignored. The default command uses an 80-row synthetic example and writes to `results/demo`.

## Included survey results

The supplied-file analysis covers **5,820 responses and 28 items**. The first component explains at least 80% of standardized variance; the first five together explain **90.50%**. This describes covariance structure and does not establish a validated satisfaction scale or identify causal drivers.

| Output | Contents |
| --- | --- |
| `results/items.csv` | Item-level descriptive statistics |
| `results/spectrum.csv` | Eigenvalues and cumulative explained variance |
| `results/loadings.csv` | First-five item–component correlations |
| `results/summary.json` | Response coverage and variance summary |
| `results/verification.txt` | Seven passing tests |

The original response rows are not bundled. The synthetic example demonstrates the same workflow with different results. See [METHODS.md](METHODS.md) for assumptions and interpretation.
