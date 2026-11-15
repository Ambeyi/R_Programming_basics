# Fish co-occurrence explorer

Explore species prevalence, site richness and pairwise overlap in binary fish observation data.

## Features

- Validates binary presence/absence values and unique site identifiers.
- Calculates species prevalence and counts of disjoint species partners.
- Summarizes the distribution of species richness across sites.
- Computes species-level Jaccard distances and exports the 20 closest pairs.
- Explicitly marks pairs of entirely absent species as undefined.
- Includes a synthetic example and seven automated tests.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python -m pip install -r requirements.txt
python run.py
python -m unittest -v
python run.py --input /path/to/fish.csv --output results/custom
```

Input contains a `Location` column and at least two species columns with 0/1 observations. The default uses the included synthetic four-site example and writes to `results/demo`.

## Included results

The supplied fish dataset contains **467 sites and 72 species**, yielding **2,556 species pairs**. Of these, **264 pairs share no observed sites**. Mean site richness is **16.82 species**. No sites are empty and no species are entirely absent.

| Output | Contents |
| --- | --- |
| `results/prevalence.csv` | Species prevalence and disjoint partner counts |
| `results/richness.csv` | Number of sites at each richness level |
| `results/closest_pairs.csv` | Twenty smallest Jaccard distances |
| `results/summary.json` | Dataset coverage and pair counts |
| `results/verification.txt` | Automated tests and independent reconciliation |

Shared observations describe co-occurrence, not ecological interaction or causation. Original site-level observations are not bundled. See [METHODS.md](METHODS.md) for definitions and limitations.
