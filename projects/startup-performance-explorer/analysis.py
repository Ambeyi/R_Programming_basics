"""Descriptive startup performance summaries with strict validation."""
import numpy as np
import pandas as pd

NUMERIC=['Equipment','Website','Payroll','Office Furniture and Supplies','Professional Consultants','Profit','Sales']
REQUIRED=['City','StartYear','IsSuccessful']+NUMERIC

def validate(frame):
    if not set(REQUIRED).issubset(frame.columns) or frame.empty:
        raise ValueError('Input must contain nonempty required columns')
    d=frame[REQUIRED].copy()
    if d.isna().any().any():raise ValueError('Required values cannot be missing')
    if not d.City.map(lambda x:isinstance(x,str) and bool(x.strip())).all():
        raise ValueError('City must be nonempty text')
    d.City=d.City.str.strip()
    for name in ['StartYear','IsSuccessful']+NUMERIC:
        d[name]=pd.to_numeric(d[name],errors='raise')
        if not np.isfinite(d[name]).all():raise ValueError('Numeric values must be finite')
    if not d.IsSuccessful.isin([0,1]).all():raise ValueError('Success labels must be 0 or 1')
    if not ((d.StartYear%1==0)&d.StartYear.between(1800,2200)).all():raise ValueError('Invalid founding year')
    d.StartYear=d.StartYear.astype(int)
    if (d[[x for x in NUMERIC if x!='Profit']]<0).any().any():raise ValueError('Spending and sales cannot be negative')
    return d

def grouped(d,dimension):
    return d.groupby(dimension,sort=True).agg(records=('Profit','size'),successes=('IsSuccessful','sum'),
        success_rate=('IsSuccessful','mean'),mean_profit=('Profit','mean'),median_profit=('Profit','median'),
        total_profit=('Profit','sum'),total_sales=('Sales','sum')).reset_index()

def analyze(frame):
    d=validate(frame)
    correlations=[]
    for name in [x for x in NUMERIC if x!='Profit']:
        defined=len(d)>1 and d[name].nunique()>1 and d.Profit.nunique()>1
        correlations.append(dict(variable=name,pearson_r=float(d[name].corr(d.Profit)) if defined else None,
                                 status='defined' if defined else 'constant_or_insufficient',records=len(d)))
    summary=dict(records=len(d),cities=int(d.City.nunique()),successes=int(d.IsSuccessful.sum()),
                 success_rate=float(d.IsSuccessful.mean()),mean_profit=float(d.Profit.mean()),
                 earliest_start_year=int(d.StartYear.min()),latest_start_year=int(d.StartYear.max()))
    return grouped(d,'City'),grouped(d,'StartYear'),pd.DataFrame(correlations),summary
