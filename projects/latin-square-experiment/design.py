"""Balanced four-by-four Latin-square simulation."""
import numpy as np
import pandas as pd

FACTORS = ['athlete', 'trial', 'shoe']

def simulate(seed=123, noise_sd=1.5):
    if not np.isfinite(noise_sd) or noise_sd < 0:
        raise ValueError('noise_sd must be finite and nonnegative')
    athlete = np.repeat(np.arange(1, 5), 4)
    trial = np.tile(np.arange(1, 5), 4)
    shoe = (athlete + trial - 2) % 4 + 1
    expected = (53 + np.array([0, -2, 3, 4])[athlete-1]
                + np.array([0, -1, 1, 3])[trial-1]
                + np.array([0, 3, 5, 1])[shoe-1])
    return pd.DataFrame(dict(athlete=athlete, trial=trial, shoe=shoe,
        time=expected + np.random.default_rng(seed).normal(0, noise_sd, 16)))

def validate(frame):
    if not set(FACTORS + ['time']).issubset(frame.columns):
        raise ValueError('Required columns: athlete, trial, shoe, time')
    if len(frame) != 16 or frame[FACTORS + ['time']].isna().any().any():
        raise ValueError('Expected 16 complete observations')
    if not np.isfinite(frame['time'].astype(float)).all():
        raise ValueError('Times must be finite')
    for factor in FACTORS:
        if set(frame[factor]) != {1, 2, 3, 4}:
            raise ValueError('Factor levels must be 1, 2, 3, 4')
    for left, right in [('athlete', 'trial'), ('athlete', 'shoe'), ('trial', 'shoe')]:
        if frame.groupby([left, right]).size().shape[0] != 16:
            raise ValueError('Every factor pair must occur exactly once')
