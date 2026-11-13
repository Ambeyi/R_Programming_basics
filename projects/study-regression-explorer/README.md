# Study regression explorer

Explore the association between study hours and exam scores using simple linear regression, correlation and held-out prediction evaluation.

## Features

- Fits an intercept and slope with least squares.
- Reports Pearson correlation and R².
- Distinguishes confidence intervals for the mean from individual prediction intervals.
- Flags predictions outside the observed study-hour range.
- Refits the model for every leave-one-out prediction and reports RMSE and MAE.
- Includes a synthetic example and seven automated tests.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python -m pip install -r requirements.txt
python run.py
python -m unittest -v
python run.py --input /path/to/Study.csv --output results/custom --hours 7 15
```

Input columns are `hours_studied` and `exam_score`. Use at least five paired finite observations with sufficient predictor variation for every validation fold. The default command uses the synthetic example and writes to `results/demo`.

## Included supplied-file results

The 26-observation exercise dataset covers 2–28 study hours. The fitted equation is **score = 28.8449 + 1.86577 × hours**. Pearson r is **0.72168**, and R² is **0.52082**. Leave-one-out RMSE is **14.67379 score units**, with MAE **11.65969**.

These results describe an association in the supplied exercise data. They do not establish that an additional study hour causes a particular score increase.

| Output | Contents |
| --- | --- |
| `results/model.json` | Coefficients, fit statistics and observed range |
| `results/predictions.csv` | Predictions, two interval types and extrapolation flags |
| `results/validation.json` | Held-out error metrics |
| `results/verification.txt` | Seven passing tests |

See [METHODS.md](METHODS.md) for assumptions and interpretation.
