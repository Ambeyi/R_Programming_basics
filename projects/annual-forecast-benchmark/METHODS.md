# Evaluation methods

Each test year is forecast using all earlier observations, starting with four training years by default. Last-value forecasts repeat the latest observation. Drift extrapolates the average annual change between the first and latest training observations. Linear trend fits ordinary least squares to year position and extrapolates one step.

Errors are prediction minus actual. MAE is mean absolute error; RMSE is the square root of mean squared error; mean error indicates signed bias. All are in the input count units. Models are sorted by MAE, with alphabetical tie breaking. Predictions are not clipped or rounded.

The historical example has eight annual observations and four one-step test years, 2011–2014. It demonstrates evaluation mechanics; it is too small to establish general forecasting superiority. Selecting the lowest-MAE method uses these test results and requires new data for independent validation. No future forecast, seasonal model or uncertainty interval is produced.

Input requires consecutive unique annual years and nonnegative finite counts. Commas in count strings are removed. Extra columns are ignored. Synthetic example results and historical results use separate output directories.
