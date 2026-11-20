# Data dictionary

| Field | Meaning |
|---|---|
| Year | Integer calendar year; sorted before evaluation |
| Birth Number | Nonnegative annual count; quoted comma-separated thousands accepted |

`folds.csv` records test year, training size, model, actual count, prediction and signed error. `metrics.csv` records number of test folds, MAE, RMSE and mean error per model. `summary.json` records input range, training size, test count and lowest-MAE model.

The historical source is the supplied US annual births file for 2007–2014. Published outputs describe that snapshot. The example CSV is fictional and is not US demographic data.
