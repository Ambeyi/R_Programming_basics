# Methods

Each scale selects its own complete cases. Blank cells are missing; all nonmissing values must be finite and within the inclusive configured bounds. Missingness does not suppress validation of other cells. Numeric values may be fractional. Rows are never imputed.

Items explicitly listed in `reverse` are transformed as minimum + maximum − value. Item direction is determined by the scale specification, never inferred from correlations.

Raw Cronbach's alpha is k/(k−1) × [1 − ΣVar(item)/Var(total)]. Sample variances use n−1. Alpha is undefined with fewer than two complete observations, fewer than two items, or zero total-score variance. Undefined values are blank in CSV. Negative alpha is preserved.

The corrected item–total correlation is Pearson's correlation between an item and the sum of the remaining items. Constant inputs yield a blank correlation. Alpha if deleted uses the same complete-case sample as the full scale, removing only the indicated column. A two-item scale therefore has no alpha-if-deleted statistic. Item SDs are sample standard deviations. The scale mean is the mean of each complete respondent's item mean after reverse scoring.

Alpha describes internal consistency for the supplied responses. It does not demonstrate a single latent factor, establish validity or causality, or justify deleting an item automatically. The programme does not fit CFA or SEM. Results depend on item coding, response variation, item count and missingness; assess item content alongside the statistics.

Runtime is O(nk²) for n responses and k items; input data are held in memory. Python 3.10+ is required, with no external packages. The example is synthetic and is intended to demonstrate calculations, not make claims about a population.
