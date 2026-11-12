# Methods

The project develops the grouped-count exploration in `assignment2.R`. The included aggregate results were calculated from `assignment2_prob2.txt`. The original grouped input is not bundled; the repository includes a synthetic three-cell example with the same schema.

The ratio for a group is sum(nChildren) / sum(nMother). This is a weighted mean of cell-level ratios using nMother as the weight. For example, cells with one mother and four children and nine mothers and nine children yield 13 / 10 = 1.3, rather than the unweighted average of 4 and 1. No percentage interpretation is appropriate because children per mother can exceed one.

Duration categories are 0-4, 5-9, 10-14, 15-19, 20-24 and 25-29. Residence labels are Suva, urban and rural. Education labels are none, lower, upper and sec+. These are retained as supplied; duration is not relabelled as maternal age. Their Cartesian product defines 72 possible combinations.

The observed file has 70 cells. The missing combinations are duration 25-29 with education sec+ for urban and rural residence. The coverage report records absence without imputing counts. A category with no observations is omitted from its summary. Unequal category coverage can affect comparisons.

Counts must be finite nonnegative integers, and each observed cell must contain at least one mother. Zero children is permitted. Missing fields, unknown categories and duplicate combinations are rejected. No data are silently dropped. Every marginal summary reconciles to the same observed totals.

No Poisson or negative-binomial regression is fitted. The output does not adjust for confounding, survey design or differences in duration composition. It describes the supplied cells and should not be interpreted as a population fertility estimate or an effect of education or residence.

Tests check a known weighted result, conserved totals, coverage, invalid input, zero child counts and input preservation. A separate standard-library CSV calculation independently reconciles source totals with the published summary.
