"""Standardized principal components for 28 five-point survey items."""
import numpy as np
import pandas as pd
ITEMS=[f'Q{i}' for i in range(1,29)]

def analyze(frame):
    if len(frame)<3 or not set(ITEMS).issubset(frame.columns):
        raise ValueError('At least three rows and Q1 through Q28 are required')
    d=frame[ITEMS].apply(pd.to_numeric,errors='raise')
    x=d.to_numpy(dtype=float)
    if not np.isfinite(x).all() or not ((x>=1)&(x<=5)&(x%1==0)).all():
        raise ValueError('Responses must be complete integer ratings from 1 through 5')
    means=x.mean(axis=0);sd=x.std(axis=0,ddof=1)
    if (sd==0).any():raise ValueError('Each item must vary')
    z=(x-means)/sd
    correlation=z.T@z/(len(x)-1)
    eigenvalues,vectors=np.linalg.eigh(correlation)
    order=np.argsort(eigenvalues)[::-1];eigenvalues=np.maximum(eigenvalues[order],0);vectors=vectors[:,order]
    for j in range(28):
        if vectors[np.argmax(abs(vectors[:,j])),j]<0:vectors[:,j]*=-1
    ratios=eigenvalues/eigenvalues.sum()
    spectrum=pd.DataFrame({'component':range(1,29),'eigenvalue':eigenvalues,'explained_ratio':ratios,'cumulative_ratio':np.cumsum(ratios)})
    items=pd.DataFrame({'item':ITEMS,'responses':len(x),'mean':means,'sample_sd':sd,'median':np.median(x,axis=0)})
    loadings=pd.DataFrame(vectors[:,:5]*np.sqrt(eigenvalues[:5]),index=ITEMS,columns=[f'PC{i}' for i in range(1,6)]).rename_axis('item').reset_index()
    summary=dict(responses=len(x),items=28,components_for_80_percent=int(np.searchsorted(np.cumsum(ratios),.8)+1),first_five_explained_ratio=float(ratios[:5].sum()))
    return items,spectrum,loadings,summary
