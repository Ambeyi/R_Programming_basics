# Methods

Input CSV needs `group` and `y` columns. Group labels are trimmed; numeric scores must be finite. Missing fields, blank labels, invalid scores and empty inputs fail validation. Additional columns, including identifiers, are ignored. Duplicate observations are retained because no unique-key contract is assumed.

For each group the tool reports count, arithmetic mean, median, sample standard deviation (n−1 denominator), minimum and maximum. Standard deviation is blank for singleton groups. Pairwise differences follow alphabetical group order and subtract the second group's mean from the first.

These summaries are descriptive. Group labels are retained as supplied: no treatment meaning, causal effect, population inference or statistical significance is assumed. The historical output uses 300 supplied score observations in three groups; source records are not bundled. The included example is synthetic.

Validation: six unit tests cover known statistics, difference direction, singleton groups, invalid values, missing schema and ordering. Independent pandas calculations reconcile historical group counts, means, medians and sample standard deviations.
