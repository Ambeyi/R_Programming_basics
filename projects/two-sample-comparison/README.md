# Two sample comparison

Compare independent numeric samples with descriptive statistics, three statistical tests and interpretable effect sizes.

## Features

- Strict CSV input validation and support for unequal group sizes.
- Welch's t-test and a 95% confidence interval for the mean difference.
- Mann–Whitney U with tie-aware probability of superiority.
- Kolmogorov–Smirnov distribution comparison.
- CSV and JSON exports and six automated tests.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python -m pip install -r requirements.txt
python run.py
python -m unittest -v
python run.py --input examples/synthetic.csv --output results/example
```

For your own data, supply a CSV with columns `group,value`, group labels `A` or `B`, and at least two finite observations with positive variance in each group.

## Synthetic example

The included invented dataset contains 12 observations in A and 11 in B, in arbitrary units. The mean difference A minus B is **6.4167**, with a 95% Welch interval of **2.7462 to 10.0872**. The tie-adjusted probability of superiority for A is **0.85985**.

These results demonstrate the workflow; they are not findings about a real population. See [METHODS.md](METHODS.md) for test assumptions, the interpretation of ties and limitations of multiple comparisons.

| Output | Contents |
| --- | --- |
| `results/group_summary.csv` | Group sizes, means, medians and sample standard deviations |
| `results/tests.csv` | Test statistics and unadjusted two-sided p-values |
| `results/effects.json` | Mean difference, interval, degrees of freedom and superiority effect |
| `results/verification.txt` | Six passing automated checks |
