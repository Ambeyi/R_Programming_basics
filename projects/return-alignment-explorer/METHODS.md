# Methods

Input columns are `Date` (ISO YYYY-MM-DD) and `Close` (positive finite number). Other columns are ignored. Invalid dates and prices are counted and excluded; duplicate parseable dates fail validation, including rows with invalid prices.

The common valid dates are sorted before calculating log(P_end) - log(P_start). Both series therefore use identical start and end dates. Missing observations can lengthen an interval; `interval_lengths.csv` exposes those gaps. At least three common dates are required.

Statistics include the arithmetic mean of interval log returns, sample standard deviation (n−1 denominator), negative-return counts and Pearson correlation. Correlation is null if either series has zero variance. Statistics are not annualised and unequal-duration intervals are not normalised by length. Close is used directly, without dividends, currency conversion or transaction costs.

Results describe the supplied series, labelled left and right because the files do not identify instruments. No forecasting, copula fitting, causal inference or investment recommendation is performed. Example CSVs are synthetic. Published source results contain aggregates only.
