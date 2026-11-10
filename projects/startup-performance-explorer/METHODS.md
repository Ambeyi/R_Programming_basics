# Methods and interpretation

The workflow follows the descriptive-analysis theme in `DPBS analysis.R`. Published aggregate results use the 1,539-row `DPBS.xlsx` assessment workbook. The bundled three-row CSV is synthetic and exercises the same code; its output differs from the workbook results.

Required columns are City, StartYear, IsSuccessful, Equipment, Website, Payroll, Office Furniture and Supplies, Professional Consultants, Profit and Sales. Missing or nonfinite required values are rejected. Success labels must be 0 or 1. Founding years must be integer values between 1800 and 2200. Expenditure and sales must be nonnegative; profit may be negative. City whitespace is trimmed. No duplicate records are silently removed because the schema does not provide a unique business identifier.

Group summaries report record counts, sums of success labels, success rates, mean and median profit, total profit and total sales. Success rate uses all records in the group as its denominator. This summarizes the supplied label; it does not define or validate business success.

Pearson correlations compare each spending or sales variable with profit over all input records. A constant variable or a sample with fewer than two rows yields a blank coefficient with an explicit status. Correlations are descriptive, sensitive to outliers and do not establish causal effects or predictive accuracy.

StartYear identifies a founding cohort. Cohort summaries are cross-sectional comparisons, not repeated annual profit measurements or a profit time series. Monetary values retain the source workbook's units; no currency conversion or inflation adjustment is performed. These assessment-file summaries should not be generalized to the wider startup population.

Tests cover known group means and rates, conservation of group totals, perfect correlation, undefined correlation, negative profit, invalid fields and preservation of input data. A separate source-workbook check reconciles record count, success totals and profit totals using openpyxl and Python arithmetic.
