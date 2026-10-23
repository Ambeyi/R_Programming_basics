"""Audit a locally supplied construction-estimates CSV; publish aggregates only."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES = ['Material_Cost', 'Labor_Cost', 'Profit_Rate', 'Discount_or_Markup']
REQUIRED = FEATURES + ['Total_Estimate']

def analyze(frame):
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    data = frame[REQUIRED].apply(pd.to_numeric, errors='raise')
    if len(data) <= len(FEATURES) + 1 or not np.isfinite(data.to_numpy()).all():
        raise ValueError('Require more than five complete, finite observations')
    x = np.column_stack([np.ones(len(data)), data[FEATURES].to_numpy()])
    y = data.Total_Estimate.to_numpy()
    coef, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != x.shape[1]:
        raise ValueError('Regression design is rank deficient')
    residual = y - x @ coef
    formula = (data.Material_Cost + data.Labor_Cost) * (1 + data.Profit_Rate / 100) + data.Discount_or_Markup
    error = y - formula.to_numpy()
    sst = float(np.sum((y - y.mean()) ** 2))
    return {
        'rows': len(data),
        'duplicate_numeric_rows': int(data.duplicated().sum()),
        'formula': '(Material_Cost + Labor_Cost) * (1 + Profit_Rate / 100) + Discount_or_Markup',
        'formula_max_absolute_error': float(np.max(np.abs(error))),
        'formula_rows_within_one_cent': int(np.sum(np.abs(error) <= 0.01)),
        'additive_ols_coefficients': dict(zip(['Intercept'] + FEATURES, map(float, coef))),
        'additive_ols_rmse_in_sample': float(np.sqrt(np.mean(residual ** 2))),
        'additive_ols_r_squared_in_sample': None if sst == 0 else float(1 - residual @ residual / sst),
        'interpretation': 'Descriptive in-sample audit; no causal or out-of-sample claim. Currency and upstream provenance are unknown.'
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path)
    parser.add_argument('--output', type=Path, default=Path('results/audit.json'))
    args = parser.parse_args()
    result = analyze(pd.read_csv(args.csv))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    print(json.dumps(result, indent=2, allow_nan=False))
