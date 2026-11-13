# Methods

This project develops the regression exercise in `R exam.R`. Included model results use the 26 rows of `Study.csv`. A separate six-row invented example is bundled to demonstrate the workflow; it does not reproduce the supplied-file results. Individual source observations are not bundled.

The least-squares slope is the sum of cross-products of centered hours and scores divided by the sum of squared centered hours. The intercept is mean score minus slope times mean hours. Residual variance uses n−2 degrees of freedom. R² is one minus residual sum of squares divided by total sum of squares; it is undefined for a constant outcome.

At a requested predictor value x, leverage is 1/n + (x−mean hours)²/Sxx. The mean confidence interval uses residual standard deviation times the square root of leverage. The individual prediction interval uses the square root of one plus leverage. Both use a two-sided 95% t critical value with n−2 degrees of freedom.

Intervals assume an appropriate linear conditional mean, independent normal errors and constant error variance. They are pointwise, not simultaneous. Predictions are not clipped to a score range, and inputs outside the observed predictor range are flagged. The model does not account for prior ability, course difficulty or other confounding factors.

Leave-one-out evaluation removes each row, fits only the remaining observations and predicts the removed score. RMSE is the square root of mean squared held-out error; MAE is mean absolute held-out error. This assesses row-level predictive performance, not performance on a separate external population. Duplicate source rows are retained because there is no identifier establishing that they are accidental duplicates; dependencies between rows would weaken the validation interpretation.

Tests cover a known line, interval-width ordering, independently calculated matrix least squares, exact-line held-out predictions, extrapolation flags, invalid inputs and constant outcomes. A fold with a constant predictor is rejected rather than silently assigned a model.
