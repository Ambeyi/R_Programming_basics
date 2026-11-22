# Methods

The CSV requires finite numeric `x` and `y`, a nonblank `myclass` and a nonblank `fold`. Labels and fold names are strings. Each supplied fold is held out in turn; all other folds form training data. No scaling, imputation, resampling or feature selection is performed.

Prediction uses Euclidean distance on the original feature scales. Equal distances retain input row order, and tied class votes use lexical class order. The neighbour count must be positive and no larger than the training set. Accuracy is correct predictions divided by held-out observations. Confusion counts aggregate held-out predictions across folds; absent combinations imply zero counts.

The supplied dataset has 200 observations split into five folds of 40. Results compare k=1,3,5. These folds evaluate configurations; choosing k from the same results is model selection, not an independent final test. Feature units, sampling design and fold-generation procedure are unspecified. Duplicate or related observations across folds could affect validity. No deployment or population-performance claim is made.

The example is synthetic. Source observation-level data are not bundled. Python 3.10 or newer is required; no external packages are needed.
