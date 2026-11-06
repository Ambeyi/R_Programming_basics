"""Additive least squares and partial F tests for a Latin square."""
import numpy as np
import pandas as pd
from scipy.stats import f
from design import FACTORS, validate

def matrix(frame, factors):
    columns = [np.ones(len(frame))]
    names = ['intercept']
    for factor in factors:
        for level in [2, 3, 4]:
            columns.append((frame[factor].to_numpy() == level).astype(float))
            names.append(f'{factor}_{level}_vs_1')
    return np.column_stack(columns), names

def analyze(frame):
    validate(frame)
    y = frame.time.to_numpy(dtype=float)
    x, names = matrix(frame, FACTORS)
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    residual = y - x @ beta
    sse = float(residual @ residual)
    df_error = len(y) - np.linalg.matrix_rank(x)
    mse = sse / df_error
    if mse <= 1e-20:
        raise ValueError('Residual variation is too small for F tests')
    rows = []
    for factor in FACTORS:
        reduced, _ = matrix(frame, [v for v in FACTORS if v != factor])
        error = y - reduced @ np.linalg.lstsq(reduced, y, rcond=None)[0]
        ss = max(0., float(error @ error) - sse)
        statistic = ss / 3 / mse
        rows.append(dict(source=factor, df=3, sum_squares=ss,
                         mean_square=ss/3, f_statistic=statistic,
                         p_value=float(f.sf(statistic, 3, df_error))))
    return (pd.DataFrame(rows), pd.DataFrame(dict(term=names, estimate=beta)),
            dict(observations=len(y), residual_df=int(df_error), residual_sum_squares=sse,
                 residual_mean_square=mse, total_sum_squares=float(((y-y.mean())**2).sum())))
