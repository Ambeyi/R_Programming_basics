# Data dictionary

Input CSV requires `scenario` (nonblank label), `year` (nonnegative elapsed years) and `amount` (signed cash flow). Extra columns are ignored.

`flows.csv` contains scenario, year, original amount, decimal rate and discounted present value. `totals.csv` contains one present-value sum per scenario and rate. Outputs retain full floating-point precision; display rounding does not affect calculations.
