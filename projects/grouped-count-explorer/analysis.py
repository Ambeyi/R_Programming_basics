"""Aggregate grouped child and mother counts without averaging cell ratios."""
import itertools
import numpy as np
import pandas as pd

LEVELS={'duration':['0-4','5-9','10-14','15-19','20-24','25-29'],
        'residence':['Suva','urban','rural'],'education':['none','lower','upper','sec+']}
KEYS=list(LEVELS)

def validate(frame):
    required=KEYS+['nMother','nChildren']
    if frame.empty or not set(required).issubset(frame.columns):
        raise ValueError('Missing required columns or empty input')
    d=frame[required].copy()
    if d.isna().any().any():raise ValueError('Required values cannot be missing')
    for name,levels in LEVELS.items():
        if not d[name].isin(levels).all():raise ValueError('Unknown level in '+name)
    if d.duplicated(KEYS).any():raise ValueError('Duplicate category combination')
    for name in ['nMother','nChildren']:
        d[name]=pd.to_numeric(d[name],errors='raise')
        if not (np.isfinite(d[name])&(d[name]%1==0)&(d[name]>=0)).all():
            raise ValueError('Counts must be finite nonnegative integers')
    if (d.nMother==0).any():raise ValueError('Mother count must be positive for observed cells')
    return d

def aggregate(d,dimensions):
    result=d.groupby(dimensions,sort=False).agg(cells=('nMother','size'),
        mothers=('nMother','sum'),children=('nChildren','sum')).reset_index()
    result['children_per_mother']=result.children/result.mothers
    for name in dimensions:
        result[name]=pd.Categorical(result[name],categories=LEVELS[name],ordered=True)
    return result.sort_values(dimensions).reset_index(drop=True)

def analyze(frame):
    d=validate(frame)
    observed=set(d[KEYS].itertuples(index=False,name=None))
    missing=[dict(zip(KEYS,cell)) for cell in itertools.product(*LEVELS.values()) if cell not in observed]
    summaries={name:aggregate(d,[name]) for name in KEYS}
    summaries['duration_residence']=aggregate(d,['duration','residence'])
    summaries['missing_cells']=pd.DataFrame(missing,columns=KEYS)
    summary=dict(observed_cells=len(d),possible_cells=72,missing_cells=len(missing),
        mothers=int(d.nMother.sum()),children=int(d.nChildren.sum()),
        children_per_mother=float(d.nChildren.sum()/d.nMother.sum()))
    return summaries,summary
