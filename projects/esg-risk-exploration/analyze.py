"""Audit and summarize an ESG panel workbook; publish aggregate outputs only."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

METRICS = ['Delta-CoVaR', 'MES', 'NSRISK', 'ESG Combined Score',
           'Environmental Pillar Score', 'Social Pillar Score', 'Governance Pillar Score']


def analyze(source, output):
    data = pd.read_excel(source)
    required = ['Entity Name', 'Year'] + METRICS
    missing = sorted(set(required)-set(data.columns))
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    if data[['Entity Name', 'Year']].isna().any().any():
        raise ValueError('Panel identifiers contain missing values')
    if data.duplicated(['Entity Name','Year']).any():
        raise ValueError('Duplicate entity-year observations')
    if not pd.api.types.is_numeric_dtype(data['Year']) or not np.isfinite(data['Year']).all() or (data['Year'] % 1 != 0).any():
        raise ValueError('Years must be finite integers')
    numeric = data[METRICS].apply(pd.to_numeric, errors='raise')
    if np.isinf(numeric.to_numpy()).any():
        raise ValueError('Infinite metric values')
    if any(numeric[c].dropna().nunique() < 2 for c in METRICS):
        raise ValueError('Each metric needs at least two distinct observed values')
    output.mkdir(parents=True, exist_ok=True)
    audit = {'rows': len(data), 'entities': int(data['Entity Name'].nunique()),
             'year_min': int(data.Year.min()), 'year_max': int(data.Year.max()),
             'duplicate_entity_years': 0,
             'complete_metric_rows': int(numeric.notna().all(axis=1).sum()),
             'missing_by_metric': {c:int(numeric[c].isna().sum()) for c in METRICS}}
    (output/'audit.json').write_text(json.dumps(audit, indent=2)+'\n', encoding='utf-8')
    numeric.describe().T.to_csv(output/'descriptive_statistics.csv')
    numeric.corr(min_periods=3).to_csv(output/'pearson_correlations.csv')
    present = numeric.notna().astype('int64')
    present.T.dot(present).to_csv(output/'correlation_pair_counts.csv')
    grouped = numeric.assign(Year=data.Year).groupby('Year')
    grouped.mean().to_csv(output/'annual_means.csv')
    grouped.count().to_csv(output/'annual_counts.csv')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workbook', type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'results')
    args = parser.parse_args()
    analyze(args.workbook, args.output)
