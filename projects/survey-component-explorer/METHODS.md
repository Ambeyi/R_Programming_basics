# Methods

The workflow develops the component-analysis theme in `exploratory.R`. Published aggregate results use Q1–Q28 from the supplied `Data1.csv`. Instructor, class and other metadata are excluded from the analysis.

Each item is centered and divided by its sample standard deviation using n−1 in the variance denominator. PCA is the eigendecomposition of the resulting 28-by-28 Pearson correlation matrix. Eigenvalues are sorted descending; negligible negative values caused by numerical rounding are clipped to zero. Explained ratios divide each eigenvalue by their sum.

Loadings are eigenvectors multiplied by the square roots of the corresponding eigenvalues. These equal item–component correlations for standardized items. For readable sign consistency, each component is oriented so its largest absolute eigenvector coefficient is positive. Signs are arbitrary; tied eigenvalues may permit different but equivalent component bases. No rotation is applied.

The first five loading columns are exported as an exploratory view, not a recommendation to retain five components. The 80% threshold is a descriptive cumulative-variance rule, not a psychometric validation criterion. Item wording is not inferred from numeric labels, and no component is assigned a substantive construct name.

Treating five-point ordinal responses as numeric is an approximation. Pearson PCA captures linear covariance, not ordinal latent structure. It does not assess causal effects, reliability, measurement invariance or out-of-sample prediction. A dominant component alone does not establish unidimensional validity.

Missing values, out-of-range ratings, fractional ratings and constant items are rejected; the workflow does not impute or silently delete observations. At least three rows are required. Repeated response patterns are retained because no unique respondent key is supplied.

Tests reconcile eigenvalues with an independent singular-value decomposition, verify total variance and explained proportions, check a rank-one example, confirm row-order invariance and exercise input validation. The synthetic example uses NumPy seed 42 and independent uniform integer draws from 1 to 5.
