# Latin-square experiment

A reproducible Python experiment that compares four simulated shoe conditions while accounting for athlete and trial differences.

## Features

- Generates a balanced 4 × 4 Latin square with configurable random seed and noise.
- Validates factor assignments and numeric outcomes.
- Fits an additive categorical model using least squares.
- Exports ANOVA tests, reference-level coefficients and model diagnostics.
- Includes a runnable simulated dataset and seven automated tests.

## Run

From this project directory, using Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
python run.py
python -m unittest -v
```

To analyze the included example or another compatible dataset:

```bash
python run.py --input examples/simulated_trials.csv --output results/example
python run.py --seed 42 --noise-sd 2 --output results/seed42
```

Input columns are `athlete`, `trial`, `shoe` (integer levels 1–4) and `time` (finite numeric values). Every athlete–trial, athlete–shoe and trial–shoe pairing must occur exactly once.

## Included simulated results

The seed-123 run contains 16 observations and six residual degrees of freedom. The shoe effect has F(3, 6) = 12.2693 and p = 0.00570. Residual mean square is 2.18323. The simulation deliberately includes shoe differences; these results illustrate the analysis and do not measure real-world footwear performance.

| File | Contents |
| --- | --- |
| `results/anova.csv` | Partial F tests for the three factors |
| `results/coefficients.csv` | Intercept and level contrasts |
| `results/summary.json` | Sample size, error variation and simulation settings |
| `results/verification.txt` | Seven passing automated checks |

See [METHODS.md](METHODS.md) for the generating process, statistical assumptions and interpretation.
