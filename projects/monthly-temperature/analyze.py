"""Summarize monthly temperature series without filling missing months."""
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd

def analyze(frame):
 if not {'Year','Month','Value'}<=set(frame): raise ValueError('Year, Month and Value required')
 d=frame[['Year','Month','Value']].apply(pd.to_numeric,errors='raise')
 if d.empty or not np.isfinite(d.to_numpy()).all(): raise ValueError('Complete finite observations required')
 if not d.Year.between(1,9999).all() or not d.Month.between(1,12).all() or (d[['Year','Month']]%1!=0).any().any(): raise ValueError('Invalid year or month')
 if d.duplicated(['Year','Month']).any(): raise ValueError('Duplicate year-month')
 d=d.sort_values(['Year','Month'])
 annual=d.groupby('Year').Value.agg(months='count',mean='mean',minimum='min',maximum='max')
 annual['complete_year']=annual.months==12
 seasonal=d.groupby('Month').Value.agg(observations='count',mean='mean',sd='std')
 metrics=dict(observations=len(d),first_year=int(d.Year.min()),last_year=int(d.Year.max()),complete_years=int(annual.complete_year.sum()),incomplete_years=int((~annual.complete_year).sum()))
 return annual,seasonal,metrics
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--output',default='results');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 annual,seasonal,metrics=analyze(pd.read_csv(a.input));annual.to_csv(out/'annual_summary.csv');seasonal.to_csv(out/'seasonal_summary.csv');(out/'summary.json').write_text(json.dumps(metrics,indent=2));print(metrics)
