# Grouped count explorer

Summarize children and mother counts across duration, residence and education categories using denominator-weighted ratios.

## Features

- Validates integer counts, category labels and unique category combinations.
- Computes pooled children-per-mother ratios from summed counts.
- Exports separate duration, residence, education and duration-by-residence summaries.
- Audits coverage of the 72 possible category combinations.
- Includes a synthetic runnable example and seven automated tests.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python -m pip install -r requirements.txt
python run.py
python -m unittest -v
python run.py --input /path/to/counts.csv --output results/custom
```

The input CSV must contain `duration,residence,education,nMother,nChildren`. The default uses `examples/synthetic.csv` and writes to `results/demo`; this example is distinct from the supplied-file results below.

## Included results

The supplied grouped-count file contains **70 observed cells**, **2,677 mothers** and **10,602 children**, giving a pooled ratio of **3.9604 children per mother**. Two of the 72 category combinations are absent. Missing combinations remain absent rather than being assigned zero counts.

| Output | Contents |
| --- | --- |
| `results/duration.csv` | Duration summaries in category order |
| `results/residence.csv` | Residence summaries |
| `results/education.csv` | Education summaries |
| `results/duration_residence.csv` | Joint duration and residence summaries |
| `results/missing_cells.csv` | Absent combinations |
| `results/summary.json` | Overall counts and ratio |
| `results/verification.txt` | Tests and independent count reconciliation |

These are descriptive summaries of supplied grouped data, not estimates of causal effects. See [METHODS.md](METHODS.md) for weighting, coverage and interpretation.
