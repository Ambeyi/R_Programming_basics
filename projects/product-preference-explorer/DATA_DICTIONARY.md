# Input schema

CSV header must include all seven fields. Each accepts an integer from 1 to 7; blank values are allowed. Extra columns are ignored.

| Field | Product attribute |
|---|---|
| imp_price | Price |
| imp_brand | Brand |
| imp_format | Format |
| imp_taste | Taste |
| imp_nutrition | Nutrition |
| imp_convenience | Convenience |
| imp_sportspecific | Sport specificity |

Outputs: `attributes.csv` contains valid/missing/invalid counts, means, medians and top-choice statistics; `distribution.csv` contains counts for every attribute and rating; `audit.json` contains response, completeness and tied-top counts.
