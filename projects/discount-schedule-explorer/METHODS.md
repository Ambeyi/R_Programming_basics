# Calculation rules

Present value equals amount / (1 + rate)^year. Rate is an effective annual decimal rate, so 0.05 means 5%. Year measures elapsed years from a shared time origin; zero is immediate and fractions are supported. Positive amounts represent inflows and negative amounts represent outflows. All cash flows must use consistent currency units and price basis.

Rows are discounted individually and summed by scenario. Repeated scenario/year rows remain separate additive cash flows. Rates may be negative but must exceed −1. Years must be finite and nonnegative; amounts and rates must be finite. Overflow raises an error. Extremely small discounted values may underflow to zero at floating-point precision.

The calculator performs arithmetic sensitivity analysis only. It does not choose an appropriate rate, infer inflation, assess risk or recommend an investment. All bundled inputs and results are synthetic.
