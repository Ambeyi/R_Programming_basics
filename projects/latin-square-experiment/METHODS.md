# Design and analysis

The 4 × 4 Latin square assigns each shoe once to every athlete and once to every trial. It contains 16 observations. The model is `time ~ athlete + trial + shoe`, with categorical effects, an intercept and level 1 as the reference for each factor. Its ten parameters leave six residual degrees of freedom.

The simulation uses intercept 53; athlete effects [0, -2, 3, 4]; trial effects [0, -1, 1, 3]; and shoe effects [0, 3, 5, 1]. Independent Gaussian noise has standard deviation 1.5 by default. Values are in arbitrary time units. The cyclic allocation is fixed; the seed controls noise only. The design follows the experiment in `Race.R` from the user's Posit project.

Least squares estimates the additive model. For each factor, a reduced model excludes that factor. The difference in residual sums of squares, divided by three and by the full model's residual mean square, gives the partial F statistic with (3, 6) degrees of freedom. Reported p-values are unadjusted across the three tests.

Inference assumes independent, normally distributed errors with constant variance and additive effects. Interactions cannot be separately estimated in this unreplicated square. These are simulated observations, not evidence that a commercial shoe improves performance. A real experiment would need a randomized allocation and attention to carryover and repeated-measure dependence.

Validation checks complete numeric outcomes, finite values, all four factor levels, 16 rows and unique pairings for every pair of factors. Near-zero residual variance is rejected because F inference is not meaningful. Tests independently verify factor sums of squares using balanced-design group means and recover the known coefficients from noiseless observations.
