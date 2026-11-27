# Data dictionary

## Input CSV

One row per response and one numeric column per item. The example has three fictional items (`a`, `b`, `c`) on a 1–5 range; `c` is reverse scored. Empty cells represent missing responses. Additional columns are ignored unless selected by a scale. Headers must be unique. No respondent identifiers are needed.

## Scale JSON

A nonempty array of objects with unique `name` values. Each object requires `items` (at least two unique column names), `minimum` and `maximum` (shared finite bounds). Optional `reverse` lists item names to reverse. Bounds apply to every selected item in that scale.

## scales.csv

| Field | Meaning |
|---|---|
| scale | Configured scale name |
| input_rows | All input response rows |
| complete_rows | Rows with every scale item observed |
| excluded_rows | Input rows minus complete rows |
| items | Number of selected items |
| alpha | Raw Cronbach alpha; blank if undefined |
| mean_score | Average of complete respondents' mean item scores |

## items.csv

| Field | Meaning |
|---|---|
| scale / item | Scale and item labels |
| reversed | Whether explicit reverse scoring was applied |
| mean / sd | Item mean and sample SD after scoring |
| corrected_item_total | Correlation with the sum of all other items |
| alpha_if_deleted | Alpha of remaining items using the full-scale complete cases |

Blank statistics mean undefined, not zero. Output files contain aggregate statistics only. Running the CLI replaces files of the same names in the chosen output directory.
