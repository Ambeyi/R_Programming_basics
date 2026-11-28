# Join Cardinality Audit

Inspect CSV key relationships before combining tables. This tool predicts the number of rows in an equality left join, identifies duplicate and missing keys, and reports unmatched rows without generating a potentially large joined table.

## Features

- Single or composite keys using exact string matching.
- Counts of distinct keys, duplicate keys and missing-key rows on each side.
- Matching and unmatched row counts.
- Projected left-join size, additional rows and expansion factor.
- Relationship classification across matched keys and a count of keys duplicated on both sides.
- Aggregate JSON output with no key identifiers or input payloads.

## Run

Python 3.10+; standard library only. From this directory:

```bash
python run.py examples/left.csv examples/right.csv --keys id period --output results/audit.json
python -m unittest -v
```

Supply CSV files with unique headers and identical key column names. CSV row widths must match their headers. The output file is replaced if it exists. Keep confidential input files outside the repository.

## Synthetic example

The examples are fictional tables with six rows each. Two matching key combinations account for three left rows. The projected left join has **8 rows**, adding **2 rows** (an expansion factor of **1.3333**). One key is duplicated on both sides. Three left rows and three right rows have no match, including missing keys. See [results/audit.json](results/audit.json).

## Matching rules and methods

All CSV values remain strings: leading zeros, case and surrounding whitespace are preserved for nonblank keys. A key with any blank, whitespace-only or null component never matches, even another missing key. Empty strings are missing; the literal text `NA` is an ordinary key. This is an explicit policy; database and dataframe defaults may differ.

For each nonmissing left key k, projected rows are left_count(k) × max(right_count(k), 1). Add one output row per missing-key left row. The expansion factor is projected rows divided by left rows; it is JSON null when the left input is empty. Additional rows are projected rows minus left rows. No actual merge is performed.

Duplicate-key counts count distinct key combinations occurring more than once, not all duplicate records. Unmatched-right counts include all occurrences of right keys absent from the left and all missing-key right rows. Relationship classification considers only matching keys: one-to-one, one-to-many, many-to-one or many-to-many according to uniqueness on each side. Both sides may have duplicates on different keys, so the overall many-to-many classification does not necessarily imply a key duplicated on both sides; `many_to_many_keys` reports that separately. With no matching keys the classification is `no_matches`.

The audit detects structural join risks, not whether a match is substantively correct. It does not infer key columns, normalise values, deduplicate records or resolve conflicts. Runtime is linear in input size for fixed-width keys; the CLI retains input rows in memory.

## Files and checks

| File | Purpose |
|---|---|
| audit.py | Key counts and cardinality calculations |
| run.py | CSV validation and JSON command-line output |
| test_audit.py | Eight tests for expansion, missingness, exact matching and edge cases |
| examples/ | Synthetic left and right inputs |
| results/audit.json | Reproducible aggregate output |

The example row count is also checked against an independently materialised nested-loop left join.
