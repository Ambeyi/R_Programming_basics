# Methods

Each observation is drawn independently with replacement from an inclusive integer interval [a, b], using a local Python random generator. Each possible age has probability 1 / (b - a + 1). This project develops the synthetic age-distribution exercise in `Question 4.R` into a standalone Python workflow. Python and R random generators need not produce identical observations from the same seed.

Bands begin at the lower bound and contain up to `width` integer ages. Endpoints are inclusive and every age belongs to exactly one band. An incomplete final band retains its actual width. Its expected count is sample size multiplied by its number of possible ages divided by (b - a + 1).

The mean and median summarize the generated observations. Population standard deviation divides the squared-deviation total by N because it describes the complete generated sample. The theoretical mean is (a + b) / 2. Outputs are descriptive; no hypothesis test or causal conclusion is implied.

Validation requires a positive integer sample size, integer seed, integer age limits between 0 and 120, and a positive integer band width. All analyzed ages must fall within the declared interval. Zero-count ages and bands remain in exported tables.

The chart displays counts, not density. With unequal band widths, counts should be interpreted alongside the expected-count column. A lower final-band count alone does not show a departure from uniform sampling.

The test suite checks a hand-calculated five-observation example, inclusive endpoint behavior, deterministic sampling, invalid values, conservation of counts, unequal-width expectations and SVG XML structure.
